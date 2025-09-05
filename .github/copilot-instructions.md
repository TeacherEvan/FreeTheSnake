# FreeTheSnake - Kindergarten Snake Game

FreeTheSnake is a Python-based educational snake game designed for kindergarten students. The game teaches shape recognition, color identification, letters, and numbers through engaging gameplay using pygame.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- Ensure Python 3.12+ is available: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`
  - NEVER CANCEL: Installation takes 30-60 seconds depending on network. Set timeout to 120+ seconds.
  - Dependencies: pygame, numpy, matplotlib
  - If installation fails due to network issues, document the limitation and continue with existing packages
- Verify installation: `python -c "import pygame, numpy, matplotlib; print('Dependencies OK')"`

### Build and Validation
- No build process required (Python interpreted language)
- Compile-check all Python files: `find src/ -name "*.py" -exec python -m py_compile {} \;`
  - Takes <1 second. Use 10+ second timeout.
- Compile-check single file: `python -m py_compile src/main.py`
  - Takes <1 second. Use 5+ second timeout.

### Testing
- Run unit tests: `PYTHONPATH=src python -m unittest discover tests/ -v`
  - NEVER CANCEL: Tests complete in <1 second. Set timeout to 30+ seconds.
  - Expected: 5/9 tests pass (known test issues exist, see Common Issues)
  - Uses Python unittest framework (no pytest required)
- Test individual module: `PYTHONPATH=src python -m unittest tests.test_game_state -v`

### Running the Application
- Start the game: `python src/main.py`
  - NEVER CANCEL: Game starts immediately but may crash on headless systems
  - Requires display/GUI environment for full functionality
  - On headless systems: Use `timeout 10 python src/main.py` to test startup
- Application cannot be fully validated without a display environment

## Validation
- ALWAYS run compile-check after making code changes: `find src/ -name "*.py" -exec python -m py_compile {} \;`
- ALWAYS test imports work: `PYTHONPATH=src python -c "from main import main; print('Imports OK')"`
- Run the limited test suite to ensure no new failures: `PYTHONPATH=src python -m unittest discover tests/ -v`
- For display-capable environments: Start the game and verify the welcome screen appears
- ALWAYS clean up Python cache files: `find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true`

## Common Issues and Workarounds
- **Test failures**: 4 known test failures exist (see Known Test Issues below)
- **Import errors in tests**: Run with `PYTHONPATH=src` prefix
- **Game startup crashes**: Expected on headless systems, game requires display
- **Missing character_colors attribute**: Known issue in welcome_screen.py
- **Network timeouts during pip install**: Use existing packages, installation may fail in some environments

### Known Test Issues
1. `test_assign_new_request`: Missing `import random` in game_state.py
2. `test_reset_level`: NoneType error in reset_level function
3. `test_draw_text`: Missing pygame import in test_utils.py
4. `test_check_win_condition`: Function returns None instead of boolean
5. `test_get_cage_rect`: Width calculation mismatch

## Project Structure and Navigation

### Key Source Files
- `src/main.py` - Application entry point and main game loop
- `src/constants.py` - Game constants, colors, levels, font definitions
- `src/game_state.py` - Central game state management
- `src/utils.py` - Utility functions for drawing, rectangles, text rendering
- `src/entities/` - Game entities (snake implementation)
- `src/screens/` - Different game screens (welcome, game, level select, etc.)
- `src/ui/` - UI components (buttons, animations, text rendering)
- `src/assets/` - Game assets (particles, shapes)

### Test Files
- `tests/test_game_state.py` - Game state functionality tests
- `tests/test_utils.py` - Utility function tests

### Configuration Files
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns (includes __pycache__)

## Common Tasks

### Adding New Game Features
1. Update constants in `src/constants.py` if needed
2. Modify game state in `src/game_state.py` for state management
3. Add UI components in `src/ui/` or update existing screens in `src/screens/`
4. Always run compile-check: `find src/ -name "*.py" -exec python -m py_compile {} \;`
5. Test with: `PYTHONPATH=src python -m unittest discover tests/ -v`

### Code Style and Standards
- No formal linting tools configured (no flake8, pylint, black)
- Follow existing code style patterns in the codebase
- Use Python docstrings for new functions following existing patterns
- Import order: standard library, third-party (pygame, numpy), local modules

### Repository Contents Reference
```
.
├── .github/                     # GitHub configurations (you are here)
├── .snapshots/                  # AI interaction snapshots (ignore)
├── src/                         # Main source code
│   ├── main.py                  # Entry point
│   ├── constants.py             # Game constants and configuration
│   ├── game_state.py           # Game state management
│   ├── utils.py                # Utility functions
│   ├── entities/               # Game entities
│   │   └── snake.py           # Snake entity implementation
│   ├── screens/               # Game screens
│   │   ├── welcome_screen.py   # Welcome/start screen
│   │   ├── game_screen.py      # Main game screen
│   │   ├── level_select_screen.py # Level selection
│   │   └── ...                # Other game screens
│   ├── ui/                    # UI components
│   │   ├── button.py          # Button implementation
│   │   ├── animations.py      # Animation system
│   │   └── ...               # Other UI components
│   └── assets/               # Game assets
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── .gitignore              # Git ignore patterns
```

### Common Constants Reference
- `STATE_WELCOME = 0` - Welcome screen state
- `STATE_LEVEL_SELECT = 1` - Level selection state  
- `STATE_PLAYING = 2` - Active gameplay state
- `STATE_GAME_OVER = 5` - Game over state
- `FPS = 60` - Game frame rate
- Color constants: `WHITE`, `BLACK`, `RED`, `GREEN`, `BLUE`, etc.
- `LEVELS` dictionary contains level configurations with target, time, and speed multipliers

## Frequently Referenced Commands
Save time by using these common command patterns:

### Development Workflow
```bash
# Full validation after changes
PYTHONPATH=src python -c "from main import main; print('Imports OK')"
find src/ -name "*.py" -exec python -m py_compile {} \;
PYTHONPATH=src python -m unittest discover tests/ -v
```

### Quick Testing
```bash
# Test specific functionality
PYTHONPATH=src python -c "from game_state import GameState; gs = GameState(); print('GameState OK')"
PYTHONPATH=src python -c "from utils import draw_text; print('Utils OK')"
```

### Cleanup
```bash
# Remove Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
```