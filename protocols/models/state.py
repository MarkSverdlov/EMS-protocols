from dataclasses import dataclass, field
from enum import Enum, auto
import random


class StateType(Enum):
    """Type of state in the protocol state machine."""

    INTRO = auto()  # No correct answer, just "Next" button
    QUESTION = auto()  # Has correct/wrong answers, shows 4 options
    FINAL = auto()  # Terminal state, triggers results screen


@dataclass
class State:
    """A state in the protocol state machine."""

    id: int
    description: str
    state_type: StateType
    correct_answer: str | None = None
    wrong_answers: list[str] = field(default_factory=list)
    next_state_ids: list[int | str] = field(default_factory=list)

    def sample_wrong_answers(self, n: int = 3) -> list[str]:
        """Sample n wrong answers from the available pool."""
        if len(self.wrong_answers) <= n:
            return self.wrong_answers.copy()
        return random.sample(self.wrong_answers, n)

    def get_shuffled_options(self) -> list[str]:
        """Get 4 shuffled options: 1 correct + 3 wrong answers."""
        if self.correct_answer is None:
            return []
        options = [self.correct_answer] + self.sample_wrong_answers(3)
        random.shuffle(options)
        return options

    def get_random_next_state_id(self) -> int | str | None:
        """Get a random next state ID from available transitions."""
        if not self.next_state_ids:
            return None
        return random.choice(self.next_state_ids)
