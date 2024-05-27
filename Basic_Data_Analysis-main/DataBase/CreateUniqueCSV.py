import pandas as pd
import numpy as np
data = pd.read_csv(r'C:\Users\Asus\PycharmProjects\Basic_Data_Analysis\Basic_Data_Analysis-main\sales_data_sample.csv')
print(data.columns)
print(data['QUANTITYORDERED'])
ModelData=data[['SALES','QUANTITYORDERED']].to_numpy()
registros_unicos = data[~data.duplicated(['PRODUCTCODE'])]
Codigos=registros_unicos['PRODUCTCODE'].to_numpy()
for codigo in Codigos:
    data_filtrado = data[data['PRODUCTCODE'] == codigo]
    data_filtrado = data_filtrado[['QUANTITYORDERED','PRODUCTLINE','PRODUCTCODE','ORDERDATE']]
    data_filtrado.to_csv(f'Product_{codigo}.csv', index=False)
print(registros_unicos[['PRODUCTLINE','PRODUCTCODE']])
