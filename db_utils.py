import sqlite3
from flask import current_app, g

DATABASE = "data.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    c = db.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS english_study (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        study_date TEXT NOT NULL,
        content TEXT NOT NULL
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS real_estate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        community TEXT NOT NULL,
        city TEXT NOT NULL,
        area REAL NOT NULL,
        floor INTEGER NOT NULL,
        total_price REAL
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )"""
    )
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin")
        )
    c.execute(
        """CREATE TABLE IF NOT EXISTS blog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT NOT NULL
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS blog_comment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS blog_like (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_id INTEGER NOT NULL,
        username TEXT NOT NULL
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS english_comment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS english_like (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER NOT NULL,
        username TEXT NOT NULL
    )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS stock_watch (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        market TEXT NOT NULL
    )"""
    )
    db.commit()
