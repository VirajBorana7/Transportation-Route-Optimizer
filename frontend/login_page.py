import tkinter as tk
from tkinter import ttk

import config
from backend import auth
from frontend import styles
from frontend.components import FlatButton


class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=styles.BG)
        self.app = app

        card = tk.Frame(self, bg=styles.CARD_BG, width=430, height=500,
                        highlightthickness=1, highlightbackground=styles.BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        tk.Label(card, text=config.APP_NAME, bg=styles.DARK, fg="white",
                 font=(styles.FONT, 15, "bold"), wraplength=380, pady=22).pack(fill="x")
        tk.Label(card, text="Please log in to continue", bg=styles.CARD_BG,
                 fg=styles.MUTED, font=styles.FONT_TEXT).pack(pady=(20, 12))

        tk.Label(card, text="Username", bg=styles.CARD_BG, font=styles.FONT_TEXT).pack(
            anchor="w", padx=45)
        self.username_entry = ttk.Entry(card, width=36)
        self.username_entry.pack(pady=(2, 12))

        tk.Label(card, text="Password", bg=styles.CARD_BG, font=styles.FONT_TEXT).pack(
            anchor="w", padx=45)
        self.password_entry = ttk.Entry(card, width=36, show="*")
        self.password_entry.pack(pady=(2, 6))

        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text="Show password", variable=self.show_password,
                        command=self.toggle_password).pack(anchor="w", padx=45)

        self.error_label = tk.Label(card, text="", bg=styles.CARD_BG, fg=styles.DANGER,
                                    font=styles.FONT_BOLD, wraplength=340)
        self.error_label.pack(pady=(10, 6))

        FlatButton(card, "Login", self.login).pack(fill="x", padx=45)
        tk.Label(card, text="Demo login: admin / 1234", bg=styles.CARD_BG,
                 fg=styles.LIGHT_MUTED, font=(styles.FONT, 9)).pack(pady=(16, 0))

        self.username_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password.get() else "*")

    def login(self):
        user, error = auth.login(self.username_entry.get(), self.password_entry.get())
        if user is None:
            self.error_label.config(text=error)
            self.password_entry.delete(0, "end")
            return
        self.app.login_success(user)

    def reset(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.show_password.set(False)
        self.toggle_password()
        self.error_label.config(text="")
        self.username_entry.focus_set()
