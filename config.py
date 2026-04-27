import os
from urllib.parse import unquote, urlparse


def _get_database_config():
    # Try standard database URLs first (Railway supports this)
    database_url = (
        os.getenv('DATABASE_URL')
        or os.getenv('MYSQL_URL')
        or os.getenv('MYSQL_DATABASE_URL')
        or os.getenv('CLEARDB_DATABASE_URL')
    )

    if database_url:
        parsed = urlparse(database_url)
        return {
            'host': parsed.hostname,
            'port': parsed.port or 3306,
            'user': parsed.username,
            'password': unquote(parsed.password) if parsed.password else '',
            'database': parsed.path.lstrip('/'),
        }

    # Fallback: Railway-specific environment variables
    return {
        'host': os.getenv('MYSQLHOST', '127.0.0.1'),
        'port': int(os.getenv('MYSQLPORT', 3306)),
        'user': os.getenv('MYSQLUSER', 'root'),
        'password': os.getenv('MYSQLPASSWORD', ''),
        'database': os.getenv('MYSQLDATABASE', 'pcos_prediction'),
    }


DB_CONFIG = _get_database_config()
MODEL_PATH = os.getenv('MODEL_PATH', 'model.pkl')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret')
