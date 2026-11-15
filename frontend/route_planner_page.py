import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import config
from backend import road_management, routes
from frontend import styles
from frontend.components import FlatButton, PageHeader

PANEL_WIDTH = 256


class RoutePlannerPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=styles.BG)
        self.app = app

        PageHeader(self, "Route Planner",
                   "Choose two cities to find the shortest open route").pack(
                       anchor="w", padx=16, pady=(14, 8))

        body = tk.Frame(self, bg=styles.BG)
        body.pack(fill="both", expand=True, padx=16)

        panel = tk.Frame(body, bg=styles.CARD_BG, width=PANEL_WIDTH,
                         highlightthickness=1, highlightbackground=styles.BORDER)
        panel.pack(side="right", fill="y", padx=(12, 0))
        panel.pack_propagate(False)
        self.build_panel(panel)

        self.current_path = []
        self.canvas = tk.Canvas(body, width=config.MAP_WIDTH, height=config.MAP_HEIGHT,
                                bg=styles.MAP_BG, highlightthickness=1,
                                highlightbackground=styles.BORDER)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw_map(self.current_path))

        self.draw_map([])

    def build_panel(self, panel):
        inner = tk.Frame(panel, bg=styles.CARD_BG)
        inner.pack(fill="both", expand=True, padx=14, pady=14)

        cities = sorted(config.CITIES)
        tk.Label(inner, text="From", bg=styles.CARD_BG, font=styles.FONT_TEXT).pack(anchor="w")
        self.start_box = ttk.Combobox(inner, values=cities, state="readonly", width=26)
        self.start_box.pack(pady=(2, 8), anchor="w")

        tk.Label(inner, text="To", bg=styles.CARD_BG, font=styles.FONT_TEXT).pack(anchor="w")
        self.end_box = ttk.Combobox(inner, values=cities, state="readonly", width=26)
        self.end_box.pack(pady=(2, 10), anchor="w")

        FlatButton(inner, "Find Route", self.find_route).pack(fill="x")

        result = tk.Frame(inner, bg=styles.PANEL_BG)
        result.pack(fill="x", pady=(12, 0))
        self.route_label = tk.Label(result, text="Pick two cities and press Find Route.",
                                    bg=styles.PANEL_BG, font=styles.FONT_TEXT,
                                    justify="left", anchor="nw", wraplength=205)
        self.route_label.pack(fill="x", padx=10, pady=(10, 4))
        self.distance_label = self.add_result_row(result, "Distance")
        self.time_label = self.add_result_row(result, "Time")
        self.fuel_label = self.add_result_row(result, "Fuel cost")
        tk.Frame(result, bg=styles.PANEL_BG, height=6).pack()

        self.status_label = tk.Label(inner, text="", bg=styles.CARD_BG, fg=styles.SUCCESS,
                                     font=(styles.FONT, 9), wraplength=225, justify="left")
        self.status_label.pack(anchor="w", pady=(6, 0))

        self.build_legend(inner)

    def add_result_row(self, parent, caption):
        row = tk.Frame(parent, bg=styles.PANEL_BG)
        row.pack(fill="x", padx=10)
        tk.Label(row, text=caption, bg=styles.PANEL_BG, fg=styles.MUTED,
                 font=styles.FONT_TEXT).pack(side="left")
        value = tk.Label(row, text="-", bg=styles.PANEL_BG, fg=styles.DARK,
                         font=styles.FONT_BOLD)
        value.pack(side="right")
        return value

    def build_legend(self, parent):
        legend = tk.Canvas(parent, width=225, height=115, bg=styles.CARD_BG,
                           highlightthickness=0)
        legend.pack(side="bottom", anchor="w")
        items = [("Start city", styles.START), ("Destination", styles.END),
                 ("City on route", styles.STOP)]
        for index, (text, colour) in enumerate(items):
            y = 10 + index * 20
            legend.create_oval(4, y - 6, 16, y + 6, fill=colour, outline=styles.DARK)
            legend.create_text(26, y, text=text, anchor="w", font=styles.FONT_TEXT)
        legend.create_line(2, 70, 18, 70, fill=styles.ROUTE, width=5, capstyle="round")
        legend.create_text(26, 70, text="Selected route", anchor="w", font=styles.FONT_TEXT)
        legend.create_line(2, 90, 18, 90, fill=styles.BLOCK, width=3, dash=(4, 3))
        legend.create_text(26, 90, text="Blocked road", anchor="w", font=styles.FONT_TEXT)

    def on_show(self):
        start, end = self.start_box.get(), self.end_box.get()
        if start and end and start != end:
            self.find_route(save=False)
        else:
            self.draw_map([])

    def reset(self):
        self.start_box.set("")
        self.end_box.set("")
        self.show_message("Pick two cities and press Find Route.")
        self.draw_map([])

    def show_message(self, text):
        self.route_label.config(text=text)
        for label in (self.distance_label, self.time_label, self.fuel_label):
            label.config(text="-")
        self.status_label.config(text="")

    def find_route(self, save=True):
        start, end = self.start_box.get(), self.end_box.get()
        if not start or not end:
            messagebox.showwarning("Select cities", "Please choose both a starting city "
                                   "and a destination.", parent=self)
            return
        if start == end:
            messagebox.showwarning("Select cities", "Starting city and destination "
                                   "must be different.", parent=self)
            return

        try:
            result = routes.calculate_route(start, end)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not read road status:\n{error}",
                                 parent=self)
            return

        if not result["found"]:
            self.show_message(result["message"])
            self.draw_map([])
            return

        self.route_label.config(text="Route\n" + " -> ".join(result["path"]))
        self.distance_label.config(text=f"{result['distance_km']} km")
        self.time_label.config(text=result["time_text"])
        self.fuel_label.config(text=f"Rs {result['fuel_cost']:.0f}")
        self.status_label.config(text="")
        self.draw_map(result["path"])

        if save:
            try:
                routes.save_route(self.app.current_user["id"], result)
                self.status_label.config(text="Route saved to history.", fg=styles.SUCCESS)
            except sqlite3.Error as error:
                messagebox.showerror("Database error", f"Could not save route:\n{error}",
                                     parent=self)

    def draw_label(self, x, y, text, font, colour=styles.DARK):
        item = self.canvas.create_text(x, y, text=text, font=font, fill=colour)
        x1, y1, x2, y2 = self.canvas.bbox(item)
        box = self.canvas.create_rectangle(x1 - 2, y1, x2 + 2, y2, fill=styles.MAP_BG, outline="")
        self.canvas.tag_lower(box, item)

    def draw_map(self, path):
        self.current_path = path
        try:
            blocked = road_management.get_blocked_roads()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not read road status:\n{error}",
                                 parent=self)
            blocked = set()

        canvas = self.canvas
        canvas.delete("all")

        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = config.MAP_WIDTH, config.MAP_HEIGHT
        scale = min(width / config.MAP_WIDTH, height / config.MAP_HEIGHT)
        offset_x = (width - config.MAP_WIDTH * scale) / 2
        offset_y = (height - config.MAP_HEIGHT * scale) / 2
        size = min(max(scale, 1), 1.5)
        cities = {name: (x * scale + offset_x, y * scale + offset_y)
                  for name, (x, y) in config.CITIES.items()}

        route_roads = {frozenset(pair) for pair in zip(path, path[1:])}

        for (a, b) in config.ROADS:
            if frozenset((a, b)) in blocked:
                canvas.create_line(*cities[a], *cities[b], fill=styles.BLOCK, width=3, dash=(6, 4))
            elif frozenset((a, b)) not in route_roads:
                canvas.create_line(*cities[a], *cities[b], fill=styles.ROAD, width=2)
        for (a, b) in config.ROADS:
            if frozenset((a, b)) in route_roads:
                canvas.create_line(*cities[a], *cities[b], fill=styles.ROUTE, width=6,
                                   capstyle="round")

        for (a, b), km in config.ROADS.items():
            x = (cities[a][0] + cities[b][0]) / 2
            y = (cities[a][1] + cities[b][1]) / 2
            on_route = frozenset((a, b)) in route_roads
            if frozenset((a, b)) in blocked:
                self.draw_label(x, y, "BLOCKED", (styles.FONT, 8, "bold"), styles.BLOCK)
            else:
                self.draw_label(x, y, f"{km} km",
                                (styles.FONT, 8, "bold" if on_route else "normal"),
                                styles.ROUTE if on_route else "#475569")

        radius = 11 * size
        for name, (x, y) in cities.items():
            colour = "white"
            if path and name == path[0]:
                colour = styles.START
            elif path and name == path[-1]:
                colour = styles.END
            elif name in path:
                colour = styles.STOP
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=colour,
                               outline=styles.DARK, width=2)
            self.draw_label(x, y + 24 * size, name, (styles.FONT, 9, "bold"))
