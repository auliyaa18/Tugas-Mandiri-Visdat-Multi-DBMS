import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_DB_URL")

# --- 1. SETUP DBMS 1: SQLite (Lokal untuk Master Produk) ---
# Menggunakan path absolut berdasarkan letak file seed_coffee.py ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sqlite_path = os.path.join(BASE_DIR, "coffee_local.db")

conn_sqlite = sqlite3.connect(sqlite_path)
cursor = conn_sqlite.cursor()

# Buat tabel master menu kopi
cursor.execute("""
CREATE TABLE IF NOT EXISTS coffee_menu (
    product_id INTEGER PRIMARY KEY,
    coffee_name TEXT,
    category TEXT,
    price REAL
)
""")

# Masukkan data master produk
menu_data = [
    (1, 'Espresso', 'Hot Coffee', 18000),
    (2, 'Cappuccino', 'Hot Coffee', 25000),
    (3, 'Caffe Latte', 'Hot Coffee', 28000),
    (4, 'Americano', 'Hot Coffee', 20000),
    (5, 'Caramel Macchiato', 'Iced Coffee', 32000),
    (6, 'Matcha Latte', 'Non-Coffee', 30000),
    (7, 'Chocolate Blend', 'Non-Coffee', 27000),
]
cursor.executemany(
    "INSERT OR REPLACE INTO coffee_menu VALUES (?, ?, ?, ?)", menu_data
)
conn_sqlite.commit()
conn_sqlite.close()
print("✅ SQLite lokal (Master Produk) berhasil di-seed di:", sqlite_path)

# --- 2. SETUP DBMS 2: PostgreSQL Supabase (Cloud untuk Transaksi) ---
engine = create_engine(SUPABASE_URL)

# Data dummy transaksi penjualan kopi
transactions_data = pd.DataFrame({
    'transaction_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'product_id': [1, 3, 5, 2, 6, 4, 7, 3],
    'quantity': [2, 1, 3, 2, 1, 4, 2, 1],
    'store_location': [
        'Jakarta',
        'Bandung',
        'Surabaya',
        'Jakarta',
        'Bandung',
        'Surabaya',
        'Yogyakarta',
        'Jakarta',
    ],
    'payment_method': [
        'Cash',
        'QRIS',
        'Credit Card',
        'QRIS',
        'Cash',
        'QRIS',
        'Cash',
        'Credit Card',
    ],
    'transaction_date': [
        '2026-04-01',
        '2026-04-02',
        '2026-04-03',
        '2026-04-04',
        '2026-04-05',
        '2026-04-06',
        '2026-04-07',
        '2026-04-08',
    ],
})

# Masukkan ke database Supabase
transactions_data.to_sql(
    'coffee_transactions', engine, if_exists='replace', index=False
)
print("✅ PostgreSQL Supabase (Data Transaksi) berhasil di-seed!")