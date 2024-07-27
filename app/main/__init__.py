# Імпорт необхідних бібліотек
from flask import Flask

# Функція для створення і конфігурації додатку Flask
def create_app():
    # Створення екземпляру додатку
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    # Конфігурація додатку з файлу config.py
    app.config.from_object('config.Config')

    # Імпорт і реєстрація блакитного принтера з файла routes.py
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Тут ми створюємо і конфігуруємо екземпляр додатку Flask.
# Імпортуємо файл routes.py, який містить маршрути (routes) нашого додатку, 
# і реєструємо його як "blueprint".
