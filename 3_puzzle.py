'''
This project solves 8-Puzzle Game using A* Search Algorithm.
The game is 3x3 sliding puzzle and to reach the goal state
the program must rearrange the tiles in order as:
1 2 3
4 5 6
7 8 0
@ Sena Kılınç 20191701033
'''
import time
import pygame
from queue import PriorityQueue

# Constants for visual presentation of the game.
WIDTH = 600
HEIGHT = 600
FPS = 60

# Colors for visual presentation of the game.
WHITE = (255, 250, 240)
BLACK = (0, 0, 0)
GREEN = (69, 139, 116)

# The goal state for the game as 2D List
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


def heuristicManhattan(state):
    '''
    This function computes the Manhattan distance heuristicManhattan for the given state.
    It takes a 2D list representing the puzzle state as input and returns an integer representing the heuristic cost. 
    The time complexity of this function is O(n^2) where n is the size of the puzzle state.
    The space complexity of this function is O(1).
    '''
    distance = 0  # This variable will be used to keep track of the Manhattan distance heuristic of the given puzzle state.
    # These nested loops iterate over each element of the 2D list state, from state[0][0] to state[2][2]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # This code block checks if the current element of the 2D list state is not equal to zero. If the element is not equal to zero, it means that the current tile is not the empty tile, and we need to compute its Manhattan distance heuristic.
                # Index represents the position of the tile in a flattened representation of the puzzle state.
                index = state[i][j] - 1
                goalRow = index // 3  # Goal row of the tile
                goalCol = index % 3  # Goal column of the tile
                # This line calculates the Manhattan distance between the current tile's current position and its goal position using the row and column indices calculated in the previous line.
                # The Manhattan distance is the absolute difference between the row indices plus the absolute difference between the column indices.
                distance += abs(goalRow - i) + abs(goalCol - j)
    return distance  # Total Manhattan distance heuristic for the puzzle state


class Node:
    '''
    This class represents a node in the search tree.
    '''

    def __init__(self, state, g=0, parent=None):
        '''
        The __init__ method is the constructor for the Node class. It takes three parameters: state, g, and parent. 
        The state parameter represents the current state of the problem being solved, typically represented as a 2D list in this context. 
        The g parameter represents the cost to reach the current state, 
        and the parent parameter is a reference to the parent node in the search tree. 
        If this node is the root node, then the parent parameter should be set to None.
        The time complexity is O(1), and the space complexity is O(n^2)
        '''
        self.state = state  # current state
        self.g = g  # cost to reach current state
        self.h = heuristicManhattan(state)  # estimated cost
        self.parent = parent  # parent node

    def f(self):
        '''
        The f method returns the sum of g and h, where h is the estimated cost to reach the goal state using the heuristic function. 
        This is the cost function used by the search algorithm to determine which nodes to explore first.
        The time complexity is O(1), and the space complexity is O(1)
        '''
        return self.g + self.h

    def __lt__(self, another):
        '''
        The compare method is used to define the comparison operator for Node objects. With this objects using the < operator.
        It returns True if the f value of this node is less than the f value of the another node. 
        This is used to maintain a priority queue of nodes to explore, where nodes with lower f values are explored first. 
        The time complexity is O(1), and the space complexity is O(1)
        '''
        return self.f() < another.f()


def moves(state):
    '''
    This function generates all possible moves that can be made from a given state in the 8-Puzzle Problem. 
    It takes a 2D list representing the puzzle state as input and returns a list of all possible successor states.
    Time complexity is still O(n^2). Space complexity is O(n^2) because the function creates a new 3x3 matrix for each possible move.
    '''
    i = None
    j = None
    # In nested loop the program fins the row i row i and column j of the empty cell represented by 0 in the puzzle.
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                break
        if state[i][j] == 0:
            break
    # This line initializes an empty list called possibleMoves to store the new states that can be reached by moving the empty cell in different directions.
    possibleMoves = []
    # This line iterates over each pair (di, dj) in the tuple ((0, 1), (1, 0), (0, -1), (-1, 0)). Each pair represents a direction in which the empty cell can be moved: right, down, left, or up.
    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        # This line checks if the empty cell can be moved in the direction represented by the current pair (di, dj) without going out of bounds. It checks that the new row i+di and column j+dj are both between 0 and 2, which are the valid indices of the puzzle.
        if 0 <= i+di < 3 and 0 <= j+dj < 3:
            # This loop creates a new copy of the state list that copies each row.
            new_state = []
            for row in state:
                new_row = []
                for element in row:
                    new_row.append(element)
                new_state.append(new_row)
            # This line swaps the values of the empty cell (at index (i, j)) with the value of the cell in the direction represented by the current pair (di, dj) (at index (i+di, j+dj)). This creates a new state that is the result of moving the empty cell in the given direction.
            new_state[i][j], new_state[i+di][j + dj] = new_state[i+di][j+dj], new_state[i][j]
            # This line appends the new state (i.e., the result of moving the empty cell in the given direction) to the list of possibleMoves.
            possibleMoves.append(new_state)
    # Finally, the function returns the list of possibleMoves, which contains all the new states that can be reached by moving the empty cell in different directions.
    return possibleMoves


def a_star(start):
    '''
    This function implements the A* search algorithm.
    It takes a start node as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    The function uses a priority queue to keep track of the frontier and a set to keep track of the visited nodes.
    The time complexity of this function is O(b^d) where b is the branching factor (which is at most 4 here), d is the maximum depth of the search tree, 
    and d can be up to the maximum number of moves required to solve the puzzle from the start state.
    The space complexity of this function is also O(b^d) to store the frontier and the visited nodes.
    '''
    queue = PriorityQueue()  # These lines initialize a priority queue, queue, which is used to keep track of the nodes on the frontier.
    queue.put((start.f(), start)) # The start node is added to the queue with its f-score as the priority value.
    visited = set() # The visited set is used to keep track of the nodes that have already been visited.
    # This is the main loop of the algorithm. It continues until the queue is empty, meaning that there are no more nodes to explore. 
    while not queue.empty():
        f, node = queue.get() # The node with the lowest f-score is removed from the queue and assigned to the node variable.
        if node.state == GOAL_STATE:  # If the current node is the goal state, a solution has been found.
            path = [] #
            while node.parent: # The function constructs a path from the start state to the goal state by tracing back through the parent nodes of each node in the path. 
                path.append(node.state) 
                node = node.parent
            path.append(start.state)
            return path[::-1] # The path is returned in reverse order, starting from the start state.
        # If the current node is not the goal state, the function adds the state of the node to the visited set.
        visited.add(tuple(map(tuple, node.state)))
        # The function generates all possible moves from the current state using the moves function, and for each move, it creates a new child node.
        for move in moves(node.state):
            if tuple(map(tuple, move)) not in visited: #If the state of the child node has not already been visited
                child = Node(move, node.g+1, node) # assigning move (state), cost to reach the child node from the start node, and node as parent node
                queue.put((child.f(), child)) # the child node is added to the priority queue with its f-score as the priority value


def solve_puzzle(start_state):
    '''
    This function solves the puzzle from the given start state using the A* search algorithm.
    It takes a 2D list representing the start state as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    This function creates a Node object from the given start_state and passes it to a_star() to solve the puzzle.
    The time and space complexity of this function is the same as the a_star function.
    The time complexity of this function is O(b^d).
    The space complexity of this function is O(b^d).
    '''
    start = Node(start_state)  # This line creates a Node object from the given start_state by calling the Node class constructor with start_state as the state parameter. The g and parent parameters are not specified, so they default to 0 and None respectively.
    path = a_star(start)  # The path variable is assigned the result of this function call.
    return path # This line returns the path variable, which contains either the optimal path from the start state to the goal state or None if a solution is not found.


# Initialize Pygame
pygame.init()
# This line creates a window for the game with a specified width and height. WIDTH and HEIGHT are constants defined earlier in the code.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# This line sets the caption of the window to "3x3 Sliding Puzzle", which is the name of the game.
pygame.display.set_caption("3x3 Sliding Puzzle")
# This line creates a Clock object, which can be used to keep track of time in the game loop. The clock object is used to limit the frame rate and ensure that the game runs smoothly.
clock = pygame.time.Clock()


class Tile:
    '''
    This class represents a tile in the puzzle. 
    '''

    def __init__(self, x, y, value):
        '''
        This is the constructor method that initializes a new tile object with the given x, y coordinates and value. 
        The rect attribute of the tile is created as a pygame. Rect object (which represents rectangle) with the given coordinates and dimensions calculated as WIDTH//3 and HEIGHT//3, respectively.
        The time complexity is O(1).
        Space complexity is O(1).
        '''
        self.rect = pygame.Rect(x, y, WIDTH//3, HEIGHT//3)
        self.value = value

    def draw(self, surface):
        '''
        This function draws the tile on a given surface, which is typically the Pygame window.
        It first sets the color variable to WHITE if the tile's value is 0, otherwise it sets it to GREEN. 
        If the tile's value is not 0, it draws a rectangle around the tile's rect with a thickness of 1 pixel using pygame.draw.rect().
        It then fills the tile's rect with the appropriate color. 
        Finally, if the tile's value is not 0, it renders the value as text using pygame.font.SysFont() with a font size of 50, and blits it onto the surface at the center of the tile's rect.
        The time complexity is O(1).
        Space complexity is O(1).
        '''
        if self.value == 0: # If the value of the tile (self.value) is 0, it sets the color variable to WHITE
            color = WHITE
        else: # If the value of the tile is not 0, it sets the color variable to GREEN
            color = GREEN
        pygame.draw.rect(surface, color, self.rect) # draw the rectangle representing the tile.
        if self.value != 0: # If the value of the tile is not 0
            font = pygame.font.SysFont(None, 50) # font size is 50
            text = font.render(str(self.value), True, BLACK) # value of the tile as text
            text_rect = text.get_rect(center=self.rect.center) # center the text
            surface.blit(text, text_rect) # draws the text on the tile's rectangle
            pygame.draw.rect(surface, BLACK, self.rect, 1) # to create border


def draw_board(state):
    '''
    This function draws the entire puzzle board on the screen, by creating a Tile object for each tile in the input state and calling its draw() method. 
    Its time complexity is O(n^2), since it creates a Tile object for each tile.
    Its space complexity is O(n^2), since it stores all the Tile objects in memory.
    '''
    for i in range(3):  # This sets up a nested loop to iterate through each row and column of the puzzle.
        for j in range(3):
            # For each tile, a new Tile object is created with a position determined by the row i and column j. 
            # The WIDTH and HEIGHT are the dimensions of the window on which the game is displayed, 
            # and // is used to perform integer division. The state[i][j] value is passed to the Tile constructor to determine the number displayed on the tile.
            tile = Tile(j*WIDTH//3, i*HEIGHT//3, state[i][j])
            # The draw() method is called on the Tile object to draw it onto the screen. The screen variable represents the Pygame window on which the game is displayed.
            tile.draw(screen)


def main():
    '''
    The main function initializes the Pygame window and sets up the starting state of the puzzle. 
    It then calls the solve_puzzle function to solve the puzzle and displays the solution on the Pygame window.
    The time complexity of the main function is determined by the time complexity of the solve_puzzle function.(O(b^d))
    The space complexity of the main function is determined by the space complexity of the solve_puzzle function.(O(b^d))
    '''

    # Define the starting state of the puzzle
    start_state = [[1, 2, 3], [0, 7, 8], [4, 5, 6], ]

    # This line calls the solve_puzzle() function to solve the puzzle using the start_state as the initial state. The resulting path is stored in the path variable.
    path = solve_puzzle(start_state)

    if path is not None:  # Checks if a solution was found by the solve_puzzle() function. If a solution was found (path is not None)
        print("Solution found!") # The code prints "Solution found!" to the console.
        print("Number of steps:", len(path) - 1) # The code prints how many steps did it take to find solution.
        # The for loop iterates through each state in the path list  and the time.sleep(1).
        for state in path: 
            draw_board(state) #draws the puzzle to the Pygame window.
            pygame.display.update() # updates the display to show the new state of the puzzle.
            time.sleep(1) # function adds a delay of one second between each state to slow down the animation.
    else: # If no solution was found
        print("No solution found.") # the code prints "No solution found."

    while True:  # This while loop waits for the user to close the Pygame window by clicking the close button.
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # When the close button is clicked
                pygame.quit() # the loop exits and the pygame.quit() function is called to exit the Pygame window.
                return


if __name__ == '__main__':
    '''
    The if __name__ == '__main__': line ensures that the main() function is only called when the script is run as the main program, and not when it is imported into another script.
    '''
    main()
