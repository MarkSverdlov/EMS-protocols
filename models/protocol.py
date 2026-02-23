from dataclasses import dataclass, field

from .state import State


@dataclass
class Protocol:
    """A protocol consisting of states forming a state machine."""

    name: str
    states: dict[int, State] = field(default_factory=dict)

    def get_initial_state(self) -> State | None:
        """Get the initial state (state with id 0)."""
        return self.states.get(0)

    def get_state(self, state_id: int) -> State | None:
        """Get a state by its ID."""
        return self.states.get(state_id)
