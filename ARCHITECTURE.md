# Architecture Guide

Primary operating instructions live in #file:.github/copilot-instructions.md.
Use this file as the repository-level architecture map and module ownership guide.

## Core Architecture

- `src/main.py` is the application entry point. It initializes pygame, logging, configuration, mobile helpers, and the main event loop. It also lazy-loads screen classes and dispatches events based on the current state.
- `src/game_state.py` is the shared runtime model. It owns high-level progression state such as the active screen, level, lives, timers, rewards, powerups, and state transitions.
- `src/screens/` contains screen controllers. Each screen class handles input, update timing, and draw orchestration for one game mode such as welcome, level select, gameplay, win, or game over.
- `src/entities/` contains gameplay actors. `Snake` is the main entity and owns movement, animation state, and entity-specific behavior.
- `src/utils.py`, `src/constants.py`, `src/config_manager.py`, and `src/logger_setup.py` provide shared infrastructure: constants, helper functions, configuration loading, and logging.
- `src/ui/` contains reusable presentation helpers such as buttons, text rendering, animations, and enhanced graphics.
- `src/assets/` contains visual effect systems and shape/particle helpers. Treat these as rendering support, not as the source of gameplay rules.
- `tests/` mirrors behavior-oriented modules and should stay aligned with gameplay state, utility behavior, and screen logic.

## Ownership Boundaries

Behavioral logic lives in the modules that decide game rules or state changes:

- `src/game_state.py` for progression, requests, timers, rewards, powerups, and state transitions.
- `src/screens/` for screen-specific event handling, flow control, and orchestration.
- `src/entities/` for actor behavior such as movement, reactions, and collision-facing behavior.

UI and asset logic lives in the modules that draw, animate, or decorate the experience:

- `src/ui/` for reusable UI widgets and presentation helpers.
- `src/assets/` for particles, shapes, and other visual effects.
- `src/screens/game_draw_helpers.py` for gameplay rendering helpers that should stay presentation-focused.

Keep game rules out of UI helpers. Rendering modules can read state, but they should not become the authoritative source for score, progression, or win/loss logic.

## Naming Conventions

- Python modules use `snake_case.py`.
- Classes use `PascalCase`.
- Constants use `UPPER_SNAKE_CASE` and are centralized in `src/constants.py` when shared.
- Screen controller classes end with `Screen`.
- Entity classes are singular nouns such as `Snake`.
- Helper functions use verb-first or action-oriented names such as `draw_game_ui`, `update_powerups`, or `generate_new_food`.

## Agent Workflow

Prefer zero-search execution when asking an agent to change behavior.

- Pin the owning implementation file.
- Pin the nearest caller or coordinating file.
- Avoid broad prompts that omit file anchors.

Examples:

- Gameplay rule change: #file:src/game_state.py and #file:src/screens/game_screen.py
- Snake behavior change: #file:src/entities/snake.py and #file:src/screens/game_screen.py
- UI rendering change: #file:src/ui/text_renderer.py and #file:src/screens/game_draw_helpers.py

If a future audio bug appears, do not ask only for "fix the audio bug." Pin the file that triggers the sound and the file that calls it so the agent does not search unrelated parts of the repository.
