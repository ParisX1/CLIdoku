# Sudoku Game

A command-line based Sudoku game written in Python.

## Table of Contents

- [Sudoku Game](#sudoku-game)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Commands](#commands)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Generate random Sudoku puzzles.
- Validate Sudoku board state.
- Solve Sudoku puzzles using a solver algorithm.
- Interactive command-line interface for playing the game.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ParisX1/Sudoku-Game.git
    cd sudoku-game
    ```

1. Install the dependencies (shouldn't be required):
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the game from the command line:
```sh
python sudoku-game.py
```

## Commands

`row col val`: try value val at row col (with zero indexing).
`help`: Show game commands.
`exit`: Exit the game.

## Contributing

1. Fork the repository.
1. Create a new branch (git checkout -b feature-branch).
1. Commit your changes (git commit -am 'Add new feature').
1. Push to the branch (git push origin feature-branch).
1. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
