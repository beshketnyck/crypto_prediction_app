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
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Графік ціни та ковзного середнього
        ax1.plot(self.data['timestamp'], self.data['current_price'], label='Current Price', color='tab:blue')
        ax1.plot(self.data['timestamp'], self.data['moving_average'], label='Moving Average', color='tab:orange')

        # Налаштування для перевертання написів з датами та додавання цін у форматі $XX.XK
        for x, y in zip(self.data['timestamp'], self.data['current_price']):
            label = f"${y/1000:.1f}K"
            ax1.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='tab:blue')
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price in USD')
        ax1.tick_params(axis='x', rotation=90)
        ax1.legend(loc='upper left')

        # Додатковий графік об'єму торгів з іншою віссю Y
        ax2 = ax1.twinx()
        ax2.bar(self.data['timestamp'], self.data['volume'], alpha=0.2, label='Volume', color='tab:gray')
        ax2.set_ylabel('Volume')
        ax2.legend(loc='upper right')

        plt.title('Bitcoin Price and Moving Average')
        plt.tight_layout()  # Зміна для кращого відображення графіка
        plt.show()
