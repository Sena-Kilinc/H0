import time
import pygame
from queue import PriorityQueue
WIDTH = 300
HEIGHT = 300
FPS = 60
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j]-1, 3)
                distance += abs(x-i) + abs(y-j)
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
    i, j = next((i, j) for i in range(3) for j in range(
        3) if state[i][j] == 0)
    possible_moves = []
    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        if 0 <= i+di < 3 and 0 <= j+dj < 3:
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[i+di][j +
                                             dj] = new_state[i+di][j+dj], new_state[i][j]
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
                child = Node(move, node.g+1, node)
                queue.put((child.f(), child))
def solve_puzzle(start_state):
    start = Node(start_state)
    path = a_star(start)
    return path
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3x3 Sliding Puzzle")
clock = pygame.time.Clock()
class Tile:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, WIDTH//3, HEIGHT//3)
        self.value = value

    def draw(self, surface):
        if self.value == 0:
            color = WHITE
        else:
            color = GRAY
            pygame.draw.rect(surface, BLACK, self.rect, 1)
        pygame.draw.rect(surface, color, self.rect)
        if self.value != 0:
            font = pygame.font.SysFont(None, 50)
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
def draw_board(state):
    for i in range(3):
        for j in range(3):
            tile = Tile(j*WIDTH//3, i*HEIGHT//3, state[i][j])
            tile.draw(screen)
def main():
    start_state = [[1, 2, 3], [0, 7, 8], [4, 5, 6], ]
    path = solve_puzzle(start_state)
    if path is not None:
        print("Solution found!")
        # Draw the puzzle
        for state in path:
            draw_board(state)
            pygame.display.update()
            time.sleep(1)
    else:
        print("No solution found.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
if __name__ == '__main__':
    main()