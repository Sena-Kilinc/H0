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

        def backtrack(i=0, j=0):
            self.steps[0] += 1

            if i == 9:
                return True

            # Create a dictionary to store the number of remaining values for each empty cell
            values = {}
            for x in range(9):
                for y in range(9):
                    if self.board[x][y] == '.':
                        values[(x, y)] = len(self.rows[x] &
                                             self.cols[y] & self.boxes[(x//3)*3+y//3])

            # Sort the empty cells on the board by the number of remaining values
            cells = sorted(values, key=values.get)

            for cell in cells:
                x, y = cell

                for num in self.rows[x] & self.cols[y] & self.boxes[(x//3)*3+y//3]:
                    self.board[x][y] = str(num)
                    self.rows[x].remove(str(num))
                    self.cols[y].remove(str(num))
                    self.boxes[(x//3)*3+y//3].remove(str(num))

                    if backtrack(*cell):
                        return True

                    # Restore the state of the board
                    self.board[x][y] = '.'
                    self.rows[x].add(str(num))
                    self.cols[y].add(str(num))
                    self.boxes[(x//3)*3+y//3].add(str(num))

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
