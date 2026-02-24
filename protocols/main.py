"""Main entry point for the EMS Protocols Practice Game."""

import tkinter as tk

from .controller import App


def main():
    """Run the EMS Protocols Practice Game."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
