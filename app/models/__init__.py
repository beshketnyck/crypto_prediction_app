from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        # Імпорт маршрутів та моделей
        from . import routes
        from .models import crypto_api, data_analyser
    return app
