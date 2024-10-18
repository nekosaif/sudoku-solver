# Sudoku Solver with PyQt5

This is a graphical Sudoku solver built using **PyQt5** and the **backtracking algorithm**. The solver reads a Sudoku puzzle from a text file, displays it in a 9x9 grid, and visually solves it step-by-step. The program updates the grid in real-time, showing the progress of the algorithm, including valid and invalid moves (with a backtracking mechanism).

## Features

- **Graphical Interface**: Displays the Sudoku board in a GUI using PyQt5.
- **Step-by-Step Solving**: Shows each step of the solving process, including the placement of numbers and backtracking.
- **Backtracking Algorithm**: Implements the standard backtracking algorithm to solve the puzzle.
- **Real-time Visualization**: Visual feedback with color coding for valid and invalid moves:
  - **Green** for valid placements
  - **Red** for backtracked invalid moves
  - **Orange (•)** for empty cells

## How It Works

1. **Input**: The Sudoku board is read from a text file (`sudoku.txt`), where:
   - Each line represents a row of the board.
   - Numbers are separated by spaces.
   - Empty cells are represented by `0`.
   
2. **Algorithm**: The solver uses a backtracking algorithm:
   - It fills empty cells (starting from the top-left) by trying numbers from 1 to 9.
   - If a number is valid according to Sudoku rules (row, column, and 3x3 subgrid), it is placed.
   - If the board reaches an invalid state, the algorithm backtracks by removing numbers and trying other possibilities.
   
3. **Visualization**: The GUI shows each step, updating the board in real-time:
   - Valid placements turn **green**.
   - Backtracked invalid moves turn **red**.
   - Empty cells are marked with an **orange dot** (`•`).

## Prerequisites

To run the project, you'll need to install **PyQt5**. Use the following command to install it:

```bash
pip install pyqt5
```
