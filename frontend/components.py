import tkinter as tk

from frontend import styles

BUTTON_KINDS = {
    "primary": (styles.PRIMARY, styles.PRIMARY_DARK),
    "danger": (styles.DANGER, styles.DANGER_DARK),
    "success": (styles.SUCCESS, styles.SUCCESS_DARK),
    "dark": (styles.DARK, styles.SIDEBAR_HOVER),
}


class FlatButton(tk.Label):

    def __init__(self, parent, text, command, kind="primary", **options):
        normal, hover = BUTTON_KINDS[kind]
        super().__init__(parent, text=text, bg=normal, fg="white",
                         font=styles.FONT_BUTTON, cursor="hand2",
                         padx=14, pady=8, **options)
        self.command = command
        self.normal_colour = normal
        self.hover_colour = hover
        self.bind("<Enter>", lambda event: self.config(bg=self.hover_colour))
        self.bind("<Leave>", lambda event: self.config(bg=self.normal_colour))
        self.bind("<ButtonRelease-1>", self.on_click)

    def on_click(self, event):
        if 0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height():
            self.command()


class PageHeader(tk.Frame):

    def __init__(self, parent, title, subtitle):
        super().__init__(parent, bg=styles.BG)
        tk.Label(self, text=title, bg=styles.BG, fg=styles.DARK,
                 font=styles.FONT_TITLE).pack(anchor="w")
        tk.Label(self, text=subtitle, bg=styles.BG, fg=styles.MUTED,
                 font=styles.FONT_TEXT).pack(anchor="w")


class StatCard(tk.Frame):

    def __init__(self, parent, title, colour):
        super().__init__(parent, bg=styles.CARD_BG, highlightthickness=1,
                         highlightbackground=styles.BORDER)
        tk.Frame(self, bg=colour, height=5).pack(fill="x")
        self.value_label = tk.Label(self, text="0", bg=styles.CARD_BG, fg=colour,
                                    font=styles.FONT_BIG_NUMBER)
        self.value_label.pack(pady=(14, 0))
        tk.Label(self, text=title, bg=styles.CARD_BG, fg=styles.MUTED,
                 font=styles.FONT_BOLD).pack(pady=(0, 16))

    def set_value(self, value):
        self.value_label.config(text=str(value))


class Sidebar(tk.Frame):

    ITEMS = [
        ("dashboard", "Dashboard"),
        ("planner", "Route Planner"),
        ("roads", "Road Management"),
        ("history", "Route History"),
        ("logout", "Logout"),
    ]

    def __init__(self, parent, width, on_navigate):
        super().__init__(parent, bg=styles.DARK, width=width)
        self.pack_propagate(False)
        self.buttons = {}
        self.active = None

        tk.Label(self, text="Route\nOptimizer", bg=styles.DARK, fg="white",
                 font=(styles.FONT, 16, "bold"), justify="left").pack(
                     anchor="w", padx=20, pady=(24, 24))

        for name, text in self.ITEMS:
            button = tk.Label(self, text=text, bg=styles.DARK, fg="white",
                              font=styles.FONT_BUTTON, anchor="w", padx=20, pady=12,
                              cursor="hand2")
            button.pack(fill="x")
            button.bind("<Enter>", lambda event, n=name: self.on_hover(n, True))
            button.bind("<Leave>", lambda event, n=name: self.on_hover(n, False))
            button.bind("<Button-1>", lambda event, n=name: on_navigate(n))
            self.buttons[name] = button

        self.user_label = tk.Label(self, text="", bg=styles.DARK, fg=styles.LIGHT_MUTED,
                                   font=(styles.FONT, 9))
        self.user_label.pack(side="bottom", pady=16)

    def on_hover(self, name, inside):
        if name != self.active:
            self.buttons[name].config(bg=styles.SIDEBAR_HOVER if inside else styles.DARK)

    def set_active(self, name):
        self.active = name
        for key, button in self.buttons.items():
            button.config(bg=styles.PRIMARY if key == name else styles.DARK)

    def set_user(self, username):
        self.user_label.config(text=f"Signed in as {username}" if username else "")
