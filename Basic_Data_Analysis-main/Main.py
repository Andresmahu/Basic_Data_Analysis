import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import matplotlib.pyplot as plt
data = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\sales_data_sample.csv')
ModelData=data[['SALES','QUANTITYORDERED']].to_numpy()
registros_unicos = data[~data.duplicated(['PRODUCTCODE'])]
Codigos=registros_unicos['PRODUCTCODE'].to_numpy()
DataMatrix=[]
ModelMatrix=[]
Tags=[]
DataTrainMatrix = []
DataTestMatrix = []
for codigo in Codigos:
    df = pd.read_csv(fr'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\DataBase\Product_{codigo}.csv')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    df.set_index('ORDERDATE', inplace=True)
    df = df.sort_index()
    Product_data = df[['QUANTITYORDERED']]
    DataMatrix.append(Product_data)
    df_unique = df[~df.duplicated(['PRODUCTCODE'])]
    Tags.append(df_unique[['PRODUCTLINE', 'PRODUCTCODE']].to_numpy())
    train_size = int(len(Product_data) * 0.8)
    train_data = Product_data.iloc[:train_size]
    test_data = Product_data.iloc[train_size:]
    DataTrainMatrix.append(train_data)
    DataTestMatrix.append(test_data)
forecasts = []
for train_data, test_data in zip(DataTrainMatrix, DataTestMatrix):
    model = sm.tsa.ARIMA(train_data, order=(5, 1, 2))
    model_fit = model.fit()
    ModelMatrix.append(model_fit)
    start = len(train_data)
    end = len(train_data) + len(test_data) - 1
    predictions = model_fit.predict(start=start, end=end, typ='levels')
    forecasts.append(predictions)
for codigo, forecast in zip(Codigos, forecasts):
    print(f'Pronóstico para el producto {codigo}:')
    print(forecast)
