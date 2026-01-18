import sqlite3
import pandas as pd

DB_NAME = "trades.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        entry REAL,
        exit REAL,
        quantity REAL,
        pnl REAL,
        status TEXT,
        date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS backtests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        strategy TEXT,
        win_rate REAL,
        total_pnl REAL,
        trades INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_trade(symbol, entry, exit, quantity, date):
    pnl = (exit - entry) * quantity if exit else 0
    status = "Closed" if exit else "Open"

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO trades (symbol, entry, exit, quantity, pnl, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (symbol, entry, exit, quantity, pnl, status, date))
    conn.commit()
    conn.close()


def get_trades():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM trades", conn)
    conn.close()
    return df


def add_backtest(strategy, win_rate, total_pnl, trades):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO backtests (strategy, win_rate, total_pnl, trades)
        VALUES (?, ?, ?, ?)
    """, (strategy, win_rate, total_pnl, trades))
    conn.commit()
    conn.close()


def get_backtests():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM backtests", conn)
    conn.close()
    return df
