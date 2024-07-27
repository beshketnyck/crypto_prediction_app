import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from app.train_model import prepare_data, train_model
from app.data_analyser import DataAnalyser

class TestModel(unittest.TestCase):
    
    def setUp(self):
        # Створюємо тестові дані з правильними стовпцями
        self.data = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2023', periods=100),
            'Price': np.random.rand(100) * 100,
            'Feature1': np.random.rand(100),
            'Feature2': np.random.rand(100)
        })
        print("Test Data:\n", self.data.head())  # Додаємо відладковий код для перевірки даних
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index('Date', inplace=True)
        
    def test_prepare_data(self):
        # Тестуємо функцію prepare_data
        features, target = prepare_data(self.data)
        self.assertIn('Feature1', features.columns)
        self.assertIn('Feature2', features.columns)
        self.assertNotIn('Price', features.columns)
        self.assertTrue(target.equals(self.data['Price']))

    def test_train_model(self):
        # Тестуємо функцію train_model
        features, target = prepare_data(self.data)
        model, rmse = train_model(features, target)
        self.assertIsNotNone(model)
        self.assertGreater(rmse, 0)

    def test_fetch_data(self):
        # Тестуємо метод fetch_data класу DataAnalyser
        api_url = 'https://api.mock.com/cryptodata'
        analyser = DataAnalyser(api_url)
        start_date = '2023-01-01'
        end_date = '2023-01-10'
        
        # Створюємо мок для requests.get
        with patch('app.data_analyser.requests.get') as mock_get:
            mock_get.return_value.json.return_value = self.data.reset_index().to_dict(orient='records')
            data = analyser.fetch_data(start_date, end_date)
            self.assertEqual(len(data), 100)

    def test_calculate_moving_average(self):
        # Тестуємо метод calculate_moving_average класу DataAnalyser
        analyser = DataAnalyser('')
        moving_average = analyser.calculate_moving_average(self.data, window_size=5)
        self.assertEqual(len(moving_average.dropna()), 96)  # 100 - window_size + 1

    def test_calculate_volatility(self):
        # Тестуємо метод calculate_volatility класу DataAnalyser
        analyser = DataAnalyser('')
        volatility = analyser.calculate_volatility(self.data, window_size=5)
        self.assertEqual(len(volatility.dropna()), 96)  # 100 - window_size + 1

if __name__ == '__main__':
    unittest.main()
