import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    API_KEY = os.environ.get('CG-qfTXGpXEPTzGvUWAHPCGEpa8') or 'your-api-key'
