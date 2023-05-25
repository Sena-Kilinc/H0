'''
This project presents a solution to the Sudoku Solver problem. 
The program is designed to fill empty cells in complex Sudoku puzzles.
By strictly adhering to the fundamental rules of Sudoku, the project ensures that 
Each digit from 1 to 9 is precisely and uniquely placed in every row, column, and 3x3 sub-box of the grid.
@ Sena Kılınç 20191701033
'''

import pygame
from typing import List


class Solution:
    #The Solution class represents a Sudoku solver

    def __init__(self, board: List[List[str]]):
        '''
        This is the constructor of the Solution class that initializes the instance variables self.board, self.rows, self.cols, self.boxes, and self.steps.
        Time complexity: O(1)
        The time complexity is constant because the number of operations performed is fixed and independent of the size of the input board.

        Space complexity: O(1)
        The space complexity is constant because the amount of additional space used is fixed and does not depend on the size of the input board.
        '''
        self.board = board
        self.rows = []     # Initialize an empty list for rows
        self.cols = []     # Initialize an empty list for columns
        self.boxes = []    # Initialize an empty list for boxes
        self.steps = [0]   # Initialize a list with a single element, 0, for steps

        # Populate the rows, cols, and boxes lists
        for i in range(9):
            row_set = set()     # Create an empty set for each row
            col_set = set()     # Create an empty set for each column
            box_set = set()     # Create an empty set for each box

            # Populate each set with numbers 1 to 9 as strings
            for j in range(1, 10):
                row_set.add(str(j))     # Add the number to the row set
                col_set.add(str(j))     # Add the number to the column set
                box_set.add(str(j))     # Add the number to the box set

            # Append the populated sets to the respective lists
            self.rows.append(row_set)   # Append the row set to the rows list
            self.cols.append(col_set)   # Append the column set to the cols list
            self.boxes.append(box_set)  # Append the box set to the boxes list
    
    def solveSudoku(self):
        '''
        This method solves the Sudoku puzzle using backtracking algorithm, and updates the board for every step using Pygame library. 
        It calls the backtrack() function recursively to solve the puzzle.
        Time complexity: O(9^(n*n)) exponential , where n is the size of the Sudoku puzzle (n=9), because in the worst case, the algorithm has to try all possible combinations of numbers for every empty cell in the board. 
        Space complexity: O(n^2) quadratic, because the algorithm uses a recursive stack to keep track of the current cell being filled.
        '''
        # These two for loops iterate over each cell in the 9x9 Sudoku board.
        for i in range(9):
            for j in range(9):
                # This if statement checks whether the current cell is already filled in or not. If it's not empty (i.e., it contains a number), the code inside the if block is executed.
                if self.board[i][j] != '.':
                    # This line converts the string representation of the number in the current cell to an integer.
                    num = int(self.board[i][j])
                    # These three lines remove the number that was just placed in the current cell from the corresponding sets of possible values for the row, column, and 3x3 box that contain the cell. This is done to ensure that the same number doesn't appear twice in the same row, column, or box.
                    self.rows[i].remove(str(num))
                    self.cols[j].remove(str(num))
                    # calculate index of the set in boxes.
                    self.boxes[(i//3)*3+j//3].remove(str(num))
                    # (i//3)*3 rounds down the row index i to the nearest multiple of 3,
                    # and adds j//3 to calculate the column offset within that row
        # solves the Sudoku puzzle using backtracking algorithm recursively. If the algorithm finds a solution, it returns True, otherwise it returns False. This line essentially starts the solving process by calling the backtrack() function with default values for the i and j parameters, which are both set to 0 initially.
        if self.backtrack():
            print("Solution found!")
        else:
            print("No solution found.")
        
    def backtrack(self,i=0, j=0): 
        '''
        This function implements the backtracking algorithm to solve the Sudoku puzzle recursively. It takes two optional parameters i and j that represent the current row and column being filled in the board. It updates the self.board and self.steps instance variables for every step.
        Time complexity: O(9^(n*n)) exponential, where n is the size of the Sudoku puzzle (n=9 for the standard Sudoku puzzle), because in the worst case, the algorithm has to try all possible combinations of numbers for every empty cell in the board.
        Space complexity: O(n^2) quadratic, because the algorithm uses a recursive stack to keep track of the current cell being filled.
        
        '''
        # Increments the first value in self.steps by 1. The self.steps list is used to keep track of the number of steps taken to solve the puzzle.
        self.steps[0] += 1

        if i == 9:  # If the value of i is equal to 9, that means we have reached the end of the puzzle and return True.
            return True
        # The values of nextRow and nextColumn are calculated based on the values of i and j.  
        nextRow = i+1 if j == 8 else i # If j is 8, nextRow will be i+1 to move to the next row, otherwise it will be the same as i.
        nextColumn = (j+1) % 9 # nextColumn is calculation ensures that j stays within the bounds of the puzzle

        # If the value at self.board[i][j] is not '.', that means it is already filled and we move to the next cell by calling backtrack(nextRow, nextColumn) recursively.
        if self.board[i][j] != '.':
            return self.backtrack(nextRow, nextColumn)
        # This loop iterates over the intersection of self.rows[i], self.cols[j], and self.boxes[(i//3)*3+j//3], which contains all the possible numbers that can be placed in the cell (i,j).
        
        for num in self.rows[i] & self.cols[j] & self.boxes[(i//3)*3+j//3]:
            self.board[i][j] = str(num)# It then places each number in the cell
            self.rows[i].remove(str(num)) # Removes it from the corresponding row,
            self.cols[j].remove(str(num)) # Removes it from the corresponding column
            self.boxes[(i//3)*3+j//3].remove(str(num)) #Removes it from the corresponding box

            # Pygame: Draw the updated board for every step
            self.draw_board()
            pygame.display.update()
            pygame.time.delay(0) # to program not to pause

            # This calls backtrack recursively on the next cell and returns True if a solution is found
            if self.backtrack(nextRow, nextColumn):
                return True
            # If no solution is found, this code adds the previously removed number back to the row, column, and box, and clears the cell (i,j) for the next iteration.
            self.rows[i].add(str(num)) # Adding back to row
            self.cols[j].add(str(num)) # Adding back to column
            self.boxes[(i//3)*3+j//3].add(str(num)) # Adding back to box
            self.board[i][j] = '.' # clears the cell 
        # Returns False if no solution is found.
        return False

    def draw_board(self):
        '''
        This method draws the Sudoku board on the Pygame screen for every step in the backtracking algorithm.
        Time complexity: O(n^2) quadratic, where n is the size of the Sudoku puzzle (n=9 for the standard Sudoku puzzle), because it has to iterate over every cell in the board to draw it on the screen.
        Space complexity: O(1), because it uses a fixed amount of memory to draw the board on the screen.
        '''
        # These two lines start a nested loop that will iterate over each cell in a 9x9 grid.
        for i in range(9):
            for j in range(9):
                # These two lines use Pygame to draw a white rectangle (with a black border) for each cell in the grid
                pygame.draw.rect(screen, (255, 255, 255), (j*50, i*50, 50, 50)) # Draws a filled white rectangle
                pygame.draw.rect(screen, (0, 0, 0), (j*50, i*50, 50, 50), 1) # Draws a rectangle with a black border
                # These lines draw the text for each cell in the grid.  
                if self.board[i][j] != '.': # If the cell contains a number (represented by a string),
                    font = pygame.font.Font(None, 40) 
                    text = font.render(self.board[i][j], True, (0, 0, 0)) # Rendered using a Pygame font.
                    text_rect = text.get_rect(center=(j*50+25, i*50+25)) # Centered within the cell 
                    screen.blit(text, text_rect) # Drawn into the screen

pygame.init() # Pygame is initializez

size = (450, 450) 
screen = pygame.display.set_mode(size) # This sets the size of the window and creates a window with the specified size
pygame.display.set_caption("Sudoku Solver") # Sets the caption of the window to "Sudoku Solver"
# This initializes the Sudoku board with a given puzzle.
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
solution = Solution(board)
solution.solveSudoku()
# This starts the Pygame event loop, which listens for events like keyboard and mouse input. It continues running until the user closes the window.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255)) # Fill the screen with white color
    solution.draw_board() # Draw the solved board
    pygame.display.update() # Update the screen

pygame.quit()# Quit from the game

# This prints the number of steps taken by the algorithm to solve the Sudoku puzzle.
print("Number of steps taken:", solution.steps[0])
