import heapq
from datetime import datetime

from config import CITIES, ROADS, SPEED, MILEAGE, PETROL
from database import get_connection
from backend.road_management import get_blocked_roads

graph = {city: {} for city in CITIES}
for (a, b), km in ROADS.items():
    graph[a][b] = km
    graph[b][a] = km


def shortest_path(start, end, blocked=None):
    blocked = blocked or set()
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        km, city, path = heapq.heappop(queue)
        if city == end:
            return km, path
        if city in visited:
            continue
        visited.add(city)

        for neighbour, distance in graph[city].items():
            if frozenset((city, neighbour)) in blocked:
                continue
            if neighbour not in visited:
                heapq.heappush(queue, (km + distance, neighbour, path + [neighbour]))

    return None, []


def format_time(km):
    total_minutes = round(km / SPEED * 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours} h {minutes} min"


def calculate_route(start, end):
    if start not in CITIES or end not in CITIES:
        return {"found": False, "message": "Please choose both a starting city and a destination."}
    if start == end:
        return {"found": False, "message": "Starting city and destination must be different."}

    km, path = shortest_path(start, end, get_blocked_roads())
    if km is None:
        return {"found": False, "message": "No route found.\nToo many roads are blocked."}

    return {
        "found": True,
        "start": start,
        "end": end,
        "path": path,
        "distance_km": km,
        "time_text": format_time(km),
        "fuel_cost": km / MILEAGE * PETROL,
    }


def save_route(user_id, result):
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """INSERT INTO route_history
                   (user_id, start_city, end_city, route_path, distance_km,
                    travel_time, fuel_cost, calculated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, result["start"], result["end"], " -> ".join(result["path"]),
                 result["distance_km"], result["time_text"], result["fuel_cost"],
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    finally:
        conn.close()


def get_history(user_id):
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM route_history WHERE user_id = ? ORDER BY id DESC",
            (user_id,)).fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]


def clear_history(user_id):
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM route_history WHERE user_id = ?", (user_id,))
    finally:
        conn.close()
