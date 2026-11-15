import tkinter as tk

import config
from frontend import styles
from frontend.components import Sidebar
from frontend.login_page import LoginPage
from frontend.dashboard import DashboardPage
from frontend.route_planner_page import RoutePlannerPage
from frontend.road_management_page import RoadManagementPage
from frontend.route_history_page import RouteHistoryPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(config.APP_NAME)
        self.configure(bg=styles.BG)
        self.resizable(True, True)
        self.minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.center_window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        styles.apply_styles(self)

        self.current_user = None

        self.login_page = LoginPage(self, self)

        self.shell = tk.Frame(self, bg=styles.BG)
        self.sidebar = Sidebar(self.shell, config.SIDEBAR_WIDTH, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.shell, bg=styles.BG)
        self.content.pack(side="left", fill="both", expand=True)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {
            "dashboard": DashboardPage(self.content, self),
            "planner": RoutePlannerPage(self.content, self),
            "roads": RoadManagementPage(self.content, self),
            "history": RouteHistoryPage(self.content, self),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        self.show_login()

    def center_window(self, width, height):
        x = (self.winfo_screenwidth() - width) // 2
        y = max((self.winfo_screenheight() - height) // 2 - 20, 0)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    def show_login(self):
        self.shell.pack_forget()
        self.login_page.reset()
        self.login_page.pack(fill="both", expand=True)

    def login_success(self, user):
        self.current_user = user
        self.login_page.pack_forget()
        self.shell.pack(fill="both", expand=True)
        self.sidebar.set_user(user["username"])
        self.show_page("dashboard")

    def logout(self):
        self.current_user = None
        self.sidebar.set_user("")
        self.pages["planner"].reset()
        self.show_login()

    def show_page(self, name):
        if name == "logout":
            self.logout()
            return
        page = self.pages[name]
        page.tkraise()
        self.sidebar.set_active(name)
        page.on_show()
