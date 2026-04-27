import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        auth_plugin='mysql_native_password'
    )


def init_db():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        conn.close()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                age INT NOT NULL,
                weight FLOAT NOT NULL,
                height FLOAT NOT NULL,
                blood_group VARCHAR(16) NOT NULL,
                menstrual_interval INT NOT NULL,
                weight_gain TINYINT(1) NOT NULL,
                hair_growth TINYINT(1) NOT NULL,
                skin_darkening TINYINT(1) NOT NULL,
                hair_loss TINYINT(1) NOT NULL,
                acne TINYINT(1) NOT NULL,
                fast_food TINYINT(1) NOT NULL,
                exercise TINYINT(1) NOT NULL,
                mood_swings TINYINT(1) NOT NULL,
                periods_regular TINYINT(1) NOT NULL,
                period_length INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                prediction TINYINT(1) NOT NULL,
                probability FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
    except Error as err:
        print('Database initialization error:', err)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
