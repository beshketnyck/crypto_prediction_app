import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mama-mia'
    API_KEY = os.environ.get('API_KEY') or 'CG-qfTXGpXEPTzGvUWAHPCGEpa8	'
    # Додайте інші конфігураційні параметри тут

# Тут ми визначаємо клас Config, який містить конфігураційні параметри для нашого додатку.
# SECRET_KEY використовується для захисту сесій і інших конфіденційних даних.