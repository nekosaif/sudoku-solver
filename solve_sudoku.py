import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

def read_sudoku_from_file(file_path):
    """
    Reads a Sudoku puzzle from a text file.

    Args:
        file_path (str): Path to the file containing the Sudoku board.
    
    Returns:
        List[List[int]]: A 2D list representing the Sudoku board.
                        Empty cells are represented by 0.
    """
    with open(file_path, 'r') as f:
        sudoku = []
        for line in f.readlines():
            row = list(map(int, line.split()))
            sudoku.append(row)
    return sudoku

def is_valid(board, row, col, num):
    """
    Checks if a number can be placed in a specific cell without breaking Sudoku rules.

    Args:
        board (List[List[int]]): The current state of the Sudoku board.
        row (int): The row of the cell.
        col (int): The column of the cell.
        num (int): The number to check.
    
    Returns:
        bool: True if placing the number is valid, False otherwise.
    """
    # Check the row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def find_empty(board):
    """
    Finds the first empty cell (represented by 0) in the Sudoku board.

    Args:
        board (List[List[int]]): The current state of the Sudoku board.
    
    Returns:
        tuple: The row and column indices of the first empty cell, or None if no empty cell is found.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

class SudokuSolver(QWidget):
    """
    A class to create a GUI-based Sudoku solver using PyQt.
    """
    def __init__(self, board):
        """
        Initializes the Sudoku solver GUI and logic.

        Args:
            board (List[List[int]]): The initial Sudoku board to solve.
        """
        super().__init__()
        self.board = board  # Store the Sudoku board
        self.gui_cells = []  # To store the GUI cells corresponding to the board
        self.initUI()  # Initialize the GUI
        self.timer = 0.001  # Time delay between updates for visualization

    def initUI(self):
        """
        Initializes the user interface for the Sudoku solver.
        """
        self.setWindowTitle('Sudoku Solver')
        self.setStyleSheet("background-color: #1e1e1e;")  # Set background color
        
        # Create a grid layout to represent the Sudoku board
        grid = QGridLayout()
        self.setLayout(grid)

        # Populate the grid with labels representing the Sudoku cells
        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = QLabel(self)
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet("color: #cccccc; border: 1px solid #cccccc;")
                cell.setFont(QFont('Helvetica', 20))
                if self.board[i][j] != 0:
                    # If the cell is not empty, display the number and use a different background
                    cell.setText(str(self.board[i][j]))
                    cell.setStyleSheet("color: #cccccc; border: 1px solid #cccccc; background-color: #2a2a2a;")
                else:
                    # Display a bullet point for empty cells
                    cell.setText("•")
                    cell.setStyleSheet("color: #ffa500; border: 1px solid #cccccc; background-color: #2a2a2a;")
                grid.addWidget(cell, i, j)
                row_cells.append(cell)
            self.gui_cells.append(row_cells)

        # Add spacing between 3x3 blocks to mimic traditional Sudoku grid formatting
        for i in range(3):
            grid.setRowMinimumHeight(i * 3 + 2, 30)
            grid.setColumnMinimumWidth(i * 3 + 2, 30)

        self.setGeometry(300, 300, 400, 400)  # Set the size and position of the window
        self.show()

    def solve_sudoku(self):
        """
        Solves the Sudoku puzzle using backtracking, updating the GUI at each step.
        
        Returns:
            bool: True if the Sudoku is solved, False if no solution exists.
        """
        # Find an empty cell to start solving
        empty_cell = find_empty(self.board)
        if not empty_cell:
            return True  # Puzzle is solved if no empty cells are left

        row, col = empty_cell

        # Try placing numbers 1 to 9 in the empty cell
        for num in range(1, 10):
            if is_valid(self.board, row, col, num):
                # Place the number if it's valid
                self.board[row][col] = num
                self.gui_cells[row][col].setText(str(num))
                self.gui_cells[row][col].setStyleSheet("color: #aaffaa; border: 1px solid #cccccc;")
                QApplication.processEvents()  # Update the GUI
                QTimer.singleShot(50, lambda: None)  # Small delay for visual effect
                time.sleep(self.timer)  # Pause for visualization

                # Recursively solve the rest of the puzzle
                if self.solve_sudoku():
                    return True

                # Backtrack if the current solution doesn't work
                self.board[row][col] = 0
                self.gui_cells[row][col].setText("")
                self.gui_cells[row][col].setStyleSheet("color: red; border: 1px solid #cccccc;")
            else:
                # Update the cell's color to red if the number is not valid
                self.gui_cells[row][col].setStyleSheet("color: red; border: 1px solid #cccccc;")
                QApplication.processEvents()
                QTimer.singleShot(50, lambda: None)
                time.sleep(self.timer)

        return False  # Return False if no number works in this cell

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku_board = read_sudoku_from_file("sudoku.txt")  # Load the Sudoku puzzle from file
    solver = SudokuSolver(sudoku_board)  # Initialize the solver with the puzzle
    solver.solve_sudoku()  # Solve the puzzle
    sys.exit(app.exec_())  # Exit the application when done
