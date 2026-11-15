from database import init_database
from frontend.app import App


def main():
    init_database()
    App().mainloop()


if __name__ == "__main__":
    main()
