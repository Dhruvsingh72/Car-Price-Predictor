import sqlite3
from datetime import datetime

DB_FILE = "car_analytics.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            brand TEXT,
            model TEXT,
            year INTEGER,
            km_driven INTEGER,
            fuel TEXT,
            transmission TEXT,
            predicted_price REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_prediction(brand, model, year, km_driven, fuel, transmission, predicted_price):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prediction_logs (brand, model, year, km_driven, fuel, transmission, predicted_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (brand, model, year, km_driven, fuel, transmission, predicted_price))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_FILE)
    # Return rows as dictionaries for easier pandas conversion
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prediction_logs ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
