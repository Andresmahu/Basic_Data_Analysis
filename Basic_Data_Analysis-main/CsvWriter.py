import pandas as pd
import random
from datetime import timedelta

def CsvWriter(data):
    registros_unicos = data[~data.duplicated(['Codigo'])]
    Codigos = registros_unicos['Codigo'].to_numpy()

    for codigo in Codigos:
        # Leer el CSV original
        csv_original_path = fr'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\DataBase\Product_{codigo}.csv'
        csv_actual = pd.read_csv(csv_original_path)
        csv_actual['ORDERDATE'] = pd.to_datetime(csv_actual['ORDERDATE'], format='mixed')

        # Filtrar los registros del CSV que contienen los datos para actualizar
        data_filtrado = data[data['Codigo'] == codigo]

        # Calcular y actualizar los valores
        for _, row in data_filtrado.iterrows():
            cantidad = row['Cantidad']

            # Actualizar QUANTITYORDERED
            quantity_ordered = random.randint(int(cantidad)//2, int(cantidad))

            # Actualizar ORDERDATE
            order_date = pd.to_datetime(csv_actual['ORDERDATE'].max()) + timedelta(days=30)
            order_date = order_date.strftime('%m-%d-%Y %H:%M:%S')
            # Calcular y actualizar STOCK
            stock_last = csv_actual['STOCK'].iloc[-1] if not csv_actual.empty else 0
            stock_new = int(stock_last) + int(cantidad) - int(quantity_ordered)

            # Crear un nuevo registro
            new_record = {
                'QUANTITYORDERED': quantity_ordered,
                'PRODUCTLINE': row['Nombre'],  # Suponiendo que 'Nombre' corresponde a 'PRODUCTLINE'
                'PRODUCTCODE': row['Codigo'],
                'ORDERDATE': order_date,
                'STOCK': stock_new
            }

            # Agregar el nuevo registro al CSV original
            nuevos_registros = pd.DataFrame(columns=csv_actual.columns)
            nuevos_registros = pd.concat([nuevos_registros, pd.DataFrame([new_record])], ignore_index=True)
            csv_actual = pd.concat([csv_actual, nuevos_registros], ignore_index=True)

        # Guardar el DataFrame actualizado en el CSV
        csv_actual.to_csv(csv_original_path, index=False)
