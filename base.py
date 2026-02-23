"""Base screen class for the protocols application."""

import tkinter as tk
from abc import ABC, abstractmethod
from collections.abc import Callable


class BaseScreen(ABC):
    """Abstract base class for all screens."""

    # Color scheme matching the medical flashcards app
    BG_COLOR = "#2c3e50"
    CARD_COLOR = "#ecf0f1"
    SUCCESS_COLOR = "#27ae60"
    ERROR_COLOR = "#e74c3c"
    TEXT_COLOR = "white"
    DARK_TEXT = "#2c3e50"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.frame = tk.Frame(root, bg=self.BG_COLOR)
        self._setup_ui()

    @abstractmethod
    def _setup_ui(self):
        """Set up the user interface. Subclasses must implement."""
        pass

    def show(self):
        """Show the screen."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        """Hide the screen."""
        self.frame.pack_forget()

    def _create_header(
        self, title_text: str, on_back: Callable[[], None] | None = None
    ) -> tk.Frame:
        """Create a header with optional back button."""
        header = tk.Frame(self.frame, bg=self.BG_COLOR)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        if on_back:
            back_btn = tk.Button(
                header,
                text="\u2190 Menu",
                command=on_back,
                font=("Helvetica", 12),
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR,
                activebackground="#34495e",
                activeforeground=self.TEXT_COLOR,
                relief=tk.FLAT,
                cursor="hand2",
            )
            back_btn.pack(side=tk.LEFT)

        title = tk.Label(
            header,
            text=title_text,
            font=("Helvetica", 18, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        title.pack(side=tk.LEFT, expand=True)

        # Spacer for centering when back button exists
        if on_back:
            spacer = tk.Frame(header, width=60, bg=self.BG_COLOR)
            spacer.pack(side=tk.RIGHT)

        return header
