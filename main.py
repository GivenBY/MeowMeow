import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from api import MeowMeowAPI
from ui import HeaderBarWindow


def main():
    api_handler = MeowMeowAPI()
    win: HeaderBarWindow = HeaderBarWindow(api_handler)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
