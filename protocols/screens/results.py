"""Results screen shown at the end of a protocol practice session."""

import tkinter as tk
from collections.abc import Callable

from ..base import BaseScreen


class ResultsScreen(BaseScreen):
    """Screen displaying final results after completing a protocol."""

    def __init__(
        self,
        root: tk.Tk,
        on_play_again: Callable[[], None],
        on_main_menu: Callable[[], None],
    ):
        self.on_play_again = on_play_again
        self.on_main_menu = on_main_menu
        super().__init__(root)

    def _setup_ui(self):
        """Set up the results UI."""
        # Title
        self.title_label = tk.Label(
            self.frame,
            text="Protocol Complete!",
            font=("Helvetica", 28, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.title_label.pack(pady=(60, 20))

        # Final state description
        self.description_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 16),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            wraplength=500,
        )
        self.description_label.pack(pady=(0, 30))

        # Score card
        self.score_frame = tk.Frame(self.frame, bg=self.CARD_COLOR, padx=40, pady=30)
        self.score_frame.pack(pady=20)

        self.score_label = tk.Label(
            self.score_frame,
            text="0 / 0 (0%)",
            font=("Helvetica", 32, "bold"),
            bg=self.CARD_COLOR,
            fg=self.DARK_TEXT,
        )
        self.score_label.pack()

        self.message_label = tk.Label(
            self.score_frame,
            text="",
            font=("Helvetica", 14),
            bg=self.CARD_COLOR,
            fg=self.DARK_TEXT,
        )
        self.message_label.pack(pady=(10, 0))

        # Buttons frame
        buttons_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        buttons_frame.pack(pady=40)

        play_again_btn = tk.Button(
            buttons_frame,
            text="Play Again",
            command=self.on_play_again,
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            padx=25,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
        )
        play_again_btn.pack(side=tk.LEFT, padx=10)

        menu_btn = tk.Button(
            buttons_frame,
            text="Main Menu",
            command=self.on_main_menu,
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=25,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
        )
        menu_btn.pack(side=tk.LEFT, padx=10)

        # Keyboard bindings
        self.frame.bind("<Return>", lambda e: self.on_play_again())
        self.frame.bind("<Escape>", lambda e: self.on_main_menu())

    def display_results(
        self, final_description: str, correct: int, total: int
    ):
        """Display the results of the practice session."""
        self.description_label.config(text=final_description)

        if total > 0:
            percentage = (correct / total) * 100
            self.score_label.config(text=f"{correct} / {total} ({percentage:.0f}%)")

            if percentage >= 90:
                message = "Excellent! Great job!"
                self.message_label.config(fg="#27ae60")
            elif percentage >= 70:
                message = "Good work! Keep practicing!"
                self.message_label.config(fg="#f39c12")
            else:
                message = "Keep practicing to improve!"
                self.message_label.config(fg="#e74c3c")

            self.message_label.config(text=message)
        else:
            self.score_label.config(text="No questions")
            self.message_label.config(text="This protocol had no questions.")

    def show(self):
        """Show the screen and enable keyboard focus."""
        super().show()
        self.frame.focus_set()
