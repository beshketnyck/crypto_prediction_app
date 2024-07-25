import unittest
import pandas as pd
from sklearn.metrics import mean_squared_error
from datetime import datetime
import pickle

class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = 'data/bitcoin_price_data.csv'
        cls.model_path = 'model.pkl'
        cls.start_date = '2024-01-01'
        cls.end_date = '2024-06-30'
        cls.data = pd.read_csv(cls.data_path)
        cls.test_data = cls.prepare_test_data(cls.data, cls.start_date, cls.end_date)

    @staticmethod
    def prepare_test_data(data, start_date, end_date):
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        test_data = data[(data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)]
        test_data['day_of_year'] = test_data['timestamp'].dt.dayofyear
        test_data['year'] = test_data['timestamp'].dt.year
        test_data['volume'] = test_data['volume'].fillna(test_data['volume'].mean())
        test_data['average_daily_volume'] = test_data['volume'].rolling(window=7).mean().fillna(method='bfill')
        test_data['volatility'] = test_data['current_price'].rolling(window=7).std().fillna(method='bfill')
        return test_data

    def test_load_data(self):
        self.assertTrue(not self.data.empty)
        print(f"Data loaded: {self.data.shape[0]} rows, {self.data.shape[1]} columns")

    def test_prepare_test_data(self):
        self.assertTrue(not self.test_data.empty)
        print(f"Test data prepared: {self.test_data.shape[0]} rows")

    def test_model(self):
        features = ['day_of_year', 'year', 'volume', 'average_daily_volume', 'volatility']
        X_test = self.test_data[features]
        y_test = self.test_data['current_price']

        with open(self.model_path, 'rb') as model_file:
            model = pickle.load(model_file)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        self.assertTrue(mse < 1000000)
        print(f"Mean Squared Error on test data: {mse}")

        result = pd.DataFrame({
            'timestamp': self.test_data['timestamp'],
            'predicted_price': predictions,
            'actual_price': y_test
        })
        print(result)

if __name__ == "__main__":
    unittest.main()
