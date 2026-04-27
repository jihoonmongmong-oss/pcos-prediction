import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'pcos_prediction'),
}

MODEL_PATH = os.getenv('MODEL_PATH', 'model.pkl')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret')
