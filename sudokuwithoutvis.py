from typing import List


class Solution:
    # The Solution class represents a Sudoku solver

    def __init__(self, board: List[List[str]]):
        self.board = board
        self.rows = []
        self.cols = []
        self.boxes = []
        self.steps = [0]

        for i in range(9):
            row_set = set()
            col_set = set()
            box_set = set()

            for j in range(1, 10):
                row_set.add(str(j))
                col_set.add(str(j))
                box_set.add(str(j))

            self.rows.append(row_set)
            self.cols.append(col_set)
            self.boxes.append(box_set)

    def backtrack(self, i=0, j=0):
        self.steps[0] += 1

        if i == 9:
            return True

        nextRow = i + 1 if j == 8 else i
        nextColumn = (j + 1) % 9

        if self.board[i][j] != '.':
            return self.backtrack(nextRow, nextColumn)

        for num in self.rows[i] & self.cols[j] & self.boxes[(i // 3) * 3 + j // 3]:
            if self.available(i, j, num):
                self.board[i][j] = str(num)
                self.rows[i].remove(str(num))
                self.cols[j].remove(str(num))
                self.boxes[(i // 3) * 3 + j // 3].remove(str(num))
                
                print("Step", self.steps[0])
                self.printBoard()

                if self.backtrack(nextRow, nextColumn):
                    return True

                self.rows[i].add(str(num))
                self.cols[j].add(str(num))
                self.boxes[(i // 3) * 3 + j // 3].add(str(num))
                self.board[i][j] = '.'

        return False

    def available(self, row, col, num):
        for c in range(9):
            if self.board[row][c] == num:
                return False

        for r in range(9):
            if self.board[r][col] == num:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        return True

    def printBoard(self):
        for row in self.board:
            print(row)
        print()

# Example puzzle
board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]

solution = Solution(board)

print("Initial puzzle:")
solution.printBoard()
print()

solution.backtrack()

# Print the solved Sudoku board
print("Solution of Sudoku:")
solution.printBoard()

# Print the number of steps taken
print("Number of steps taken:", solution.steps[0])
