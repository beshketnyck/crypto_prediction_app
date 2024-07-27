import requests
import pandas as pd

class DataAnalyser:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, start_date, end_date):
        # Запит даних з API
        response = requests.get(self.api_url, params={'start': start_date, 'end': end_date})
        data = response.json()

        # Перетворення JSON-даних в DataFrame
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        return df

    def calculate_moving_average(self, data, window_size):
        # Обчислення ковзного середнього
        moving_average = data['Price'].rolling(window=window_size).mean()
        return moving_average

    def calculate_volatility(self, data, window_size):
        # Обчислення волатильності
        volatility = data['Price'].rolling(window=window_size).std()
        return volatility

# Основна частина, де ми створюємо екземпляр DataAnalyser і виконуємо аналіз даних
if __name__ == '__main__':
    api_url = 'https://api.example.com/cryptodata'
    analyser = DataAnalyser(api_url)

    start_date = '2023-01-01'
    end_date = '2023-06-30'
    data = analyser.fetch_data(start_date, end_date)

    moving_average = analyser.calculate_moving_average(data, window_size=30)
    volatility = analyser.calculate_volatility(data, window_size=30)

    print(f'Moving Average:\n{moving_average}')
    print(f'Volatility:\n{volatility}')
