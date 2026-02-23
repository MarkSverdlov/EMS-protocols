"""Main application controller."""

import tkinter as tk
from pathlib import Path

from .gameplay import GameplayController
from .models import Protocol, State
from .parser import load_protocols_from_directory
from .screens import GameScreen, ProtocolSelectScreen, ResultsScreen


class App:
    """Main application managing screens and gameplay."""

    def __init__(self, root: tk.Tk, data_dir: Path | None = None):
        """Initialize the application.

        Args:
            root: The tkinter root window
            data_dir: Directory containing protocol markdown files
        """
        self.root = root
        self.root.title("EMS Protocol Practice")
        self.root.geometry("700x600")
        self.root.configure(bg="#2c3e50")

        # Load protocols
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.protocols = load_protocols_from_directory(data_dir)
        self.current_protocol_name: str | None = None

        # Create gameplay controller
        self.gameplay = GameplayController(
            protocols=self.protocols,
            on_state_changed=self._on_state_changed,
            on_game_complete=self._on_game_complete,
            on_score_updated=self._on_score_updated,
        )

        # Create screens
        self.protocol_select = ProtocolSelectScreen(
            root=self.root,
            protocol_names=list(self.protocols.keys()),
            on_start=self._start_game,
        )

        self.game_screen = GameScreen(
            root=self.root,
            on_back=self._back_to_menu,
            on_answer=self._on_answer,
            on_continue=self._on_continue,
        )

        self.results_screen = ResultsScreen(
            root=self.root,
            on_play_again=self._play_again,
            on_main_menu=self._back_to_menu,
        )

        # Show initial screen
        self.protocol_select.show()

    def _start_game(self, protocol_name: str):
        """Start a game with the selected protocol."""
        self.current_protocol_name = protocol_name
        self.protocol_select.hide()
        self.game_screen.show()
        self.gameplay.start_game(protocol_name)

    def _back_to_menu(self):
        """Return to the protocol selection menu."""
        self.game_screen.hide()
        self.results_screen.hide()
        self.protocol_select.show()

    def _on_state_changed(self, state: State):
        """Handle state change from gameplay controller."""
        self.game_screen.display_state(state)

    def _on_answer(self, answer: str, _user_selected: bool):
        """Handle user answer."""
        is_correct = self.gameplay.handle_answer(answer)
        correct_answer = self.gameplay.get_current_correct_answer()
        self.game_screen.show_feedback(is_correct, correct_answer or "")

    def _on_continue(self):
        """Handle continue button press."""
        self.gameplay.advance_to_next_state()

    def _on_score_updated(self, correct: int, total: int):
        """Handle score update (could be used for live score display)."""
        pass

    def _on_game_complete(self, final_state: State | None, correct: int, total: int):
        """Handle game completion."""
        self.game_screen.hide()
        description = final_state.description if final_state else "Protocol complete!"
        self.results_screen.display_results(description, correct, total)
        self.results_screen.show()

    def _play_again(self):
        """Play the same protocol again."""
        self.results_screen.hide()
        self.game_screen.show()
        if self.current_protocol_name:
            self.gameplay.start_game(self.current_protocol_name)
