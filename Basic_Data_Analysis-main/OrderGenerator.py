# Importar la biblioteca pandas como 'pd' para manipulación de datos
import pandas as pd
# Importar la biblioteca numpy como 'np' para operaciones numéricas
import numpy as np
# Definir la función DataLoad para cargar y procesar datos de ventas
def DataLoad():
    # Leer un archivo CSV y almacenarlo en un DataFrame de pandas llamado 'data'
    data = pd.read_csv(
        r'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\sales_data_sample.csv')
    # Eliminar los registros duplicados basados en la columna 'PRODUCTCODE' y almacenar los registros únicos en 'registros_unicos'
    registros_unicos = data[~data.duplicated(['PRODUCTCODE'])]
    # Convertir la columna 'PRODUCTCODE' de 'registros_unicos' en un array de numpy llamado 'Codigos'
    Codigos = registros_unicos['PRODUCTCODE'].to_numpy()
    # Inicializar listas vacías para almacenar matrices de datos y stock
    DataMatrix = []
    Stock = []
    # Iterar sobre cada código de producto en 'Codigos'
    for codigo in Codigos:
        # Leer un archivo CSV específico para cada producto y almacenarlo en un DataFrame
        df = pd.read_csv(
            fr'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\DataBase\Product_{codigo}.csv')
        # Convertir la columna 'ORDERDATE' a tipo datetime
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='mixed')
        # Establecer 'ORDERDATE' como índice del DataFrame
        df.set_index('ORDERDATE', inplace=True)
        # Ordenar el DataFrame por el índice (fecha de pedido)
        df = df.sort_index()
        # Seleccionar columnas específicas y convertirlas en un array de numpy
        Product_data = df[['QUANTITYORDERED', 'PRODUCTCODE', 'PRODUCTLINE']].to_numpy()
        # Obtener el último valor de la columna 'STOCK' y agregarlo a la lista 'Stock'
        UltimoStock = df[['STOCK']].iloc[-1].values[0]
        Stock.append(UltimoStock)
        # Agregar los datos del producto a 'DataMatrix'
        DataMatrix.append(Product_data)
    # Devolver 'DataMatrix' y 'Stock'
    return DataMatrix, Stock
# Definir la función moving_average_sales para calcular el promedio móvil de las ventas
def moving_average_sales(sales_data, window_size):
    # Extraer la columna de cantidad de ventas del array de datos de ventas
    sales_data_num = sales_data[:, 0]
    # Inicializar una lista vacía para almacenar los promedios móviles
    moving_averages = []
    # Calcular el promedio móvil para cada ventana de datos
    for i in range(len(sales_data) - window_size + 1):
        # Seleccionar una ventana de datos de ventas
        window = sales_data_num[i:i + window_size]
        # Calcular el promedio de la ventana
        average = sum(window) / window_size
        # Agregar el promedio a la lista de promedios móviles
        moving_averages.append([average, ])
    # Devolver la lista de promedios móviles
    return moving_averages
# Definir la función predict_next_month_sales para predecir las ventas del próximo mes
def predict_next_month_sales(sales_data, window_size):
    # Calcular los promedios móviles de los datos de ventas
    moving_averages = moving_average_sales(sales_data, window_size)
    # Calcular una predicción sumando los promedios móviles y ajustando con un valor aleatorio
    prediction = int(np.sum(moving_averages) / len(moving_averages)) + np.random.randint(1, 20)
    # Crear una lista con la predicción y los detalles del producto
    pedido = [prediction, sales_data[0, 1], sales_data[0, 2]]
    # Devolver la predicción
    return pedido
# Definir la función GenerateOrder para generar órdenes de pedido
def GenerateOrder():
    # Cargar datos y stock usando la función DataLoad
    DataMatrix, Stock = DataLoad()
    # Definir el tamaño de la ventana para el promedio móvil
    window_size = 3
    # Inicializar listas vacías para almacenar predicciones y pedidos
    predictions = []
    Pedidos = []
    # Iterar sobre cada conjunto de datos de producto en 'DataMatrix'
    for Product in DataMatrix:
        # Predecir las ventas del próximo mes para el producto actual
        next_month_prediction = predict_next_month_sales(Product, window_size)
        # Agregar la predicción a la lista de predicciones
        predictions.append(next_month_prediction)
    # Iterar sobre las predicciones para generar los pedidos
    for i in range(len(predictions)):
        pedido = 0
        # Si la predicción es mayor que el stock actual, calcular el pedido necesario
        if predictions[i][0] > Stock[i]:
            pedido = predictions[i][0] - Stock[i] + np.random.randint(1, 15)
        # Agregar el pedido a la lista de pedidos
        Pedidos.append([pedido, predictions[i][1], predictions[i][2], predictions[i][1] + '_' + predictions[i][2]])
    # Convertir la lista de pedidos en un array de numpy
    Pedidos = np.array(Pedidos)
    # Filtrar los pedidos que no son cero
    Indices = Pedidos[:, 0] != '0'
    Pedidos = Pedidos[Indices]
    # Convertir el array de pedidos en un DataFrame de pandas
    df = pd.DataFrame(Pedidos, columns=['Cantidad', 'Codigo', 'Nombre', 'Modelo'])
    # Devolver el DataFrame de pedidos
    return df
