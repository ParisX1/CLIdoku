"""
Sudoku command line game.

Author: Thomas O'Mara
Date: 2024
License: MIT License
"""

import copy
import random
import timeit

def play(board):
    """
    Game loop

    Args:
        board (int array): sudoku board for the player to solve

    Returns:
        int: return zero on game success
    """

    # Deep Copy Board For Undo Function
    boardCopy = copy.deepcopy(board)
    printBoard(board)
    movesList = []

    # Play Game Until Solved
    while True:

        # Assign User Input
        userInput = input("Enter move as 'row col value' OR 'help' : ").split(' ')
        if len(userInput) == 3 and userInput[0].isdecimal() and userInput[1].isdecimal() and userInput[2].isdecimal():
            i = int(userInput[0])
            j = int(userInput[1])
            x = int(userInput[2])

            # Check Allowed Moves & Update Board If Allowed
            allowedMoves = options(board, i, j)
            if board[i][j] != 0:
                print("Board position taken.")
            elif x in allowedMoves:
                board[i][j] = x
                movesList.append([i,j])
            else:
                print("The value {} is not allowed.".format(str(x)))
            printBoard(board)

        # Undo Last Move
        elif (userInput[0] == 'u' or userInput[0] == 'undo'):
            if len(movesList) > 0:
                undoRef = movesList.pop()
                board[undoRef[0]][undoRef[1]] = 0
                printBoard(board)
            else:
                print("No more moves to  undo")

        # Provide Hint
        elif (userInput[0] == 'h' or userInput[0] == 'hint'):
            hintRow, hintCol = hint(board)
            hintCopy = copy.deepcopy(board)
            hintCopy[hintRow][hintCol] = "*"
            printBoard(hintCopy)
            print("({}, {})".format(hintRow, hintCol))

        # Solve Board
        elif (userInput[0] == 's' or userInput[0] == 'solve'):
            board = solve(board, 1)
            printBoard(board)

        # New Board
        elif userInput[0] == 'n' or userInput[0] == 'new':
            boardSize = getBoardSize()
            board = generate(boardSize)
            boardCopy = copy.deepcopy(board)
            printBoard(board)

        # Help / Display Options
        elif userInput[0] == 'help':
            printOptions()

        # Quit Game
        elif userInput[0] == 'q' or userInput[0] == 'quit':
            return 0

        # Restart Chosen Board
        elif userInput[0] == 'r' or userInput[0] == 'restart':
            board = boardCopy
            boardCopy = copy.deepcopy(board) # Deepcopy For Restart
            movesList = [] # Reset Moves List
            printBoard(board)

        else:
            print('Invalid input')

        # Check For Board Completion
        if checkBoardCompleted(board):
            print("\nCongratulations you have solved the Sudoku!")
            return 0

def printBoard(board):
    """
    Print board with aligned rows and columns

    Args:
        board (int array): sudoku board
    """
    length = int(len(board[0]))
    k = int(length**.5)
    rowLength = int(length + k +1)
    print("-" * rowLength)
    for row1 in range(k):
        for row2 in range(k):
            rowRef = int(((row1 * k) + row2))
            print("|", end='')
            for col1 in range(k):
                for col2 in range(k):
                    colRef = int(((col1 * k) + col2))
                    if board[rowRef][colRef] == 0:
                        print(" ", end='')
                    elif board[rowRef][colRef] == 10:
                        print("A", end='')
                    elif board[rowRef][colRef] == 11:
                        print("B", end='')
                    elif board[rowRef][colRef] == 12:
                        print("C", end='')
                    elif board[rowRef][colRef] == 13:
                        print("D", end='')
                    elif board[rowRef][colRef] == 14:
                        print("E", end='')
                    elif board[rowRef][colRef] == 15:
                        print("F", end='')
                    elif board[rowRef][colRef] == 16:
                        print("G", end='')
                    else:
                        print(board[rowRef][colRef], end='')
                print("|", end='')
            print("")
        print("-" * rowLength)

def generate(k):
    """
    Generate a new random board

    Args:
        k (int): size of board k**2 by k**2.  If k = 2, the board is 4 x 4

    Returns:
        int array: A random, uniquely solvable k**2 by k**2 board
    """

    if k == 2:
        print("Generating board... (this may take a while)")
    elif k > 2:
        print("Generating board... (this may take a very long time)")

    n = k**2

    # Generate a New Completed Board
    board = createEmptyBoard(k)
    board = generateRandom(board)[0]

    # Remove First n Values From Random Positions
    numbers = []
    for i in range(1,n + 1):
        numbers.append(i)
    randRow = 0
    randCol = 0
    numberToRemove = 0
    while len(numbers) > 0:
        randRow =  random.randrange(0, n)
        randCol =  random.randrange(0, n)
        numberToRemove = board[randRow][randCol]
        if numberToRemove in numbers:
            board[randRow][randCol] = 0
            numbers.pop(numbers.index(numberToRemove))

    # Remove Random Values Until Unique Solution Found
    uniqueBoard = []
    while len(backtrack(board, 2)) < 2:
        uniqueBoard = copy.deepcopy(board)
        nextIteration = False
        while nextIteration == False:
            randRow = random.randrange(0, n)
            randCol = random.randrange(0, n)
            if board[randRow][randCol] != 0:
                board[randRow][randCol] = 0
                nextIteration = True
    return uniqueBoard

def getBoardSize():
    """
    Prompt user to input the size of the board either small, normal or big

    Returns:
        int: The size (k) of the board.  Eg if k = 2 we have a 2**2 board (4 x 4)
             k is the size of each subarray within the board
    """
    while(True):
        size = input("Choose board size ('small' 4x4 | 'normal' 9x9 | 'big' 16x16): ").strip().lower()
        if size == "small":
            return 2
        elif size == "normal":
            return 3
        elif size == "big":
            return 4


def createEmptyBoard(k):
    """
    Create a k**2 by k**2 Board

    Args:
        k (int): size of board k**2.  Ie if k = 2 the board is 4 x 4

    Returns:
        int array: empty k**2 by k**2 array
    """
    n = k**2
    board = []
    for i in range(n):
        board.append([0] * n)
    return board

def generateRandom(board):
    """
    Generate a ramdomised board

    Args:
        board (int array): empty sudoku board

    Returns:
        int array: randomised board
    """
    board = inferred(board)
    if checkBoardCompleted(board):
        return [board]
    else:
        boardList = []
        row, col = randomPosition(board)
        optionsList = options(board, row, col)
        random.shuffle(optionsList)
        for option in optionsList:
            board[row][col] = option
            boardCopy = copy.deepcopy(board)
            boardList += generateRandom(boardCopy)
            if len(boardList) > 0 and checkBoardCompleted(boardList[0]):
                return boardList
        return boardList

def randomPosition(board):
    """
    Find an empty position on the board

    Args:
        board (int array): sudoku board

    Returns:
        int: a random row and col position representing an empty position
    """
    n = len(board[0])
    emptyPositions = []
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:
                emptyPositions.append([row,col])
    returnValues = emptyPositions[random.randint(0, len(emptyPositions)-1)]
    return returnValues[0], returnValues[1]

def hint(board):
    """
    Find the row, col position that is best to play next based on finding the location
    with the lowest number of potential values that can be played at each empty location

    Args:
        board (int array): sudoku board

    Returns:
        int: row and col location that is best to play next (least number of potential options)
    """
    rowRef = 0
    colRef = 0
    minOptions = len(board)
    if checkBoardCompleted(board):
        return None, None
    else:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    if len(options(board, i, j)) < minOptions:
                        minOptions = len(options(board, i, j))
                        rowRef = i
                        colRef = j
        return rowRef, colRef

def options(board, i, j):
    """
    Generate a list of valid values that can be played at a specified i, j position

    Args:
        board (int array): sudoku board
        i (int): row position
        j (int): col position

    Returns:
        int array: list of possible valid values that can be placed at position i, j
    """
    allowedValues = []
    allCurrentValues = subgridValues(board, i, j)
    rowColList = colRowValues(board, i, j)
    for i in rowColList:
        if i not in allCurrentValues:
            allCurrentValues.extend([i])
    for i in range(1, len(board) + 1):
        if i not in allCurrentValues:
            allowedValues.append(i)
    return allowedValues

def subgridValues(board, row, col):
    """
    Generate a list of values within a sub grid of the board

    Args:
        board (int array): sudoku board
        row (int): row position to find the sub array
        col (int): col position to find the sub array

    Returns:
        int array: list of values within the sub array
    """
    length = int(len(board[0]))
    subgridLen = int(length**.5)
    row1 = int(row // subgridLen)
    col1 = int(col // subgridLen)
    valuesList = []
    for row2 in range(subgridLen):
        rowRef = int(((row1 * subgridLen) + row2))
        for col2 in range(subgridLen):
            colRef = int(((col1 * subgridLen) + col2))
            num = int((board[rowRef][colRef]))
            if num != 0:
                valuesList.append(num)
    return valuesList

def colRowValues(board, row, col):
    """
    Generate a list of values on a board for a specified row and column

    Args:
        board (int array): sudoku board
        row (int): row position to find the board values
        col (int): col position to find the board values

    Returns:
        int array: list of values on the board along a given row and col
    """
    rowColValues = []
    for i in range(len(board)):
        if board[row][i] != 0:
            rowColValues.append(board[row][i])
        if board[i][col] != 0:
            rowColValues.append(board[i][col])
    return rowColValues

def checkBoardCompleted(board):
    """
    Check if the board is completed / solved

    Args:
        board (int array): sudoku board

    Returns:
        bool: True if board is solved; False otherwise
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return False
    return True

def solve(board, solutions = 1):
    """
    Solve sudoku board via backtracking (calls backtracking function)
    Times solve time for benchmarking

    Args:
        board (int array): sudoku board to solve
        solutions (int, optional): Only return solutions number of solved boards. Defaults to 1.

    Returns:
        int array: solved sudoku board
    """
    startTime = timeit.default_timer()
    board = backtrack(board, solutions)

    endTime = timeit.default_timer()
    totalTime = endTime - startTime
    min = int(totalTime // 60)
    sec = totalTime % 60
    sec = round(sec % 60, 3)
    print("Run time: {} min {} secs".format(min, sec))

    return board[0]

def backtrack(board, solutions = 1):
    """
    Solve a sudoku board via backtracking

    Inference
    Use inference to solve board as much as possible until "stuck"; then make a single "smart guess";
    and again, infer as much as possible.  This approach replicates actual human behavior in solving
    Sudoku and substantially reduces computational complexity, enabling solving the larger / more
    complex boards in reasonable time.  Inference requires no recursion/backtracking to implement and
    thus is highly efficient, especially where we may traverse long "dead end" recursive branches for
    the larger and more difficult boards.

    Backtracking
    Base case is a solved board added to results list.
    For backtracking, select the first empty (zero-value) cell and obtain the list of valid options.
    Then recursively iterate over these options until reaching base-case and return the solved board
    to results list.

    Args:
        board (int array): current state of the sudoku board
        solutions (int, optional): Only return solutions number of solved boards. Defaults to 1.

    Returns:
        int array (array of solved boards): solved sudoku boards
    """
    board = inferred(board)
    if checkBoardCompleted(board):
        return [board]
    else:
        res = []
        row, col = quickHint(board)
        for o in options(board, row, col):
            board[row][col] = o
            boardCopy = copy.deepcopy(board)
            if len(res) < solutions: # Only return "solutions" number of solved boards
                res += backtrack(boardCopy)
        return res

def quickHint(board):
    """
    Quickly find the best position for a hint based on the heuristic that the row or col
    with the lowest number of empty values would be the best place for the next guess

    Args:
        board (int array): sudoku board

    Returns:
        int: row and col position with the highest count (lowest empty positions)
    """
    n = len(board[0])
    rowCount=[0]*n
    colCount=[0]*n

    # Count Values in Rows and Cols
    for i in range(n):
        for j in range(n):
            if board[i][j]  != 0:
                rowCount[i] += 1
                colCount[j] += 1

    # Find Max
    maxValue = 0
    maxRow = None
    maxCol = None
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                if rowCount[i] + colCount[j] > maxValue:
                    maxValue = rowCount[i] + colCount[j]
                    maxRow = i
                    maxCol = j

    return maxRow, maxCol

def inferred(board):
    """
    Check each non-solved position and attempt to solved via "Forward Single" or "Backward Single" methods

    Args:
        board (int array): sudoku board to solve

    Returns:
        int array: new Sudoku board with all values field from input board plus all values that can be
        inferred by repeated application of forward and backward single rule
    """
    inferCopy = copy.deepcopy(board)
    improved = True
    while improved == True:
        improved = False
        for i in range(len(inferCopy)):
            for j in range(len(inferCopy[i])):
                if inferCopy[i][j] == 0:
                    solution = valueBySingle(inferCopy, i, j)
                    if solution  !=  None:
                        inferCopy[i][j] = solution
                        improved = True
    return inferCopy

def valueBySingle(board, i, j):
    """
    Check if position i, j can be solved by either "Forward Single" or "Backward Single" methods

    Forward Single:  Find if a row, col or sub grid has only one value remaining
    Backward Single: For the allowable options for a cell, find if, given the the row, col or sub
                     grid allowable options, a value exists that can only be played at that cell

    Args:
        board (int array): sudoku board
        i (int): row position
        j (int): column position

    Returns:
        int array: The correct value for field (i, j) in board if it can be inferred as either
        a forward or a backward single; or None otherwise.
    """

    # Check Forward Single
    optionsList = options(board, i, j)
    if len(optionsList) == 1:
        return optionsList[0]

    # If No Forward Single, Check Forward Backward

    # Check Rows
    rowOptions = optionsInRow(board, i, j)
    for x in optionsList:
        if x not in rowOptions:
            return x

    # Check Columns
    colOptions = optionsInCol(board, i, j)
    for x in optionsList:
        if x not in colOptions:
            return x

    # Check Subgrid
    subOptions = optionsInSubgrid(board, i, j)
    for x in optionsList:
        if x not in subOptions:
            return x

    return None

def optionsInRow(board, i, j_exclude):
    """
    Generate a unique list of all allowed values for all positions on the the row i
    Ignore position j_exclude

    Args:
        board (int array): sudoku board
        i (int): row to check
        j_exclude (int): row position to exclude

    Returns:
        int array: List of allowed values for each cell on row i (excluding j_exclude)
    """
    rowOptionsList = []
    cellOptions = []
    for j in range(len(board[i])):
        if (board[i][j] == 0):
            if (j != j_exclude):
                cellOptions += options(board, i, j)
    for x in cellOptions:
        if x not in rowOptionsList:
            rowOptionsList.append(x)
    return rowOptionsList

def optionsInCol(board, i_exclude, j):
    """
    Generate a unique list of all allowed values for all positions on the the col j
    Ignore position i_exclude

    Args:
        board (int array): sudoku board
        i_exclude (int): col position to exclude
        j (int): col to check

    Returns:
        int array: List of allowed values for each cell on col j (excluding i_exclude)
    """
    colOptionsList = []
    cellOptions = []
    for i in range(len(board)):
        if (board[i][j] == 0):
            if (i != i_exclude):
                cellOptions += options(board, i, j)
    for x in cellOptions:
        if x not in colOptionsList:
            colOptionsList.append(x)
    return colOptionsList

def optionsInSubgrid(board, i, j):
    """
    Generate a unique list of all allowed values for all positions with the sub grid found at
    location i, j.  Ignores the cell i, j

    Args:
        board (int array): sudoku board
        i (int): row location to find sub array
        j (int): col location to find sub array

    Returns:
        int array: List of allowed values for each cell with the sub grid at i, j (excluding i, j itself)
    """

    subOptionsList = []
    subOptions = []
    activeRef = [i,j]

    length = int(len(board[0]))
    k = int(length**.5) # Sub grid width (# cells)
    row1 = int(i // k) # Set base row sub grid number (there are k * k sub grids)
    col1 = int(j // k)

    for row2 in range(k):
        rowRef = int(((row1 * k) + row2))
        for col2 in range(k):
            colRef = int(((col1 * k) + col2))

            refChecker = [rowRef, colRef]

            if int(board[rowRef][colRef]) == 0:
                if refChecker != activeRef:
                        subOptions += options(board, rowRef, colRef)

    # Create List of Options Where Each Option Listed Once
    for x in subOptions:
        if x not in subOptionsList:
            subOptionsList.append(x)
    return subOptionsList

def printOptions():
    """
    Print valid user input list for playing the game
    """
    print("\n~ Sudoku Command Line Game ~")
    print("Inputs:")
    print("'rol col value' - place a value on the board.  Eg '3 2 6' will place 6 at row 3, col 2.")
    print(" - Note that indexing is zero based")
    print("'undo' or 'u' - undo your last move.")
    print("'hint' or 'h' - an asterisk will be displayed at the easiest location for your next play.")
    print("'solve' or 's' - the board will solved and displayed.")
    print("'new' or 'n' - generate a new board.")
    print("'help' or 'h' - display valid input options.")
    print("'restart' or 'r' - restart the board from the beginning.")
    print("'quit' or 'q' - quit the game.")

def main():
    print("~ Sudoku Command Line Game ~")
    boardSize = getBoardSize()
    board = generate(boardSize)
    play(board)

if __name__ == "__main__":
    main()
