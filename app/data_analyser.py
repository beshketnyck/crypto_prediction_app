import requests
import pandas as pd

class DataAnalyser:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, start_date, end_date):
        # Запит даних з API CoinGecko
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '1h,24h,7d'
        }
        response = requests.get(self.api_url, params=params)
        data = response.json()

        # Перетворення JSON-даних в DataFrame
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(start_date)
        df = df[['Date', 'name', 'current_price']]
        df.set_index('Date', inplace=True)

        return df

    def calculate_moving_average(self, data, window_size):
        # Обчислення ковзного середнього
        moving_average = data['current_price'].rolling(window=window_size).mean()
        return moving_average

    def calculate_volatility(self, data, window_size):
        # Обчислення волатильності
        volatility = data['current_price'].rolling(window=window_size).std()
        return volatility
