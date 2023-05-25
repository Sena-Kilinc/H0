import time
from queue import PriorityQueue

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

class Node:
    def __init__(self, state, g=0, parent=None):
        self.state = state
        self.g = g
        self.h = heuristic(state)
        self.parent = parent

    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f() < other.f()

def moves(state):
    i, j = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    possible_moves = []
    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if 0 <= i + di < 3 and 0 <= j + dj < 3:
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[i + di][j + dj] = new_state[i + di][j + dj], new_state[i][j]
            possible_moves.append(new_state)
    return possible_moves

def a_star(start):
    queue = PriorityQueue()
    queue.put((start.f(), start))
    visited = set()
    while not queue.empty():
        f, node = queue.get()
        if node.state == GOAL_STATE:
            path = []
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.append(start.state)
            return path[::-1]
        visited.add(tuple(map(tuple, node.state)))
        for move in moves(node.state):
            if tuple(map(tuple, move)) not in visited:
                child = Node(move, node.g + 1, node)
                queue.put((child.f(), child))

def solve_puzzle(start_state):
    start = Node(start_state)
    path = a_star(start)
    return path

def print_board(state):
    for i in range(3):
        for j in range(3):
            print(state[i][j], end=' ')
        print()

def main():
    start_state = [[1, 2, 3], [0, 7, 8], [4, 5, 6]]
    path = solve_puzzle(start_state)
    if path is not None:
        print("Solution found!")
        # Print the puzzle states
        for state in path:
            print_board(state)
            print()
            time.sleep(1)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
