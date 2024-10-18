import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

def read_sudoku_from_file(file_path):
    with open(file_path, 'r') as f:
        sudoku = []
        for line in f.readlines():
            row = list(map(int, line.split()))
            sudoku.append(row)
    return sudoku

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

class SudokuSolver(QWidget):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.gui_cells = []
        self.initUI()
        self.timer = 0.001

    def initUI(self):
        self.setWindowTitle('Sudoku Solver')
        self.setStyleSheet("background-color: #1e1e1e;")
        
        grid = QGridLayout()
        self.setLayout(grid)

        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = QLabel(self)
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet("color: #cccccc; border: 1px solid #cccccc;")
                cell.setFont(QFont('Helvetica', 20))
                if self.board[i][j] != 0:
                    cell.setText(str(self.board[i][j]))
                    cell.setStyleSheet("color: #cccccc; border: 1px solid #cccccc; background-color: #2a2a2a;")
                else:
                    cell.setText("•")
                    cell.setStyleSheet("color: #ffa500; border: 1px solid #cccccc; background-color: #2a2a2a;")
                grid.addWidget(cell, i, j)
                row_cells.append(cell)
            self.gui_cells.append(row_cells)

        for i in range(3):
            grid.setRowMinimumHeight(i * 3 + 2, 30)
            grid.setColumnMinimumWidth(i * 3 + 2, 30)

        self.setGeometry(300, 300, 400, 400)
        self.show()

    def solve_sudoku(self):
        empty_cell = find_empty(self.board)
        if not empty_cell:
            return True

        row, col = empty_cell

        for num in range(1, 10):
            if is_valid(self.board, row, col, num):
                self.board[row][col] = num
                self.gui_cells[row][col].setText(str(num))
                self.gui_cells[row][col].setStyleSheet("color: #aaffaa; border: 1px solid #cccccc;")
                QApplication.processEvents()
                QTimer.singleShot(50, lambda: None)
                time.sleep(self.timer)  # Added a small delay

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0
                self.gui_cells[row][col].setText("")
                self.gui_cells[row][col].setStyleSheet("color: red; border: 1px solid #cccccc;")
            else:
                self.gui_cells[row][col].setStyleSheet("color: red; border: 1px solid #cccccc;")
                QApplication.processEvents()
                QTimer.singleShot(50, lambda: None)
                time.sleep(self.timer)  # Added a small delay

        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku_board = read_sudoku_from_file("sudoku.txt")
    solver = SudokuSolver(sudoku_board)
    solver.solve_sudoku()
    sys.exit(app.exec_())