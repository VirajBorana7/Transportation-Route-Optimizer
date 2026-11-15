# Transportation and Route Optimization System

A Python + Tkinter desktop application (SQLite, heapq Dijkstra). No pip packages needed.

## Run
    python main.py

Default login: **admin / 1234**

Press F11 to toggle full screen (Esc exits); the maximize button also works.

The database file `transport.db` is created automatically on first run.
To reset everything (history and blocked roads), close the app and delete `transport.db`.

## Files
| File | Purpose |
|------|---------|
| main.py | Entry point: creates the database, starts the window |
| config.py | Cities, roads, speed / mileage / petrol price, window sizes |
| database.py | SQLite connection, table creation, default roads and demo user |
| backend/auth.py | Login check (salted PBKDF2-SHA256 password hashes via hashlib) |
| backend/routes.py | Dijkstra (heapq), distance / time / fuel, route history in SQLite |
| backend/road_management.py | Block / unblock roads, road counts (stored in SQLite) |
| frontend/app.py | The single Tk window; switches between login and pages |
| frontend/styles.py | Colours, fonts, ttk styling |
| frontend/components.py | FlatButton, PageHeader, StatCard, Sidebar |
| frontend/login_page.py | Page 1 - Login |
| frontend/dashboard.py | Page 2 - Dashboard |
| frontend/route_planner_page.py | Page 3 - Route Planner with the map |
| frontend/road_management_page.py | Page 4 - Road Management |
| frontend/route_history_page.py | Page 5 - Route History |

## Database tables
- `users` (id PK, username UNIQUE, password_hash, salt)
- `road_status` (id PK, city_a, city_b, distance_km, is_blocked)
- `route_history` (id PK, user_id FK -> users.id, start_city, end_city, route_path, distance_km, travel_time, fuel_cost, calculated_at)

## Assumptions (unchanged from the original project)
Average speed 60 km/h, mileage 12 km/litre, petrol Rs 100/litre.
