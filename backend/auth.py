import hmac
import sqlite3

from database import get_connection, hash_password


def login(username, password):
    username = username.strip()
    if not username or not password:
        return None, "Please enter both username and password."

    try:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT id, username, password_hash, salt FROM users WHERE username = ?",
                (username,)).fetchone()
        finally:
            conn.close()
    except sqlite3.Error as error:
        return None, f"Database error: {error}"

    if row is None or not hmac.compare_digest(
            row["password_hash"], hash_password(password, row["salt"])):
        return None, "Incorrect username or password."

    return {"id": row["id"], "username": row["username"]}, ""
