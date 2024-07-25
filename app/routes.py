from flask import render_template, request
from . import create_app
from .models.crypto_api import CryptoAPI
from .models.data_analyser import DataAnalyser
import pandas as pd
import os

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    days = request.form.get('days', 30)
    crypto_api = CryptoAPI(api_key="CG-qfTXGpXEPTzGvUWAHPCGEpa8")  # Вставте свій API ключ
    data = crypto_api.get_market_data('bitcoin')
    if data:
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.to_csv('data/bitcoin_price_data.csv', index=False)
        return "Data fetched and saved successfully."
    else:
        return "Error fetching data."

@app.route('/analyse_data', methods=['POST'])
def analyse_data():
    file_path = 'data/bitcoin_price_data.csv'
    if os.path.exists(file_path):
        analyser = DataAnalyser(file_path)
        data = analyser.load_data()
        analyser.calculate_moving_average(period=7)
        analyser.plot_data()
        return "Data analysis completed and plotted."
    else:
        return "Data file not found."
