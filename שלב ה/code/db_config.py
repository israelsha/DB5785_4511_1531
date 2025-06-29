import psycopg2
from tkinter import messagebox

DB_CONFIG = {
    'dbname': 'DBProject',
    'user': 'israel_sha',
    'password': '4321',
    'host': 'localhost',
    'port': '5432'
}

def connect_to_db():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        return None
