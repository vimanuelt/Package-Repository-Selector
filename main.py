# main.py

from prs.ui import RepositorySelectorUI

def main():
    # Create an instance of the GUI window
    ui_window = RepositorySelectorUI()
    # Show the Gtk window and start the main loop
    ui_window.show()

if __name__ == "__main__":
    main()

