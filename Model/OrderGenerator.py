import pandas as pd
import numpy as np


class SalesData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.unique_records = self.data[~self.data.duplicated(['PRODUCTCODE'])]
        self.codes = self.unique_records['PRODUCTCODE'].to_numpy()

    def get_product_data(self, product_code,):
        df = pd.read_csv(
            fr'DataBases/Product_{product_code}.csv')
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='mixed')
        df.set_index('ORDERDATE', inplace=True)
        df = df.sort_index()
        product_data = df[['QUANTITYORDERED', 'PRODUCTCODE', 'PRODUCTLINE']].to_numpy()
        last_stock = df[['STOCK']].iloc[-1].values[0]
        return product_data, last_stock


class SalesAnalysis:
    def __init__(self, sales_data, window_size=3):
        self.sales_data = sales_data
        self.window_size = window_size

    def moving_average_sales(self):
        sales_data_num = self.sales_data[:, 0]
        moving_averages = []
        for i in range(len(self.sales_data) - self.window_size + 1):
            window = sales_data_num[i:i + self.window_size]
            average = sum(window) / self.window_size
            moving_averages.append([average, ])
        return moving_averages

    def predict_next_month_sales(self):
        moving_averages = self.moving_average_sales()
        prediction = int(np.sum(moving_averages) / len(moving_averages)) + np.random.randint(1, 20)
        order = [prediction, self.sales_data[0, 1], self.sales_data[0, 2]]
        return order


class OrderGenerator:
    def __init__(self, sales_data_file):
        self.sales_data = SalesData(sales_data_file)
        self.data_matrix = []
        self.stock = []

    def load_data(self):
        for code in self.sales_data.codes:
            product_data, last_stock = self.sales_data.get_product_data(code)
            self.data_matrix.append(product_data)
            self.stock.append(last_stock)

    def generate_orders(self):
        self.load_data()
        predictions = []
        orders = []
        window_size = 3

        for product_data in self.data_matrix:
            analysis = SalesAnalysis(product_data, window_size)
            next_month_prediction = analysis.predict_next_month_sales()
            predictions.append(next_month_prediction)

        for i in range(len(predictions)):
            order_quantity = 0
            if predictions[i][0] > self.stock[i]:
                order_quantity = predictions[i][0] - self.stock[i] + np.random.randint(1, 15)
            orders.append(
                [order_quantity, predictions[i][1], predictions[i][2], predictions[i][1] + '_' + predictions[i][2]])

        orders = np.array(orders)
        indices = orders[:, 0] != '0'
        orders = orders[indices]
        df = pd.DataFrame(orders, columns=['Cantidad', 'Codigo', 'Nombre', 'Modelo'])
        return df

