import sqlite3

from database import get_connection


def get_all_roads():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT city_a, city_b, distance_km, is_blocked FROM road_status ORDER BY id").fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]


def get_blocked_roads():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT city_a, city_b FROM road_status WHERE is_blocked = 1").fetchall()
    finally:
        conn.close()
    return {frozenset((row["city_a"], row["city_b"])) for row in rows}


def count_roads():
    conn = get_connection()
    try:
        return conn.execute("SELECT COUNT(*) FROM road_status").fetchone()[0]
    finally:
        conn.close()


def count_blocked_roads():
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT COUNT(*) FROM road_status WHERE is_blocked = 1").fetchone()[0]
    finally:
        conn.close()


def _set_blocked(city_a, city_b, blocked):
    state = "BLOCKED" if blocked else "OPEN"
    try:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT is_blocked FROM road_status WHERE city_a = ? AND city_b = ?",
                (city_a, city_b)).fetchone()
            if row is None:
                return False, "That road does not exist."
            if row["is_blocked"] == int(blocked):
                return False, f"{city_a} - {city_b} is already {state}."
            with conn:
                conn.execute(
                    "UPDATE road_status SET is_blocked = ? WHERE city_a = ? AND city_b = ?",
                    (int(blocked), city_a, city_b))
        finally:
            conn.close()
    except sqlite3.Error as error:
        return False, f"Database error: {error}"

    verb = "blocked" if blocked else "unblocked"
    return True, f"Road {city_a} - {city_b} has been {verb}."


def block_road(city_a, city_b):
    return _set_blocked(city_a, city_b, True)


def unblock_road(city_a, city_b):
    return _set_blocked(city_a, city_b, False)
