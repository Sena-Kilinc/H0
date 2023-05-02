import time
import pygame
from queue import PriorityQueue

# Define constants
WIDTH = 200
HEIGHT = 200
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the goal state
GOAL_STATE = [[1, 2], [3, 0]]

# Define the heuristic function


def heuristic(state):
    distance = 0
    for i in range(2):
        for j in range(2):
            if state[i][j] != 0:
                x, y = divmod(state[i][j]-1, 2)
                distance += abs(x-i) + abs(y-j)
    return distance

# Define the node class


class Node:
    def __init__(self, state, g=0, parent=None):
        self.state = state
        self.g = g
        self.h = heuristic(state)
        self.parent = parent

    def f(self):
        return self.g + self.h

# Define the possible moves


def moves(state):
    i, j = next((i, j) for i in range(2) for j in range(2) if state[i][j] == 0)
    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if 0 <= i+di < 2 and 0 <= j+dj < 2:
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[i+di][j +
                                             dj] = new_state[i+di][j+dj], new_state[i][j]
            yield new_state

# Define the A* search algorithm


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
                child = Node(move, node.g+1, node)
                queue.put((child.f(), child))

# Define the puzzle solver function


def solve_puzzle(start_state):
    # Solve the puzzle
    start = Node(start_state)
    path = a_star(start)
    return path


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2x2 Sliding Puzzle")
clock = pygame.time.Clock()

# Define the tile class


class Tile:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, WIDTH//2, HEIGHT//2)
        self.value = value

    def draw(self, surface):
        if self.value == 0:
            pygame.draw.rect(surface, WHITE, self.rect)
        else:
            pygame.draw.rect(surface, GRAY, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 1)
            font = pygame.font.SysFont(None, 50)
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)


# Define the draw function


def draw_board(state):
    for i in range(2):
        for j in range(2):
            tile = Tile(j*WIDTH//2, i*HEIGHT//2, state[i][j])
            tile.draw(screen)


def main():
    # Define the initial state
    start_state = [[2, 3], [1, 0]]

    # Solve the puzzle
    path = solve_puzzle(start_state)

    # Animate the path
    for state in path:
        screen.fill(WHITE)
        draw_board(state)
        pygame.display.flip()
        time.sleep(1)  # Wait for 1 seconds before moving to the next step
        clock.tick(FPS)
    # Check if a solution was found
    if path:
        print("Solution found!")
    else:
        print("No solution found.")
    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == '__main__':
    main()
