from typing import List


class Solution:
    # define a function to solve Sudoku problem that takes in 2D list of strings and returns None
    def solveSudoku(self, board: List[List[str]]) -> None:
        # create sets of numbers 1 through 9 for each row, column and boxes
        rows = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        cols = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        boxes = [set(str(i) for i in range(1, 10)) for _ in range(9)]
        steps = [0]  # initialize step counter

        # iterate through the board
        for i in range(9):
            for j in range(9):
                # if cell is not empty then remove its value from the corresponding row column and box sets
                if board[i][j] != '.':
                    num = int(board[i][j])
                    rows[i].remove(str(num))
                    cols[j].remove(str(num))
                    # calculate index of the set in boxes.
                    boxes[(i//3)*3+j//3].remove(str(num))
                    # (i//3)*3 rounds down the row index i to the nearest multiple of 3,
                    # and adds j//3 to calculate the column offset within that row

    # define a recursive function to backtrack and solve the Sudoku puzzle
        def backtrack(board, i=0, j=0):
            steps[0] += 1  # increment step counter

            # if we reach the end of the board, return True
            if i == 9:
                return True
          # compute the indices of the next cell to fill
            # checks if we are at the end of a row  (i.e., column index is 8)
            next_i = i+1 if j == 8 else i
            # If we are at the end of the row, it moves to the next row by incrementing i by 1.
            # Otherwise, next_i remains the same as i.
            # This ensures that if j is at the end of a row (i.e., it is 8), the value of next_j will be 0, which corresponds to the first column of the next row.
            next_j = (j+1) % 9
            # If j is not at the end of the row, next_j will be the next column in the same row.

            # if the current cell is not empty, move on to the next cell
            if board[i][j] != '.':
                return backtrack(board, next_i, next_j)

        # try all possible values for the current cell that satisfy the constraints
            for num in rows[i] & cols[j] & boxes[(i//3)*3+j//3]:
                # fill the current cell with the value num
                board[i][j] = str(num)
                # remove num from the corresponding row, column, and box sets
                rows[i].remove(str(num))
                cols[j].remove(str(num))
                boxes[(i//3)*3+j//3].remove(str(num))
                # recursively call backtrack to fill the next cell
                if backtrack(board, next_i, next_j):
                    return True
                # if we can't find a solution, backtrack by adding the removed value back to the sets
                rows[i].add(str(num))
                cols[j].add(str(num))
                boxes[(i//3)*3+j//3].add(str(num))
                # reset the current cell to empty
                board[i][j] = '.'
            # if we've tried all possible values and haven't found a solution, return False
            return False
    # call the backtrack function on the input board to solve the Sudoku puzzle
        backtrack(board)
        print("Number of steps:", steps[0])


board = [["5", "3", ".", ".", "7", ".", ".", ".", "."],
         ["6", ".", ".", "1", "9", "5", ".", ".", "."],
         [".", "9", "8", ".", ".", ".", ".", "6", "."],
         ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
         ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
         ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
         [".", "6", ".", ".", ".", ".", "2", "8", "."],
         [".", ".", ".", "4", "1", "9", ".", ".", "5"],
         [".", ".", ".", ".", "8", ".", ".", "7", "9"]]

Solution().solveSudoku(board)

for row in board:
    print(row)

"""
Solution:
We can solve this problem by using the backtracking algorithm. We will fill the Sudoku board row by row, and for each empty cell, we will try all the possible digits that can be placed in that cell. If we find a digit that satisfies the Sudoku rules, we will move on to the next empty cell. If we cannot find a digit that satisfies the rules, we will backtrack and try a different digit for the previous empty cell.

We can represent the Sudoku board as a 2D list of characters. We will define a helper function that takes the current row and column and returns True if we can place a digit in that cell that satisfies the Sudoku rules, and False otherwise. This function will check the current row, current column, and current 3x3 sub-box to see if the digit we are trying to place already exists in any of these locations.

Then, we will define the main function that will use the backtracking algorithm to fill the Sudoku board. The main function will iterate over each cell in the board, and if the cell is empty, it will try to place a digit in that cell. If the digit placement is successful, it will move on to the next cell. If the digit placement is not successful, it will backtrack and try a different digit for the previous cell

To solve the Sudoku problem efficiently, we can use the backtracking algorithm with constraint propagation techniques. This algorithm recursively tries digits in the empty cells until a valid solution is found or all possibilities are exhausted. Constraint propagation techniques are used to reduce the search space by eliminating impossible values for cells based on the constraints of the puzzle.

The time complexity of the backtracking algorithm is exponential, but we can reduce the search space by using constraint propagation techniques. One such technique is called "elimination," where we eliminate possible values for cells based on the constraints of the puzzle.
The algorithm first creates sets for the rows, columns, and boxes, containing all possible digits for each. It then eliminates digits based on the existing values in the board. The backtrack function recursively tries digits for each empty cell until a valid solution is found or all possibilities are exhausted. It first checks if the current cell is already filled, and if so, moves on to the next cell. Otherwise, it tries all possible digits for the current cell that satisfy the constraints of the puzzle. If a digit leads to a valid solution, the algorithm returns True, and the puzzle is solved. Otherwise, the algorithm backtracks and tries a different digit until all possibilities are exhausted.

Using the constraint propagation techniques reduces the search space and allows the algorithm to find the solution faster. The time complexity of the algorithm depends on the number of empty cells in the puzzle, with a worst-case time complexity of O(9^(n^2)) for a completely empty puzzle. However, in practice, the algorithm can solve most Sudoku puzzles quickly, even those with only a few empty cells.
The solveSudoku function takes a partially-filled Sudoku board as input and attempts to fill in the remaining empty cells with valid values. The function uses a combination of constraint propagation and backtracking search to achieve this.

Constraint Propagation:

The algorithm starts by initializing three sets, rows, cols, and boxes, each containing the digits 1 to 9. These sets represent the possible digits that can be placed in each row, column, and box of the Sudoku board.

Next, the algorithm loops over each cell of the input board, and if the cell is not empty (i.e., contains a digit), it removes that digit from the corresponding row, column, and box sets. This step is a form of constraint propagation since it narrows down the possible values that can be placed in the empty cells based on the values that have already been placed in the board.

Backtracking Search:

After the constraint propagation step, the algorithm starts the backtracking search by calling the backtrack function. This function takes the partially-filled board as input and a set of indices i and j that represent the current cell being filled.

The backtrack function uses a recursive depth-first search to try out different values in the current cell and move on to the next cell. For each empty cell, it tries out all possible values that are valid based on the remaining values in the corresponding row, column, and box sets.

If a valid value is found for the current cell, the function updates the corresponding row, column, and box sets to reflect the new value, and then moves on to the next empty cell. If no valid value is found for the current cell, the function backtracks to the previous cell and tries a different value.

If the algorithm successfully fills in all empty cells, it returns True, indicating that a valid solution has been found. Otherwise, it returns False, indicating that no solution was found.

Printing the Result:

Finally, after the solveSudoku function completes, the resulting board is printed out using a simple for loop that prints each row of the board on a separate line.

Here's what each line of the code does:

from typing import List: This line imports the List data type from the typing module. It is used later to define the input parameter type for the solveSudoku function.

class Solution:: This line defines a class named Solution.

def solveSudoku(self, board: List[List[str]]) -> None:: This line defines a method named solveSudoku that takes in a 2D list of strings (board) and returns None. The self parameter refers to the instance of the class.

5-7. These lines initialize 3 sets of digits (1-9) to represent the possible values for each row, column, and box. They are stored in rows, cols, and boxes, respectively.

9-12. These lines iterate through the entire board and remove any existing numbers from the corresponding row, column, and box sets.

14-31. This is the main recursive function that solves the Sudoku puzzle using backtracking. It takes in the current board state and the current i and j indices. If i is equal to 9, it means the function has reached the end of the board and returns True.

The function first calculates the next indices (next_i and next_j) depending on the current indices. If the current cell already has a number, it moves to the next cell.

Otherwise, it loops through the intersection of the possible values for the current cell's row, column, and box sets. For each possible value, it updates the board, removes the value from the corresponding sets, and recursively calls the function with the updated board and indices.

If the function returns True, it means a solution has been found, so the function returns True to the previous call. Otherwise, it backtracks by restoring the previous state of the board and the sets and moves on to the next possible value.

32-36. If the function reaches this point, it means there is no solution, so it returns False.

38-53. This code initializes the input board and solves it using the solveSudoku method of the Solution class. Then, it prints the board line by line to display the solved Sudoku puzzle.

"""
