import pandas as pd
import random
from datetime import timedelta

class CsvUpdater:
    def __init__(self, data):
        self.data = data
        self.registros_unicos = data[~data.duplicated(['Codigo'])]
        self.codigos = self.registros_unicos['Codigo'].to_numpy()

    def update_csvs(self):
        for codigo in self.codigos:
            self.update_csv_for_codigo(codigo)

    def update_csv_for_codigo(self, codigo):
        csv_original_path = fr'DataBases/Product_{codigo}.csv'
        csv_actual = pd.read_csv(csv_original_path)
        csv_actual['ORDERDATE'] = pd.to_datetime(csv_actual['ORDERDATE'], format='mixed')

        data_filtrado = self.data[self.data['Codigo'] == codigo]

        for _, row in data_filtrado.iterrows():
            csv_actual = self.update_row(csv_actual, row)

        csv_actual.to_csv(csv_original_path, index=False)

    def update_row(self, csv_actual, row):
        cantidad = row['Cantidad']
        quantity_ordered = random.randint(int(cantidad) // 2, int(cantidad))

        order_date = pd.to_datetime(csv_actual['ORDERDATE'].max()) + timedelta(days=30)
        order_date = order_date.strftime('%m-%d-%Y %H:%M:%S')

        stock_last = csv_actual['STOCK'].iloc[-1] if not csv_actual.empty else 0
        stock_new = int(stock_last) + int(cantidad) - int(quantity_ordered)

        new_record = {
            'QUANTITYORDERED': quantity_ordered,
            'PRODUCTLINE': row['Nombre'],
            'PRODUCTCODE': row['Codigo'],
            'ORDERDATE': order_date,
            'STOCK': stock_new
        }

        nuevos_registros = pd.DataFrame([new_record], columns=csv_actual.columns)
        csv_actual = pd.concat([csv_actual, nuevos_registros], ignore_index=True)
        return csv_actual


