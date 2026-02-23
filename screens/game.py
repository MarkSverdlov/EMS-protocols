"""Main game screen for protocol practice."""

import tkinter as tk
from collections.abc import Callable

from ..base import BaseScreen
from ..models import State, StateType


class GameScreen(BaseScreen):
    """Screen for playing the protocol practice game."""

    def __init__(
        self,
        root: tk.Tk,
        on_back: Callable[[], None],
        on_answer: Callable[[str, bool], None],
        on_continue: Callable[[], None],
    ):
        self.on_back = on_back
        self.on_answer_callback = on_answer
        self.on_continue_callback = on_continue
        self.answer_buttons: list[tk.Button] = []
        self.current_options: list[str] = []
        self.answered = False
        super().__init__(root)

    def _setup_ui(self):
        """Set up the game UI."""
        # Header with back button
        self._create_header("Protocol Practice", self.on_back)

        # Main content area
        self.content_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Scenario card
        self.card_frame = tk.Frame(
            self.content_frame,
            bg=self.CARD_COLOR,
            padx=30,
            pady=25,
        )
        self.card_frame.pack(fill=tk.X, pady=(0, 20))

        self.scenario_label = tk.Label(
            self.card_frame,
            text="",
            font=("Helvetica", 16),
            bg=self.CARD_COLOR,
            fg=self.DARK_TEXT,
            wraplength=500,
            justify=tk.LEFT,
        )
        self.scenario_label.pack()

        # Answer buttons frame
        self.buttons_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        self.buttons_frame.pack(fill=tk.X, pady=10)

        # Create 4 answer buttons
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Helvetica", 13),
                bg=self.CARD_COLOR,
                fg=self.DARK_TEXT,
                activebackground="#bdc3c7",
                activeforeground=self.DARK_TEXT,
                wraplength=450,
                justify=tk.LEFT,
                anchor="w",
                padx=15,
                pady=10,
                cursor="hand2",
                relief=tk.FLAT,
            )
            btn.pack(fill=tk.X, pady=5)
            btn.config(command=lambda idx=i: self._on_answer_clicked(idx))
            self.answer_buttons.append(btn)

        # Feedback frame (initially hidden)
        self.feedback_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)

        self.feedback_label = tk.Label(
            self.feedback_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            fg="white",
            padx=20,
            pady=15,
        )
        self.feedback_label.pack(fill=tk.X)

        # Continue button (shown after answering or for INTRO states)
        self.continue_btn = tk.Button(
            self.content_frame,
            text="Continue",
            command=self._on_continue_clicked,
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=25,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
        )

        # Keyboard bindings
        self.frame.bind("1", lambda e: self._on_key_answer(0))
        self.frame.bind("2", lambda e: self._on_key_answer(1))
        self.frame.bind("3", lambda e: self._on_key_answer(2))
        self.frame.bind("4", lambda e: self._on_key_answer(3))
        self.frame.bind("<Return>", lambda e: self._on_key_continue())
        self.frame.bind("<space>", lambda e: self._on_key_continue())

    def display_state(self, state: State):
        """Display a state on the screen."""
        self.answered = False
        self.scenario_label.config(text=state.description)

        # Hide feedback
        self.feedback_frame.pack_forget()
        self.continue_btn.pack_forget()

        if state.state_type == StateType.QUESTION:
            # Show answer buttons with shuffled options
            self.current_options = state.get_shuffled_options()
            self._show_answer_buttons()
            for i, option in enumerate(self.current_options):
                self.answer_buttons[i].config(
                    text=f"{i + 1}. {option}",
                    state=tk.NORMAL,
                    bg=self.CARD_COLOR,
                    fg=self.DARK_TEXT,
                )
        elif state.state_type == StateType.INTRO:
            # Hide answer buttons, show Next button
            self._hide_answer_buttons()
            self.continue_btn.config(text="Next")
            self.continue_btn.pack(pady=20)
        else:
            # FINAL state - shouldn't normally display here
            self._hide_answer_buttons()

    def _show_answer_buttons(self):
        """Show all answer buttons."""
        self.buttons_frame.pack(fill=tk.X, pady=10)

    def _hide_answer_buttons(self):
        """Hide all answer buttons."""
        self.buttons_frame.pack_forget()

    def _on_answer_clicked(self, index: int):
        """Handle answer button click."""
        if self.answered or index >= len(self.current_options):
            return

        self.answered = True
        selected = self.current_options[index]

        # Disable all buttons
        for btn in self.answer_buttons:
            btn.config(state=tk.DISABLED)

        # The callback will tell us if it was correct and show feedback
        self.on_answer_callback(selected, True)  # True indicates user made selection

    def show_feedback(self, is_correct: bool, correct_answer: str):
        """Show feedback after answering."""
        if is_correct:
            self.feedback_label.config(
                text="Correct!",
                bg=self.SUCCESS_COLOR,
            )
        else:
            self.feedback_label.config(
                text=f"Incorrect. The correct answer was:\n{correct_answer}",
                bg=self.ERROR_COLOR,
            )

        # Highlight correct/wrong answers
        for i, option in enumerate(self.current_options):
            if option == correct_answer:
                self.answer_buttons[i].config(bg=self.SUCCESS_COLOR, fg="white")
            elif self.answer_buttons[i]["state"] == tk.DISABLED and not is_correct:
                # This was the selected wrong answer
                if self.answer_buttons[i]["bg"] != self.SUCCESS_COLOR:
                    self.answer_buttons[i].config(bg=self.ERROR_COLOR, fg="white")

        self.feedback_frame.pack(fill=tk.X, pady=15)
        self.continue_btn.config(text="Continue")
        self.continue_btn.pack(pady=10)

    def _on_continue_clicked(self):
        """Handle continue button click."""
        self.on_continue_callback()

    def _on_key_answer(self, index: int):
        """Handle number key press for answer selection."""
        if (
            not self.answered
            and self.buttons_frame.winfo_ismapped()
            and index < len(self.current_options)
        ):
            self._on_answer_clicked(index)

    def _on_key_continue(self):
        """Handle Enter/Space key for continue."""
        if self.continue_btn.winfo_ismapped():
            self._on_continue_clicked()

    def show(self):
        """Show the screen and enable keyboard bindings."""
        super().show()
        self.frame.focus_set()
