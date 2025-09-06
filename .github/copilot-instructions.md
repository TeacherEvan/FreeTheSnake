# FreeTheSnake - Kindergarten Snake Game

FreeTheSnake is a Python-based educational game built with pygame for kindergarten students. The game teaches letter recognition, number recognition, shape recognition, and hand-eye coordination through engaging snake gameplay.

**ALWAYS** reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Dependencies
- **Python Requirements**: Python 3.8+ required (Python 3.12.3 confirmed working)
- **Install Dependencies**: 
  ```bash
  pip install -r requirements.txt
  ```
  - Takes ~11 seconds to complete
  - Installs: pygame, numpy, matplotlib
  - **NEVER CANCEL**: Always let installation complete

### Build and Run
- **No Build Step Required**: This is a pure Python application with no compilation needed
- **Run the Game**:
  ```bash
  python src/main.py
  ```
  - Game initializes successfully in <1 second
  - Creates `logs/` directory with detailed logging
  - **GUI Application**: Requires display - will show "Broken pipe" errors in headless environments (this is expected)

### Testing
- **Run Unit Tests**:
  ```bash
  PYTHONPATH=src python -m unittest discover tests/ -v
  ```
  - Takes <1 second to complete
  - Runs 9 tests covering game state and utility functions
  - **NEVER CANCEL**: Tests are fast but always let complete
  - ALSA audio warnings are expected in headless environments

### Validation Commands
- **Test Full Application Stack**:
  ```bash
  # In headless environment (CI/servers)
  export SDL_VIDEODRIVER=dummy && timeout 10s python src/main.py
  
  # Check logs for successful initialization
  tail -20 logs/freethesnake_*.log
  ```
  - Application should initialize pygame, fonts, game state, and screens
  - Log should show "All screens initialized successfully"
  - **Expected**: Broken pipe errors when running headless (normal behavior)
  - **Expected**: Font warnings "Font is None for text..." in headless environments (fallback fonts work correctly)

## Validation Scenarios

### Manual Testing Requirements
**ALWAYS** run these validation steps after making code changes:

1. **Dependency Check**: `pip install -r requirements.txt` (takes ~11 seconds)
2. **Test Suite**: `PYTHONPATH=src python -m unittest discover tests/ -v` (takes <1 second)
3. **Application Startup**: `python src/main.py` with appropriate video driver
4. **Log Verification**: Check `logs/` directory for successful initialization

### Code Change Validation
- **For Game Logic Changes**: Always run the full test suite
- **For UI/Screen Changes**: Test application startup to ensure no import errors
- **For Configuration Changes**: Verify `config.ini` parsing and game initialization
- **For New Features**: Add corresponding unit tests in `tests/` directory

## Project Structure

### Repository Layout
```
FreeTheSnake/
├── .github/                 # GitHub configuration
├── .snapshots/             # AI interaction snapshots (ignore)
├── src/                    # Main source code
│   ├── main.py            # Game entry point
│   ├── constants.py       # Game constants and configuration
│   ├── game_state.py      # Game state management
│   ├── utils.py           # Utility functions
│   ├── config_manager.py  # Configuration file handling
│   ├── logger_setup.py    # Logging configuration
│   ├── screens/           # Game screens (welcome, game, etc.)
│   ├── entities/          # Game entities (snake, etc.)
│   ├── ui/               # UI components (buttons, text, animations)
│   └── assets/           # Game assets (particles, shapes)
├── tests/                 # Unit tests
├── logs/                 # Game logs (created at runtime)
├── config.ini            # Game configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

### Key Files and Components
- **Entry Point**: `src/main.py` - Initialize pygame and start main game loop
- **Game States**: Defined in `src/constants.py` (welcome, playing, game over, etc.)
- **Configuration**: `config.ini` for game settings, screen dimensions, debug options
- **Testing**: Uses Python unittest framework with test discovery
- **Logging**: Automatic file logging to `logs/` directory with timestamps

## Development Guidelines

### Code Quality
- **No Linting Tools**: No linting tools are currently configured
- **Testing Framework**: Uses Python unittest - add tests for new functionality
- **Code Style**: Follow existing patterns in the codebase
- **Error Handling**: Application has comprehensive error handling and logging

### Common Tasks

#### Adding New Game Features
1. Add constants to `src/constants.py` if needed
2. Implement logic in appropriate module (`entities/`, `screens/`, `ui/`)
3. Add corresponding unit tests in `tests/`
4. Test with full validation scenario
5. Verify logging shows expected behavior

#### Debugging Issues
1. Check `logs/` directory for detailed error information
2. Run tests to isolate component issues: `PYTHONPATH=src python -m unittest discover tests/ -v`
3. Test individual screens/components in isolation
4. Use debug mode: Set `debug_mode = true` in `config.ini`

#### Working with Configuration
- **Game Settings**: Modify `config.ini` for screen dimensions, FPS, debug options
- **Educational Content**: Configure letter/number/shape inclusion in `[Education]` section
- **Visual Effects**: Enable/disable animations, particles in `[Graphics]` section

## Environment Considerations

### Display Requirements
- **Local Development**: Requires active display for full GUI interaction
- **Headless/CI Environment**: Use `SDL_VIDEODRIVER=dummy` for testing
- **Expected Errors**: ALSA audio warnings and broken pipe errors in headless mode are normal

### Performance Notes
- **Startup Time**: <1 second for application initialization
- **Test Execution**: <1 second for full test suite
- **Dependency Installation**: ~11 seconds with good network connection
- **Memory Usage**: Minimal - suitable for resource-constrained environments

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure `PYTHONPATH=src` is set when running tests
- **Display Issues**: Use `SDL_VIDEODRIVER=dummy` in headless environments  
- **Audio Warnings**: ALSA warnings are expected in Docker/CI environments
- **Font Issues**: Application includes fallback font handling for missing system fonts
- **Font Warnings**: "Font is None" warnings in headless environments are expected (fallback fonts work correctly)

### Quick Fixes
- **Application Won't Start**: Check Python version (3.8+ required)
- **Tests Fail**: Verify all dependencies installed with `pip install -r requirements.txt`
- **Config Issues**: Check `config.ini` syntax and ensure all required sections exist

Remember: This is an educational game for kindergarten students focusing on learning through play. Any changes should maintain the educational value and child-friendly interface.