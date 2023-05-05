import pygame
from typing import List


class Solution:
    '''
    This is the constructor of the Solution class that initializes the instance variables self.board, self.rows, self.cols, self.boxes, and self.steps.
    Time complexity: O(81), which is constant.
    Space complexity: O(27), which is also constant.
    '''
    # define a function to solve Sudoku problem that takes in 2D list of strings and returns None

    def __init__(self, board: List[List[str]]):
        self.board = board
        self.rows = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.cols = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.boxes = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.steps = [0]
    '''
    This method solves the Sudoku puzzle using backtracking algorithm, and updates the board for every step using Pygame library. It calls the backtrack() function recursively to solve the puzzle.
    Time complexity: O(9^(n*n)), where n is the size of the Sudoku puzzle (n=9 for the standard Sudoku puzzle), because in the worst case, the algorithm has to try all possible combinations of numbers for every empty cell in the board.
    Space complexity: O(n*n), because the algorithm uses a recursive stack to keep track of the current cell being filled.
    '''
    # This is the beginning of the solveSudoku method, which is defined inside a class. The method takes no arguments besides the self parameter, which refers to the instance of the class.

    def solveSudoku(self):
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
        '''
        This function implements the backtracking algorithm to solve the Sudoku puzzle recursively. It takes two optional parameters i and j that represent the current row and column being filled in the board. It updates the self.board and self.steps instance variables for every step.
        Time complexity: O(9^(n*n)), where n is the size of the Sudoku puzzle (n=9 for the standard Sudoku puzzle), because in the worst case, the algorithm has to try all possible combinations of numbers for every empty cell in the board.
        Space complexity: O(n*n), because the algorithm uses a recursive stack to keep track of the current cell being filled.
        
        '''
        def backtrack(i=0, j=0):  # This method is defined with two parameters i and j both of which have default values of 0.
            # Increments the first value in self.steps by 1. The self.steps list is used to keep track of the number of steps taken to solve the puzzle.
            self.steps[0] += 1

            if i == 9:  # If the value of i is equal to 9, that means we have reached the end of the puzzle and return True.
                return True
            # The values of next_i and next_j are calculated based on the values of i and j. If j is 8, next_i will be i+1 to move to the next row, otherwise it will be the same as i. next_j is calculated using the modulus operator, which ensures that j stays within the bounds of the puzzle
            next_i = i+1 if j == 8 else i
            next_j = (j+1) % 9

            # If the value at self.board[i][j] is not '.', that means it is already filled and we move to the next cell by calling backtrack(next_i, next_j) recursively.
            if self.board[i][j] != '.':
                return backtrack(next_i, next_j)
            # This loop iterates over the intersection of self.rows[i], self.cols[j], and self.boxes[(i//3)*3+j//3], which contains all the possible numbers that can be placed in the cell (i,j). It then places each number in the cell, removes it from the corresponding row, column, and box, and then proceeds to the next cell.
            for num in self.rows[i] & self.cols[j] & self.boxes[(i//3)*3+j//3]:
                self.board[i][j] = str(num)
                self.rows[i].remove(str(num))
                self.cols[j].remove(str(num))
                self.boxes[(i//3)*3+j//3].remove(str(num))

                # Pygame: Draw the updated board for every step
                self.draw_board()
                pygame.display.update()
                pygame.time.delay(0)

                # This calls backtrack recursively on the next cell and returns True if a solution is found
                if backtrack(next_i, next_j):
                    return True
                # If no solution is found, this code adds the previously removed number back to the row, column, and box, and clears the cell (i,j) for the next iteration.
                self.rows[i].add(str(num))
                self.cols[j].add(str(num))
                self.boxes[(i//3)*3+j//3].add(str(num))
                self.board[i][j] = '.'
            # Returns False if no solution is found.
            return False
        # which solves the Sudoku puzzle using backtracking algorithm recursively. If the algorithm finds a solution, it returns True, otherwise it returns False. This line essentially starts the solving process by calling the backtrack() function with default values for the i and j parameters, which are both set to 0 initially.
        backtrack()
    '''
    This method draws the Sudoku board on the Pygame screen for every step in the backtracking algorithm.
    Time complexity: O(n*n), where n is the size of the Sudoku puzzle (n=9 for the standard Sudoku puzzle), because it has to iterate over every cell in the board to draw it on the screen.
    Space complexity: O(1), because it uses a fixed amount of memory to draw the board on the screen.
    '''
    # This line defines a method called draw_board that belongs to a class

    def draw_board(self):
        # These two lines start a nested loop that will iterate over each cell in a 9x9 grid.
        for i in range(9):
            for j in range(9):
                # These two lines use Pygame to draw a white rectangle (with a black border) for each cell in the grid. The first line draws a filled rectangle, and the second line draws a rectangle with a border.
                pygame.draw.rect(screen, (255, 255, 255), (j*50, i*50, 50, 50))
                pygame.draw.rect(screen, (0, 0, 0), (j*50, i*50, 50, 50), 1)
                # These lines draw the text for each cell in the grid. If the cell contains a number (represented by a string), then it is rendered using a Pygame font. The text is centered within the cell and drawn onto the screen.
                if self.board[i][j] != '.':
                    font = pygame.font.Font(None, 40)
                    text = font.render(self.board[i][j], True, (0, 0, 0))
                    text_rect = text.get_rect(center=(j*50+25, i*50+25))
                    screen.blit(text, text_rect)


# Pygame: Initialize
pygame.init()
# This sets the size of the window and creates a window with the specified size. It also sets the caption of the window to "Sudoku Solver".
size = (450, 450)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku Solver")
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

    # Pygame: Fill the screen with white color
    screen.fill((255, 255, 255))

    # Pygame: Draw the solved board
    solution.draw_board()

    # Pygame: Update the screen
    pygame.display.update()

# Pygame: Quit
pygame.quit()

# This prints the number of steps taken by the algorithm to solve the Sudoku puzzle.
print("Number of steps taken:", solution.steps[0])
