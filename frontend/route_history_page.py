import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from backend import routes
from frontend import styles
from frontend.components import FlatButton, PageHeader


class RouteHistoryPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=styles.BG)
        self.app = app

        PageHeader(self, "Route History", "Every route you have calculated").pack(
            anchor="w", padx=24, pady=(20, 10))

        controls = tk.Frame(self, bg=styles.BG)
        controls.pack(fill="x", padx=24, pady=(0, 10))
        FlatButton(controls, "Refresh History", self.refresh_table).pack(side="left")
        FlatButton(controls, "Clear History", self.clear_history, kind="danger").pack(
            side="left", padx=(10, 0))
        self.count_label = tk.Label(controls, text="", bg=styles.BG, fg=styles.MUTED,
                                    font=styles.FONT_BOLD)
        self.count_label.pack(side="right")

        table_frame = tk.Frame(self, bg=styles.BG)
        table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        columns = ("id", "start", "end", "route", "distance", "time", "fuel", "date")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        headings = {"id": "#", "start": "From", "end": "To", "route": "Route",
                    "distance": "Distance", "time": "Time", "fuel": "Fuel Cost",
                    "date": "Date & Time"}
        widths = {"id": 40, "start": 100, "end": 100, "route": 270, "distance": 75,
                  "time": 80, "fuel": 75, "date": 135}
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column],
                              anchor="w" if column in ("route", "start", "end") else "center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

    def on_show(self):
        self.refresh_table()

    def refresh_table(self):
        user = self.app.current_user
        if user is None:
            return
        try:
            history = routes.get_history(user["id"])
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load history:\n{error}",
                                 parent=self)
            return

        self.table.delete(*self.table.get_children())
        for number, row in enumerate(history, start=1):
            self.table.insert("", "end", values=(
                number, row["start_city"], row["end_city"], row["route_path"],
                f"{row['distance_km']:.0f} km", row["travel_time"],
                f"Rs {row['fuel_cost']:.0f}", row["calculated_at"]))
        self.count_label.config(text=f"{len(history)} route(s) saved")

    def clear_history(self):
        if not messagebox.askyesno("Clear history",
                                   "Are you sure you want to delete all saved routes?\n"
                                   "This cannot be undone.", parent=self):
            return
        try:
            routes.clear_history(self.app.current_user["id"])
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not clear history:\n{error}",
                                 parent=self)
            return
        self.refresh_table()
        messagebox.showinfo("History cleared", "Your route history has been cleared.",
                            parent=self)
