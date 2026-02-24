"""Parser for markdown protocol files."""

from pathlib import Path

from .models import Protocol, State, StateType


def parse_protocol_file(filepath: Path) -> Protocol:
    """Parse a markdown protocol file into a Protocol object.

    Format:
        Protocol Name
        ================================
        0: State description
        # Correct answer:
        Answer text
        # Wrong answers:
        Wrong answer 1
        Wrong answer 2
        # Next state:
        1
        2
    """
    content = filepath.read_text()
    lines = content.strip().split("\n")

    # Parse protocol name (first line before ===)
    protocol_name = lines[0].strip()

    # Skip the === line
    line_idx = 1
    while line_idx < len(lines) and lines[line_idx].startswith("="):
        line_idx += 1

    states: dict[int, State] = {}
    current_state_id: int | None = None
    current_description: str = ""
    current_correct: str | None = None
    current_wrong: list[str] = []
    current_next: list[int | str] = []
    section: str | None = None

    def save_current_state():
        nonlocal current_state_id, current_description, current_correct
        nonlocal current_wrong, current_next

        if current_state_id is None:
            return

        # Determine state type
        if not current_next:
            state_type = StateType.FINAL
        elif current_correct is None:
            state_type = StateType.INTRO
        else:
            state_type = StateType.QUESTION

        states[current_state_id] = State(
            id=current_state_id,
            description=current_description,
            state_type=state_type,
            correct_answer=current_correct,
            wrong_answers=current_wrong,
            next_state_ids=current_next,
        )

        # Reset for next state
        current_state_id = None
        current_description = ""
        current_correct = None
        current_wrong = []
        current_next = []

    while line_idx < len(lines):
        line = lines[line_idx].rstrip()
        line_idx += 1

        # Skip empty lines at section boundaries
        if not line and section is None:
            continue

        # Check for state definition (e.g., "0: Description")
        if ":" in line and not line.startswith("#"):
            parts = line.split(":", 1)
            try:
                state_id = int(parts[0].strip())
                # Save previous state if exists
                save_current_state()
                current_state_id = state_id
                current_description = parts[1].strip()
                section = None
                continue
            except ValueError:
                pass  # Not a state definition

        # Check for section headers
        if line.startswith("# Correct answer"):
            section = "correct"
            continue
        elif line.startswith("# Wrong answer"):
            section = "wrong"
            continue
        elif line.startswith("# Next state"):
            section = "next"
            continue

        # Empty line resets section (but not inside wrong answers)
        if not line:
            if section not in ("wrong",):
                section = None
            continue

        # Add content based on current section
        content_text = line.strip()
        if not content_text:
            continue

        if section == "correct":
            current_correct = content_text
            section = None
        elif section == "wrong":
            current_wrong.append(content_text)
        elif section == "next":
            # Try to parse as int (state ID) or keep as string (protocol name)
            try:
                current_next.append(int(content_text))
            except ValueError:
                current_next.append(content_text)

    # Save the last state
    save_current_state()

    return Protocol(name=protocol_name, states=states)


def load_protocols_from_directory(directory: Path) -> dict[str, Protocol]:
    """Load all protocol files from a directory."""
    protocols = {}

    if not directory.exists():
        return protocols

    for filepath in directory.glob("*.md"):
        protocol = parse_protocol_file(filepath)
        protocols[protocol.name] = protocol

    return protocols
