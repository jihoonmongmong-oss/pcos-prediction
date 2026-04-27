import os
from urllib.parse import unquote, urlparse


def _get_database_config():
    database_url = (
        os.getenv('DATABASE_URL')
        or os.getenv('MYSQL_DATABASE_URL')
        or os.getenv('CLEARDB_DATABASE_URL')
    )
    if database_url:
        parsed = urlparse(database_url)
        return {
            'host': parsed.hostname or '127.0.0.1',
            'port': parsed.port or 3306,
            'user': parsed.username or 'root',
            'password': unquote(parsed.password) if parsed.password else '',
            'database': parsed.path.lstrip('/') or 'pcos_prediction',
        }

    return {
        'host': os.getenv('DB_HOST', os.getenv('MYSQL_HOST', '127.0.0.1')),
        'port': int(os.getenv('DB_PORT', os.getenv('MYSQL_PORT', 3306))),
        'user': os.getenv('DB_USER', os.getenv('MYSQL_USER', 'root')),
        'password': os.getenv('DB_PASSWORD', os.getenv('MYSQL_PASSWORD', '')),
        'database': os.getenv('DB_NAME', os.getenv('MYSQL_DATABASE', 'pcos_prediction')),
    }


DB_CONFIG = _get_database_config()
MODEL_PATH = os.getenv('MODEL_PATH', 'model.pkl')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret')
