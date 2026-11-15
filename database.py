import hashlib
import secrets
import sqlite3

import config


def get_connection():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                               salt.encode("utf-8"), 100_000).hex()


def init_database():
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    username      TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    salt          TEXT NOT NULL
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS road_status (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_a      TEXT NOT NULL,
                    city_b      TEXT NOT NULL,
                    distance_km INTEGER NOT NULL,
                    is_blocked  INTEGER NOT NULL DEFAULT 0,
                    UNIQUE (city_a, city_b)
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS route_history (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id       INTEGER NOT NULL,
                    start_city    TEXT NOT NULL,
                    end_city      TEXT NOT NULL,
                    route_path    TEXT NOT NULL,
                    distance_km   REAL NOT NULL,
                    travel_time   TEXT NOT NULL,
                    fuel_cost     REAL NOT NULL,
                    calculated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )""")

            for (city_a, city_b), km in config.ROADS.items():
                conn.execute(
                    "INSERT OR IGNORE INTO road_status (city_a, city_b, distance_km) VALUES (?, ?, ?)",
                    (city_a, city_b, km))

            exists = conn.execute("SELECT 1 FROM users WHERE username = ?",
                                  (config.DEFAULT_USERNAME,)).fetchone()
            if not exists:
                salt = secrets.token_hex(8)
                conn.execute(
                    "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                    (config.DEFAULT_USERNAME, hash_password(config.DEFAULT_PASSWORD, salt), salt))
    finally:
        conn.close()
