def solve_n_queens(n):
    # Create an empty board
    board = [['-' for i in range(n)] for j in range(n)]

    def is_safe(row, col):
        # Check if the given position is safe for a queen
        for i in range(n):
            if board[i][col] == 'Q':  # Check column
                return False
            if board[row][i] == 'Q':  # Check row
                return False
            # Check upper left diagonal
            if (row-i >= 0 and col-i >= 0 and board[row-i][col-i] == 'Q'):
                return False
            # Check upper right diagonal
            if (row-i >= 0 and col+i < n and board[row-i][col+i] == 'Q'):
                return False
        return True

    def solve_backtracking(row):
        if row == n:  # Base case: all queens are placed
            return True
        for col in range(n):  # Try all columns in the current row
            if is_safe(row, col):
                board[row][col] = 'Q'
                if solve_backtracking(row+1):  # Recursively solve the next row
                    return True
                board[row][col] = '-'  # Backtrack
        return False

    # Start with the first row
    solve_backtracking(0)

    # Print the board as a table
    for row in board:
        print('|' + '|'.join(row) + '|')


solve_n_queens(5)
