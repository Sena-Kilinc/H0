from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = []
        cols = []
        boxes = []
        steps = [0]

        for i in range(9):
            row_set = set()
            col_set = set()
            box_set = set()

            for j in range(1, 10):
                row_set.add(str(j))
                col_set.add(str(j))
                box_set.add(str(j))

            rows.append(row_set)
            cols.append(col_set)
            boxes.append(box_set)

        for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    num = int(board[i][j])
                    rows[i].remove(str(num))
                    cols[j].remove(str(num))
                    boxes[(i//3)*3+j//3].remove(str(num))
        
        print("Initial puzzle:")
        self.printBoard(board)
        print()

        self.backtrack(board, rows, cols, boxes, steps)

        print("Solution of Sudoku:")
        self.printBoard(board)

    def backtrack(self, board, rows, cols, boxes, steps, i=0, j=0):
        steps[0] += 1

        if i == 9:
            return True

        next_i = i+1 if j == 8 else i
        next_j = (j+1) % 9

        if board[i][j] != '.':
            return self.backtrack(board, rows, cols, boxes, steps, next_i, next_j)

        for num in rows[i] & cols[j] & boxes[(i//3)*3+j//3]:
            board[i][j] = str(num)
            rows[i].remove(str(num))
            cols[j].remove(str(num))
            boxes[(i//3)*3+j//3].remove(str(num))

            print("Step", steps[0])
            self.printBoard(board)

            if self.backtrack(board, rows, cols, boxes, steps, next_i, next_j):
                return True

            rows[i].add(str(num))
            cols[j].add(str(num))
            boxes[(i//3)*3+j//3].add(str(num))
            board[i][j] = '.'

        return False
    
    def printBoard(self, board: List[List[str]]) -> None:
        for row in board:
            print(row)
        print()
board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

solution= Solution()
solution.solveSudoku(board)