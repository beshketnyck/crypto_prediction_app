from flask import render_template, request
from . import main
from ..models.crypto_api import CryptoAPI
from ..models.data_analyser import DataAnalyser
import pandas as pd
import os

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/fetch_data', methods=['POST'])
def fetch_data():
    days = int(request.form.get('days', 30))
    crypto_api = CryptoAPI(api_key="CG-qfTXGpXEPTzGvUWAHPCGEpa8")
    data = crypto_api.get_market_data('bitcoin', days)
    if data is not None and not data.empty:
        data.to_csv('data/bitcoin_price_data.csv', index=False)
        return "Data fetched and saved successfully."
    else:
        return "Error fetching data."

@main.route('/analyse_data', methods=['POST'])
def analyse_data():
    file_path = 'data/bitcoin_price_data.csv'
    if os.path.exists(file_path):
        analyser = DataAnalyser(file_path)
        data = analyser.load_data()
        period = int(request.form.get('period', 7))
        if 'current_price' in data.columns:
            analyser.calculate_moving_average(period=period)
            analyser.plot_data()
            return "Data analysis completed and plotted."
        else:
            return f"Error: 'current_price' column not found. Available columns: {list(data.columns)}"
    else:
        return "Data file not found."

@main.route('/train_model', methods=['POST'])
def train_model():
    file_path = 'data/bitcoin_price_data.csv'
    if os.path.exists(file_path):
        analyser = DataAnalyser(file_path)
        analyser.load_data()
        analyser.train_model()
        return "Model trained successfully."
    else:
        return "Data file not found."

@main.route('/predict', methods=['POST'])
def predict():
    file_path = 'data/bitcoin_price_data.csv'
    if os.path.exists(file_path):
        analyser = DataAnalyser(file_path)
        analyser.load_data()
        day_of_year = int(request.form.get('day_of_year'))
        year = int(request.form.get('year'))
        # Видаляємо об'єм торгів
        X = pd.DataFrame({'day_of_year': [day_of_year], 'year': [year]})
        prediction = analyser.predict(X)
        if prediction is not None:
            return f"Predicted price: ${prediction[0]:.2f}"
        else:
            return "Model is not trained yet."
    else:
        return "Data file not found."
