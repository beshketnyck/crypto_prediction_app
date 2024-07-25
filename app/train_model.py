import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

def prepare_data(data_path):
    data = pd.read_csv(data_path)
    required_columns = ['timestamp', 'current_price', 'volume']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Required column '{col}' is missing from data")

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['day_of_year'] = data['timestamp'].dt.dayofyear
    data['year'] = data['timestamp'].dt.year
    data['volume'] = data['volume'].fillna(data['volume'].mean())
    data['average_daily_volume'] = data['volume'].rolling(window=7).mean().fillna(method='bfill')
    data['volatility'] = data['current_price'].rolling(window=7).std().fillna(method='bfill')
    return data

def train_model(file_path):
    data = prepare_data(file_path)
    features = ['day_of_year', 'year', 'volume', 'average_daily_volume', 'volatility']
    X = data[features]
    y = data['current_price']

    model = RandomForestRegressor()
    model.fit(X, y)

    with open('model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    data_path = 'data/bitcoin_price_data.csv'
    train_model(data_path)
