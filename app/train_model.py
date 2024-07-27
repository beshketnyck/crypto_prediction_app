import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Функція для завантаження даних
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Функція для підготовки даних
def prepare_data(data):
    # Конвертуємо стовпець Date до типу datetime
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

    # Вибираємо лише цінові особливості
    features = data.drop(columns=['Price'])
    target = data['Price']

    return features, target

# Функція для тренування моделі
def train_model(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    return model, rmse

# Основна частина, де ми завантажуємо дані, готуємо їх і тренуємо модель
if __name__ == '__main__':
    data = load_data('path_to_your_data.csv')
    features, target = prepare_data(data)
    model, rmse = train_model(features, target)
    print(f'Model RMSE: {rmse:.2f}')
