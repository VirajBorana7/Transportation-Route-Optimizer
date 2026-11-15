import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "transport.db")

APP_NAME = "Transportation and Route Optimization System"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
SIDEBAR_WIDTH = 200

MAP_WIDTH = 696
MAP_HEIGHT = 570

CITIES = {
    "Hyderabad": (280, 60),   "Vijayawada": (520, 100),
    "Bengaluru": (250, 260),  "Mysuru": (130, 340),
    "Chennai": (560, 270),    "Puducherry": (630, 380),
    "Coimbatore": (120, 470), "Tiruchirappalli": (380, 400),
    "Madurai": (330, 520),
}

ROADS = {
    ("Chennai", "Bengaluru"): 345,       ("Chennai", "Puducherry"): 150,
    ("Chennai", "Vijayawada"): 450,      ("Chennai", "Tiruchirappalli"): 330,
    ("Chennai", "Madurai"): 460,         ("Bengaluru", "Hyderabad"): 570,
    ("Bengaluru", "Mysuru"): 145,        ("Bengaluru", "Coimbatore"): 365,
    ("Hyderabad", "Vijayawada"): 275,    ("Mysuru", "Coimbatore"): 195,
    ("Coimbatore", "Tiruchirappalli"): 215, ("Coimbatore", "Madurai"): 215,
    ("Tiruchirappalli", "Madurai"): 135, ("Puducherry", "Tiruchirappalli"): 200,
}

SPEED = 60
MILEAGE = 12
PETROL = 100

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "1234"
