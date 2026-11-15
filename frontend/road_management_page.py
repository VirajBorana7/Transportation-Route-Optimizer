import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from backend import road_management
from frontend import styles
from frontend.components import FlatButton, PageHeader


class RoadManagementPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=styles.BG)
        self.app = app

        PageHeader(self, "Road Management",
                   "Select a road, then block or unblock it").pack(
                       anchor="w", padx=24, pady=(20, 10))

        table_frame = tk.Frame(self, bg=styles.BG)
        table_frame.pack(fill="both", expand=True, padx=24)
        columns = ("city_a", "city_b", "distance", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings",
                                  selectmode="browse", height=14)
        headings = {"city_a": "City A", "city_b": "City B",
                    "distance": "Distance (km)", "status": "Status"}
        widths = {"city_a": 220, "city_b": 220, "distance": 150, "status": 150}
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column], anchor="center")
        self.table.tag_configure("blocked", foreground=styles.DANGER)
        self.table.tag_configure("open", foreground=styles.SUCCESS)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        controls = tk.Frame(self, bg=styles.BG)
        controls.pack(fill="x", padx=24, pady=(14, 0))
        FlatButton(controls, "Block Road", self.block_selected, kind="danger").pack(side="left")
        FlatButton(controls, "Unblock Road", self.unblock_selected, kind="success").pack(
            side="left", padx=(10, 0))
        self.summary_label = tk.Label(controls, text="", bg=styles.BG, fg=styles.MUTED,
                                      font=styles.FONT_BOLD)
        self.summary_label.pack(side="right")

        self.message_label = tk.Label(self, text="", bg=styles.BG, font=styles.FONT_BOLD,
                                      anchor="w")
        self.message_label.pack(fill="x", padx=24, pady=(10, 16))

    def on_show(self):
        self.message_label.config(text="")
        self.refresh_table()

    def refresh_table(self, select=None):
        try:
            roads = road_management.get_all_roads()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load roads:\n{error}", parent=self)
            return

        self.table.delete(*self.table.get_children())
        blocked_count = 0
        for road in roads:
            is_blocked = bool(road["is_blocked"])
            blocked_count += is_blocked
            item_id = f"{road['city_a']}|{road['city_b']}"
            self.table.insert("", "end", iid=item_id,
                              values=(road["city_a"], road["city_b"], road["distance_km"],
                                      "BLOCKED" if is_blocked else "OPEN"),
                              tags=("blocked" if is_blocked else "open",))
        self.summary_label.config(
            text=f"{len(roads) - blocked_count} open  |  {blocked_count} blocked")
        if select and self.table.exists(select):
            self.table.selection_set(select)

    def selected_road(self):
        selection = self.table.selection()
        if not selection:
            return None
        city_a, city_b = selection[0].split("|")
        return city_a, city_b, selection[0]

    def show_message(self, text, success):
        self.message_label.config(text=text, fg=styles.SUCCESS if success else styles.DANGER)

    def change_status(self, action):
        road = self.selected_road()
        if road is None:
            self.show_message("Please select a road from the table first.", False)
            return
        city_a, city_b, item_id = road
        success, message = action(city_a, city_b)
        self.show_message(message, success)
        self.refresh_table(select=item_id)

    def block_selected(self):
        self.change_status(road_management.block_road)

    def unblock_selected(self):
        self.change_status(road_management.unblock_road)
