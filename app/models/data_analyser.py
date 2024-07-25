import pandas as pd
import matplotlib.pyplot as plt

class DataAnalyser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.file_path)

    def calculate_moving_average(self, period):
        self.data['moving_average'] = self.data['current_price'].rolling(window=period).mean()

    def plot_data(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['date'], self.data['current_price'], label='Current Price')
        plt.plot(self.data['date'], self.data['moving_average'], label='Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price of Bitcoin')
        plt.legend()
        plt.show()
