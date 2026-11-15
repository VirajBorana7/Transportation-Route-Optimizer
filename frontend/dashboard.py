import sqlite3
import tkinter as tk
from tkinter import messagebox

import config
from backend import road_management
from frontend import styles
from frontend.components import FlatButton, PageHeader, StatCard

ABOUT_TEXT = (
    "This application helps you plan travel between nine cities in South India. "
    "It uses Dijkstra's shortest-path algorithm to find the shortest route, then "
    "estimates the travel time (average speed 60 km/h) and the fuel cost "
    "(12 km/litre, Rs 100/litre). Roads can be blocked or unblocked, and the "
    "route planner automatically avoids blocked roads. Every route you calculate "
    "is saved in the route history."
)


class DashboardPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=styles.BG)
        self.app = app

        PageHeader(self, "Dashboard", config.APP_NAME).pack(anchor="w", padx=24, pady=(20, 8))

        self.welcome_label = tk.Label(self, text="", bg=styles.BG, fg=styles.PRIMARY,
                                      font=styles.FONT_HEADING)
        self.welcome_label.pack(anchor="w", padx=24, pady=(0, 14))

        cards = tk.Frame(self, bg=styles.BG)
        cards.pack(fill="x", padx=24)
        self.city_card = StatCard(cards, "Total Cities", styles.PRIMARY)
        self.road_card = StatCard(cards, "Total Roads", styles.SUCCESS)
        self.blocked_card = StatCard(cards, "Blocked Roads", styles.DANGER)
        for column, card in enumerate((self.city_card, self.road_card, self.blocked_card)):
            card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
            cards.grid_columnconfigure(column, weight=1, uniform="cards")

        tk.Label(self, text="Quick Access", bg=styles.BG, fg=styles.DARK,
                 font=styles.FONT_HEADING).pack(anchor="w", padx=24, pady=(24, 8))
        buttons = tk.Frame(self, bg=styles.BG)
        buttons.pack(anchor="w", padx=24)
        quick_links = [("Route Planner", "planner", "primary"),
                       ("Road Management", "roads", "success"),
                       ("Route History", "history", "dark")]
        for column, (text, page, kind) in enumerate(quick_links):
            FlatButton(buttons, text, lambda p=page: app.show_page(p), kind=kind,
                       width=18).grid(row=0, column=column, padx=(0, 10))

        about = tk.Frame(self, bg=styles.CARD_BG, highlightthickness=1,
                         highlightbackground=styles.BORDER)
        about.pack(fill="x", padx=24, pady=(24, 0))
        tk.Label(about, text="About this application", bg=styles.CARD_BG,
                 fg=styles.DARK, font=styles.FONT_HEADING).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Label(about, text=ABOUT_TEXT, bg=styles.CARD_BG, fg=styles.MUTED,
                 font=styles.FONT_TEXT, justify="left", wraplength=900).pack(
                     anchor="w", padx=16, pady=(0, 14))

    def on_show(self):
        user = self.app.current_user
        self.welcome_label.config(text=f"Welcome, {user['username']}!" if user else "")
        self.city_card.set_value(len(config.CITIES))
        try:
            self.road_card.set_value(road_management.count_roads())
            self.blocked_card.set_value(road_management.count_blocked_roads())
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load statistics:\n{error}")
