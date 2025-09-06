# FreeTheSnake - Kindergarten Snake Game

Welcome to FreeTheSnake! This engaging and colorful game is designed to enhance enthusiasm and learning for kindergarten students through fun gameplay and vibrant visuals.

## Project Overview

FreeTheSnake is a simple yet captivating educational game where players control a friendly snake that moves around the screen, collecting various shapes, numbers, and letters. The game encourages hand-eye coordination, shape recognition, letter recognition, and color identification in a playful environment.

## Features

- **Engaging Gameplay**: Players guide the snake to collect requested items while avoiding obstacles
- **Educational Content**: Numbers (1-10), letters (A-Z, a-z), and shapes for comprehensive learning
- **Colorful Visuals**: Bright and cheerful graphics designed to attract young children
- **Simple Controls**: Easy-to-use arrow key controls suitable for kindergarten students
- **Character Selection**: Multiple snake characters with different colors and names
- **Progressive Levels**: Difficulty increases as players advance through levels
- **Animated Effects**: Colorful animations and visual feedback to keep children engaged

## Requirements

- Python 3.8 or higher
- pygame 2.0 or higher
- numpy
- matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TeacherEvan/FreeTheSnake.git
   ```

2. Navigate to the project directory:
   ```bash
   cd FreeTheSnake
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the following command:
```bash
python src/main.py
```

### Game Controls
- **Arrow Keys**: Move the snake
- **Mouse**: Navigate menus and select options
- **ESC**: Pause game or return to menu

## Development

### Running Tests
To run the test suite:
```bash
PYTHONPATH=src python -m unittest discover tests/ -v
```

### Project Structure
```
FreeTheSnake/
├── src/
│   ├── main.py              # Main game entry point
│   ├── constants.py         # Game constants and configuration
│   ├── game_state.py        # Game state management
│   ├── utils.py             # Utility functions
│   ├── screens/             # Game screens
│   ├── entities/            # Game entities (snake, food)
│   ├── ui/                  # UI components
│   └── assets/              # Game assets
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Educational Goals

This game is designed to help kindergarten students with:
- **Letter Recognition**: Uppercase and lowercase letters
- **Number Recognition**: Numbers 1-10 and basic counting
- **Shape Recognition**: Basic geometric shapes
- **Hand-Eye Coordination**: Controlling the snake with arrow keys
- **Color Identification**: Different colored items and characters
- **Following Instructions**: Collecting specific requested items

## Contributing

Contributions are welcome! If you have ideas for new features or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thank you for checking out FreeTheSnake! We hope it brings joy and learning to young players. Special thanks to educators who provided feedback on the educational value and age-appropriate design.