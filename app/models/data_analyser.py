import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

class DataAnalyser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = None

    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.data

    def calculate_moving_average(self, period):
        self.data['moving_average'] = self.data['current_price'].rolling(window=period).mean()
        self.data['moving_average'].fillna(method='bfill', inplace=True)
        return self.data

    def plot_data(self):
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(self.data['timestamp'], self.data['current_price'], label='Current Price', color='tab:blue')
        ax1.plot(self.data['timestamp'], self.data['moving_average'], label='Moving Average', color='tab:orange')

        for x, y in zip(self.data['timestamp'], self.data['current_price']):
            label = f"${y/1000:.1f}K"
            ax1.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center', color='tab:blue')
        
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price in USD')
        ax1.tick_params(axis='x', rotation=90)
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()
        ax2.bar(self.data['timestamp'], self.data['volume'], alpha=0.2, label='Volume', color='tab:gray')
        ax2.set_ylabel('Volume')
        ax2.legend(loc='upper right')

        plt.title('Bitcoin Price and Moving Average')
        plt.tight_layout()
        plt.show()

    def prepare_data_for_model(self):
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data['day_of_year'] = self.data['timestamp'].dt.dayofyear
        self.data['year'] = self.data['timestamp'].dt.year
        features = ['day_of_year', 'year']  # Видалили 'volume'
        X = self.data[features]
        y = self.data['current_price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_model(self):
        X_train, X_test, y_train, y_test = self.prepare_data_for_model()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Model Mean Squared Error: {mse}")
        with open('model.pkl', 'wb') as model_file:
            pickle.dump(self.model, model_file)

    def predict(self, X):
        if self.model is None:
            try:
                with open('model.pkl', 'rb') as model_file:
                    self.model = pickle.load(model_file)
            except FileNotFoundError:
                print("Model file not found. Train the model first.")
                return None
        return self.model.predict(X)
