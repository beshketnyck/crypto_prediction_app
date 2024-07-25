from flask import render_template, request
from .models.crypto_api import CryptoAPI
from .models.data_analyser import DataAnalyser
import pandas as pd
import os

from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    days = request.form.get('days', 30)
    crypto_api = CryptoAPI(api_key="YOUR_API_KEY")  # Вставте свій API ключ
    data = crypto_api.get_market_data('bitcoin')
    if data is not None:
        data.to_csv('data/bitcoin_price_data.csv', index=False)
        return "Data fetched and saved successfully."
    else:
        return "Error fetching data."

@app.route('/analyse_data', methods=['POST'])
def analyse_data():
    file_path = 'data/bitcoin_price_data.csv'
    if os.path.exists(file_path):
        analyser = DataAnalyser(file_path)
        data = analyser.load_data()
        print(data.columns)  # Додайте цей рядок для виводу стовпців
        if 'current_price' in data.columns:
            analyser.calculate_moving_average(period=7)
            analyser.plot_data()
            return "Data analysis completed and plotted."
        else:
            return f"Error: 'current_price' column not found. Available columns: {list(data.columns)}"
    else:
        return "Data file not found."