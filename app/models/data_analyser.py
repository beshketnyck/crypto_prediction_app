import pandas as pd
import matplotlib.pyplot as plt

class DataAnalyser:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.data

    def calculate_moving_average(self, period):
        self.data['moving_average'] = self.data['current_price'].rolling(window=period).mean()
        self.data['moving_average'].fillna(method='bfill', inplace=True)  # Заповнення NaN значень
        return self.data

    def plot_data(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['timestamp'], self.data['current_price'], label='Current Price')
        plt.plot(self.data['timestamp'], self.data['moving_average'], label='Moving Average')
        
        # Налаштування для перевертання написів з датами та додавання цін
        for x, y in zip(self.data['timestamp'], self.data['current_price']):
            label = f"{y:.2f}"
            plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')
        
        plt.xticks(rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Price in USD')
        plt.title('Bitcoin Price and Moving Average')
        plt.legend()
        plt.tight_layout()  # Зміна для кращого відображення графіка
        plt.show()
