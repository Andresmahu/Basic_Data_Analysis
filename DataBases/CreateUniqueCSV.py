# Importar la biblioteca pandas como 'pd' para manipulación de datos
import pandas as pd
# Importar la biblioteca numpy como 'np' para operaciones numéricas
import numpy as np
# Leer un archivo CSV y almacenarlo en un DataFrame de pandas llamado 'data'
data = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\sales_data_sample.csv')
# Eliminar los registros duplicados basados en la columna 'PRODUCTCODE' y almacenar los registros únicos en 'registros_unicos'
registros_unicos = data[~data.duplicated(['PRODUCTCODE'])]
#Convertir la columna 'PRODUCTCODE' de 'registros_unicos' en un array de numpy llamado 'Codigos'
Codigos = registros_unicos['PRODUCTCODE'].to_numpy()
# Iterar sobre cada código de producto en 'Codigos'
for codigo in Codigos:
    # Filtrar el DataFrame original para obtener solo los registros con el código de producto actual
    data_filtrado = data[data['PRODUCTCODE'] == codigo]
    # Seleccionar solo las columnas 'QUANTITYORDERED', 'PRODUCTLINE', 'PRODUCTCODE' y 'ORDERDATE' de 'data_filtrado'
    data_filtrado = data_filtrado[['QUANTITYORDERED', 'PRODUCTLINE', 'PRODUCTCODE', 'ORDERDATE']]
    # Convertir la columna 'QUANTITYORDERED' en un array de numpy llamado 'Ventas'
    Ventas = data_filtrado['QUANTITYORDERED'].to_numpy()
    # Inicializar la lista 'Stock' con un valor inicial de 150
    Stock = [150]
    # Calcular los valores de 'STOCK' para los registros restantes
    for i in range(1, len(data_filtrado)):
        # Obtener el valor de 'QUANTITYORDERED' del registro anterior
        venta = data_filtrado['QUANTITYORDERED'].iloc[i - 1]
        # Obtener el valor de 'QUANTITYORDERED' del próximo registro
        proxima_venta = data_filtrado['QUANTITYORDERED'].iloc[i]
        # Si el stock actual menos la venta anterior es menor o igual a la próxima venta
        if Stock[-1] - venta <= proxima_venta:
            # Añadir al stock actual menos la venta anterior, un valor aleatorio entre la próxima venta y la próxima venta + 20
            Stock.append(Stock[-1] - venta + np.random.randint(proxima_venta, proxima_venta + 20))
        else:
            # Si no, simplemente restar la venta anterior del stock actual
            Stock.append(Stock[-1] - venta)
    # Agregar la columna 'STOCK' calculada a 'data_filtrado'
    data_filtrado['STOCK'] = Stock
    # Guardar 'data_filtrado' en un archivo CSV, nombrado según el código de producto actual
    data_filtrado.to_csv(f'Product_{codigo}.csv', index=False)
