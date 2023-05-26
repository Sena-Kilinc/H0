'''
This project presents a solution to the Sudoku Solver problem. 
The program is designed to fill empty cells in complex Sudoku puzzles.
By strictly adhering to the fundamental rules of Sudoku, the project ensures that 
Each digit from 1 to 9 is precisely and uniquely placed in every row, column, and 3x3 sub-box of the grid.
@ Sena Kılınç 20191701033
'''
from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        '''
        This method solves the Sudoku puzzle using backtracking algorithm.
        This method also make sures that the same number doesn't appear twice in the same row, column, or box.   
        Time Complexity: O(9^(n^2)) Exponential. The number of possible combinations for each cell is 9, and there are a total of n^2 cells on the Sudoku board. 
        Space Complexity: O(n^2) Quadratic.
        '''
        rows = [] # Initialize an empty list for rows
        cols = [] # Initialize an empty list for columns
        boxes = [] # Initialize an empty list for boxes
        steps = [0] # Initialize a list with a single element, 0, for steps

        for i in range(9): # Populate the rows, cols, and boxes lists
            row_set = set() # Create an empty set for each row
            col_set = set() # Create an empty set for each column
            box_set = set() # Create an empty set for each box
            
            for j in range(1, 10):# Populate each set with numbers 1 to 9 as strings
                row_set.add(str(j)) # Add the number to the row set
                col_set.add(str(j)) # Add the number to the column set
                box_set.add(str(j)) # Add the number to the box set
            # Append the populated sets to the respective lists
            rows.append(row_set) # Append the row set to the rows list
            cols.append(col_set) # Append the column set to the cols list
            boxes.append(box_set) # Append the box set to the boxes list
        # These two for loops iterate over each cell in the 9x9 Sudoku board.
        for i in range(9):
            for j in range(9):
                # This if statement checks whether the current cell is already filled in or not. If it's not empty (i.e., it contains a number), the code inside the if block is executed.                
                if board[i][j] != '.':
                    num = int(board[i][j]) # This line converts the string representation of the number in the current cell to an integer.
                    # These three lines remove the number that was just placed in the current cell from the corresponding sets of possible values for the row, column, and 3x3 box that contain the cell.                 
                    rows[i].remove(str(num))
                    cols[j].remove(str(num))
                    boxes[(i//3)*3+j//3].remove(str(num)) # calculate index of the set in boxes and remove the number that was just placed
        
        print("Initial puzzle:")
        self.printBoard(board) # Print the initial puzzle board
        print()

        self.backtrack(board, rows, cols, boxes, steps) # Start the Sudoku-solving recursion

        print("Solution of Sudoku:") # Print the solution board
        self.printBoard(board)

    def backtrack(self, board, rows, cols, boxes, steps, i=0, j=0):
        '''
        This function implements the backtracking algorithm to solve the Sudoku puzzle recursively. 
        It takes two optional parameters i and j that represent the current row and column being filled in the board. It updates the self.board and self.steps instance variables for every step.
        Time Complexity: O(9^(n^2)) Exponential. The number of possible combinations for each cell is 9, and there are a total of n^2 cells on the Sudoku board. 
        Space Complexity: O(n^2) Quadratic.
        '''
        steps[0] += 1 # Increase to keep track of the number of steps taken to solve the puzzle

        if i == 9: # If the value of i is equal to 9, that means we have reached the end of the puzzle and return True.
            return True

        nextRow = i+1 if j == 8 else i # If j is 8, nextRow will be i+1 to move to the next row, otherwise it will be the same as i.
        nextColumn = (j+1) % 9  # nextColumn is calculation ensures that j stays within the bounds of the puzzle
        # If the value at self.board[i][j] is not '.', that means it is already filled and we move to the next cell by calling backtrack(nextRow, nextColumn) recursively.
        if board[i][j] != '.':
            return self.backtrack(board, rows, cols, boxes, steps, nextRow, nextColumn)
        
        # This loop iterates over the intersection of self.rows[i], self.cols[j], and self.boxes[(i//3)*3+j//3], which contains all the possible numbers that can be placed in the cell (i,j).
        for num in rows[i] & cols[j] & boxes[(i//3)*3+j//3]:
            board[i][j] = str(num) # It then places each number in the cell
            rows[i].remove(str(num)) # Removes it from the corresponding row
            cols[j].remove(str(num)) # Removes it from the corresponding column
            boxes[(i//3)*3+j//3].remove(str(num)) # Removes it from the corresponding box

            print("Step", steps[0])
            self.printBoard(board) # print on the board

            # This calls backtrack recursively on the next cell and returns True if a solution is found
            if self.backtrack(board, rows, cols, boxes, steps, nextRow, nextColumn):
                return True
            # If no solution is found, this code adds the previously removed number back to the row, column, and box, and clears the cell (i,j) for the next iteration.
            rows[i].add(str(num)) # Adding back to row
            cols[j].add(str(num)) # Adding back to column
            boxes[(i//3)*3+j//3].add(str(num)) # Adding back to box
            board[i][j] = '.' # clears the cell 
         # Returns False if no solution is found.
        return False
    
    def printBoard(self, board: List[List[str]]) -> None:
        '''
        The function iterates through each cell in the board once to print its value.
        Time Complexity: O(n) Linear.
        Space Complexity: O(1) Constant.
        '''
        for row in board:
            print(row)
        print()

# Initialize Sudoku board with a given puzzle.
board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

# This creates an instance of the Solution class with the given board and solves the Sudoku puzzle.
solution= Solution()
solution.solveSudoku(board) # to 