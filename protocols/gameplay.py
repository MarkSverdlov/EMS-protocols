"""Gameplay controller for the protocol practice game."""

from collections.abc import Callable

from .models import Protocol, State, StateType


class GameplayController:
    """Event-driven controller for gameplay logic.

    Manages game state and emits events via callbacks.
    Has no knowledge of UI implementation.
    """

    def __init__(
        self,
        protocols: dict[str, Protocol],
        on_state_changed: Callable[[State], None],
        on_game_complete: Callable[[State, int, int], None],
        on_score_updated: Callable[[int, int], None],
    ):
        """Initialize the gameplay controller.

        Args:
            protocols: Dictionary mapping protocol names to Protocol objects
            on_state_changed: Called when state changes (State)
            on_game_complete: Called when game ends (final_state, correct, total)
            on_score_updated: Called when score changes (correct, total)
        """
        self.protocols = protocols
        self.on_state_changed = on_state_changed
        self.on_game_complete = on_game_complete
        self.on_score_updated = on_score_updated

        self.current_protocol: Protocol | None = None
        self.current_state: State | None = None
        self.correct_answers = 0
        self.total_questions = 0

    def start_game(self, protocol_name: str):
        """Start a new game with the specified protocol."""
        if protocol_name not in self.protocols:
            raise ValueError(f"Unknown protocol: {protocol_name}")

        self.current_protocol = self.protocols[protocol_name]
        self.current_state = self.current_protocol.get_initial_state()
        self.correct_answers = 0
        self.total_questions = 0

        if self.current_state:
            self.on_state_changed(self.current_state)

    def handle_answer(self, answer: str) -> bool:
        """Handle a user's answer.

        Args:
            answer: The answer text selected by the user

        Returns:
            True if the answer was correct, False otherwise
        """
        if self.current_state is None:
            return False

        is_correct = answer == self.current_state.correct_answer
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1

        self.on_score_updated(self.correct_answers, self.total_questions)
        return is_correct

    def advance_to_next_state(self):
        """Advance to the next state in the protocol."""
        if self.current_state is None or self.current_protocol is None:
            return

        next_id = self.current_state.get_random_next_state_id()

        if next_id is None:
            # No next state - this is a final state
            self.on_game_complete(
                self.current_state, self.correct_answers, self.total_questions
            )
            return

        if isinstance(next_id, str):
            # Switch to a different protocol
            if next_id in self.protocols:
                self.current_protocol = self.protocols[next_id]
                self.current_state = self.current_protocol.get_initial_state()
            else:
                # Protocol not found, treat as game complete
                self.on_game_complete(
                    self.current_state, self.correct_answers, self.total_questions
                )
                return
        else:
            # Stay in current protocol
            self.current_state = self.current_protocol.get_state(next_id)

        if self.current_state:
            # Check if new state is FINAL
            if self.current_state.state_type == StateType.FINAL:
                self.on_game_complete(
                    self.current_state, self.correct_answers, self.total_questions
                )
            else:
                self.on_state_changed(self.current_state)
        else:
            # State not found, end game
            self.on_game_complete(
                self.current_state, self.correct_answers, self.total_questions
            )

    def get_current_correct_answer(self) -> str | None:
        """Get the correct answer for the current state."""
        if self.current_state:
            return self.current_state.correct_answer
        return None
