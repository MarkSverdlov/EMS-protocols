# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
python main.py
# or
python -m protocols
```

No external dependencies required - uses only tkinter from the standard library.

## Architecture

This is a tkinter-based EMS protocols practice game with MVC-style architecture:

**Controllers:**
- `controller.py` (App) - Main orchestrator managing screen transitions and protocol loading
- `gameplay.py` (GameplayController) - Event-driven game logic with no UI dependencies; tracks state, score, and answer validation

**Models** (`models/`):
- `Protocol` - Collection of states representing a complete medical protocol
- `State` - Single decision point with type (INTRO/QUESTION/FINAL), correct/wrong answers, and next state references
- StateType enum determines UI behavior: INTRO shows "Next" button, QUESTION shows 4 answer options, FINAL triggers results

**Screens** (`screens/`):
- `ProtocolSelectScreen` - Protocol list selection
- `GameScreen` - Main gameplay with answer buttons (keys 1-4) and feedback display
- `ResultsScreen` - Final score and performance message

**Parser** (`parser.py`) - Loads `.md` protocol files from `data/` directory

## Protocol File Format

Protocols are markdown files in `data/` with this structure:

```
Protocol Name
=============
0: Initial state description
# Next states:
1
2

1: Question state description
# Correct answer:
The correct answer text
# Wrong answers:
Wrong option 1
Wrong option 2
(... more wrong answers, 3 randomly selected)
# Next state:
3
```

States can reference other protocols by name for cross-protocol linking.

## Color Scheme Constants

Defined in `base.py` and used throughout:
- `BG_COLOR = "#2c3e50"` (dark blue-gray background)
- `CARD_COLOR = "#ecf0f1"` (light gray cards)
- `SUCCESS_COLOR = "#27ae60"` (green for correct)
- `ERROR_COLOR = "#e74c3c"` (red for incorrect)
- `DARK_TEXT = "#2c3e50"` (dark text on light backgrounds)
