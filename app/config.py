import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_API_URL = 'https://api.coingecko.com/api/v3'
    API_KEY = os.environ.get('API_KEY') or 'CG-qfTXGpXEPTzGvUWAHPCGEpa8'
    # Додайте інші конфігураційні параметри тут

# Тут ми визначаємо клас Config, який містить конфігураційні параметри для нашого додатку.
# SECRET_KEY використовується для захисту сесій і інших конфіденційних даних.