import pygame
from typing import List


class Solution:
    def __init__(self, board: List[List[str]]):
        self.board = board
        self.rows = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.cols = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.boxes = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        self.steps = [0]

    def solveSudoku(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != '.':
                    num = int(self.board[i][j])
                    self.rows[i].remove(str(num))
                    self.cols[j].remove(str(num))
                    self.boxes[(i//3)*3+j//3].remove(str(num))

        def backtrack(i=0, j=0):
            self.steps[0] += 1

            if i == 9:
                return True

            next_i = i+1 if j == 8 else i
            next_j = (j+1) % 9

            if self.board[i][j] != '.':
                return backtrack(next_i, next_j)

            for num in self.rows[i] & self.cols[j] & self.boxes[(i//3)*3+j//3]:
                self.board[i][j] = str(num)
                self.rows[i].remove(str(num))
                self.cols[j].remove(str(num))
                self.boxes[(i//3)*3+j//3].remove(str(num))

                # Pygame: Draw the updated board for every step
                self.draw_board()
                pygame.display.update()
                pygame.time.delay(0)

                if backtrack(next_i, next_j):
                    return True

                self.rows[i].add(str(num))
                self.cols[j].add(str(num))
                self.boxes[(i//3)*3+j//3].add(str(num))
                self.board[i][j] = '.'

            return False

        backtrack()

    def draw_board(self):
        # Pygame: Draw the board
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, (255, 255, 255), (j*50, i*50, 50, 50))
                pygame.draw.rect(screen, (0, 0, 0), (j*50, i*50, 50, 50), 1)
                if self.board[i][j] != '.':
                    font = pygame.font.Font(None, 40)
                    text = font.render(self.board[i][j], True, (0, 0, 0))
                    text_rect = text.get_rect(center=(j*50+25, i*50+25))
                    screen.blit(text, text_rect)


# Pygame: Initialize
pygame.init()
size = (450, 450)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku Solver")

board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

solution = Solution(board)
solution.solveSudoku()
# Pygame: Event loop
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
