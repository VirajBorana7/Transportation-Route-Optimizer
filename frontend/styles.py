from tkinter import ttk

BG = "#e2e8f0"
CARD_BG = "#ffffff"
MAP_BG = "#f8fafc"
DARK = "#0f172a"
SIDEBAR_HOVER = "#1e293b"
PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
DANGER = "#dc2626"
DANGER_DARK = "#b91c1c"
SUCCESS = "#16a34a"
SUCCESS_DARK = "#15803d"
MUTED = "#475569"
LIGHT_MUTED = "#94a3b8"
BORDER = "#cbd5e1"
PANEL_BG = "#f1f5f9"

ROAD = "#94a3b8"
ROUTE = "#2563eb"
START = "#4ade80"
END = "#f87171"
STOP = "#fde68a"
BLOCK = "#dc2626"

FONT = "Segoe UI"
FONT_TITLE = (FONT, 20, "bold")
FONT_HEADING = (FONT, 13, "bold")
FONT_TEXT = (FONT, 10)
FONT_BOLD = (FONT, 10, "bold")
FONT_BUTTON = (FONT, 10, "bold")
FONT_BIG_NUMBER = (FONT, 28, "bold")


def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("Treeview", font=FONT_TEXT, rowheight=28, background="white",
                    fieldbackground="white", bordercolor=BORDER, borderwidth=1)
    style.configure("Treeview.Heading", font=FONT_BOLD, background=DARK,
                    foreground="white", padding=6, relief="flat")
    style.map("Treeview.Heading", background=[("active", SIDEBAR_HOVER)])
    style.map("Treeview", background=[("selected", PRIMARY)],
              foreground=[("selected", "white")])

    style.configure("TCombobox", padding=5, font=FONT_TEXT)
    style.configure("TEntry", padding=6)
    style.configure("TCheckbutton", background=CARD_BG, font=(FONT, 9))
