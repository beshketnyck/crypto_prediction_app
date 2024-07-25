from flask import render_template, request
from . import create_app
from .models.crypto_api import CryptoAPI
from .models.data_analyser import DataAnalyser

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    days = request.form.get('days', 30)
    crypto_api = CryptoAPI()
    data = crypto_api.fetch_data(days)
    if data is not None:
        data.to_csv('data/bitcoin_price_data.csv', index=False)
        return "Data fetched and saved successfully."
    else:
        return "Error fetching data."

@app.route('/analyze_data', methods=['POST'])
def analyze_data():
    analyser = DataAnalyser('data/bitcoin_price_data.csv')
    analyser.load_data()
    analyser.calculate_moving_average(period=30)
    analyser.plot_data()
    return "Data analyzed and plotted successfully."
