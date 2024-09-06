# CLIdoku - A CLI Sudoku Game

CLIdoku enables you to play Sudoku straight from your command-line interface. Generate unique boards in three sizes:
- Small (4 x 4)
- Normal (9 x 9)
- Big (16 x 16)

## Features

- Generate unique, random Sudoku puzzles
- Boards generated using a backtracking solver algorithm
- Moves are validated to ensure correctness
- Undo moves if you make a mistake
- Generate hints for next best position to play
- Interactive command-line interface for playing the game

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ThomasOMara/Sudoku-Game.git
    cd Sudoku-Game
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

`row col val`: Play value 'val' at position 'row', 'col' (with zero indexing).  
`undo`: Undo your last move.  
`hint`: Receive a hint for the best location to play.  
`solve`: Solve and display the solved board.  
`new`: Create a new board.  
`help`: Show game commands.  
`restart`: Restart the current board from the beginning.  
`quit`: Exit the game.  

## Contributing

1. Fork the repository.
1. Create a new branch (git checkout -b feature-branch).
1. Commit your changes (git commit -am 'Add new feature').
1. Push to the branch (git push origin feature-branch).
1. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
