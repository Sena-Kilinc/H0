import time
import pygame
from queue import PriorityQueue

# Define constants
WIDTH = 300
HEIGHT = 300
FPS = 60

# Define colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)


# Define the goal state 2D List
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Define the heuristic function


def heuristic(state):
    '''
    This function computes the Manhattan distance heuristic for the given state.
    It takes a 2D list representing the puzzle state as input and returns an integer representing the heuristic cost. 
    The time complexity of this function is O(n^2) where n is the size of the puzzle state.
    The space complexity of this function is O(1).
    '''
    distance = 0  # This variable will be used to keep track of the Manhattan distance heuristic of the given puzzle state.
    # These nested loops iterate over each element of the 2D list state, from state[0][0] to state[2][2]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # This code block checks if the current element of the 2D list state is not equal to zero. If the element is not equal to zero, it means that the current tile is not the empty tile, and we need to compute its Manhattan distance heuristic.
                x, y = divmod(state[i][j]-1, 3)  # This line uses the divmod() function to calculate the row and column indices of the current tile's goal position in the puzzle. The divmod() function takes two arguments: state[i][j]-1, which is the index of the current tile, and 3, which is the number of columns in the puzzle. The divmod() function returns a tuple containing the quotient and remainder of the division operation. The quotient represents the row index of the current tile's goal position, and the remainder represents the column index of the current tile's goal position.
                # This line calculates the Manhattan distance between the current tile's current position and its goal position using the row and column indices calculated in the previous line. The Manhattan distance is the absolute difference between the row indices plus the absolute difference between the column indices.
                distance += abs(x-i) + abs(y-j)
    return distance  # This line calculates the Manhattan distance between the current tile's current position and its goal position using the row and column indices calculated in the previous line. The Manhattan distance is the absolute difference between the row indices plus the absolute difference between the column indices.

# Define the node class


class Node:
    '''
    This class represents a node in the search tree, which contains the current state, the cost to reach this state, 
    the estimated cost to reach the goal state (using the heuristic function), and a reference to its parent node.
    '''

    def __init__(self, state, g=0, parent=None):
        '''
        The __init__ method is the constructor for the Node class. It takes three parameters: state, g, and parent. The state parameter represents the current state of the problem being solved, typically represented as a 2D list in this context. The g parameter represents the cost to reach the current state, and the parent parameter is a reference to the parent node in the search tree. If this node is the root node, then the parent parameter should be set to None.
        '''

        self.state = state  # current state
        self.g = g  # cost to reach current state
        self.h = heuristic(state)  # estimated cost
        self.parent = parent

    def f(self):
        '''
        The f method returns the sum of g and h, where h is the estimated cost to reach the goal state using the heuristic function. This is the cost function used by the search algorithm to determine which nodes to explore first.
        '''
        return self.g + self.h

    def __lt__(self, other):
        '''
        The __lt__ method is used to define the comparison operator for Node objects. In this case, it returns True if the f value of this node is less than the f value of the other node, where other is another Node object being compared to this one. This is used to maintain a priority queue of nodes to explore, where nodes with lower f values are explored first.
        '''
        return self.f() < other.f()

# Define the possible moves

# This defines a function called moves that takes a 2D list representing the current state of the puzzle as input.


def moves(state):
    '''
    This function generates all possible moves that can be made from a given state in the 8-puzzle problem. 
    It takes a 2D list representing the puzzle state as input and returns a list of all possible successor states.
    time complexity is still O(n^2). Space complexity is O(n^2) because the function creates a new 3x3 matrix for each possible move.
    '''
    i, j = next((i, j) for i in range(3) for j in range(
        3) if state[i][j] == 0)  # This line finds the row i and column j of the empty cell (represented by 0 in the puzzle) in the given state by using the next() function to find the first tuple (i, j) in a generator expression that satisfies the condition state[i][j] == 0. This line assumes that there is only one empty cell in the puzzle.
    # This line initializes an empty list called possible_moves to store the new states that can be reached by moving the empty cell in different directions.
    possible_moves = []
    # This line iterates over each pair (di, dj) in the tuple ((0, 1), (1, 0), (0, -1), (-1, 0)). Each pair represents a direction in which the empty cell can be moved: right, down, left, or up.
    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        # This line checks if the empty cell can be moved in the direction represented by the current pair (di, dj) without going out of bounds. It checks that the new row i+di and column j+dj are both between 0 and 2, which are the valid indices of the puzzle.
        if 0 <= i+di < 3 and 0 <= j+dj < 3:
            # This line creates a new copy of the state list by using a list comprehension that copies each row of state using the [:] slice notation. This creates a new list of lists that has the same values as state, but is a separate object in memory. This ensures that the original state list is not modified during the execution of the moves() function.
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[i+di][j +
                                             dj] = new_state[i+di][j+dj], new_state[i][j]   # This line swaps the values of the empty cell (at index (i, j)) with the value of the cell in the direction represented by the current pair (di, dj) (at index (i+di, j+dj)). This creates a new state that is the result of moving the empty cell in the given direction.
            # This line appends the new state (i.e., the result of moving the empty cell in the given direction) to the list of possible_moves.
            possible_moves.append(new_state)
    # Finally, the function returns the list of possible_moves, which contains all the new states that can be reached by moving the empty cell in different directions.
    return possible_moves

# Define the A* search algorithm


def a_star(start):
    '''
    This function implements the A* search algorithm.
    It takes a start node as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    The function uses a priority queue to keep track of the frontier and a set to keep track of the visited nodes.
    The time complexity of this function is O(b^d) where b is the branching factor (which is at most 4 here), d is the maximum depth of the search tree, 
    and d can be up to the maximum number of moves required to solve the puzzle from the start state.
    The space complexity of this function is also O(b^d) to store the frontier and the visited nodes.
    '''
    queue = PriorityQueue()  # These lines initialize a priority queue, queue, which is used to keep track of the nodes on the frontier. The start node is added to the queue with its f-score as the priority value. The visited set is used to keep track of the nodes that have already been visited.
    queue.put((start.f(), start))
    visited = set()
    # This is the main loop of the algorithm. It continues until the queue is empty, meaning that there are no more nodes to explore. The node with the lowest f-score is removed from the queue and assigned to the node variable.
    while not queue.empty():
        f, node = queue.get()
        if node.state == GOAL_STATE:  # If the current node is the goal state, a solution has been found. The function constructs a path from the start state to the goal state by tracing back through the parent nodes of each node in the path. The path is returned in reverse order, starting from the start state.
            path = []
            while node.parent:
                path.append(node.state)
                node = node.parent
            path.append(start.state)
            return path[::-1]
        # If the current node is not the goal state, the function adds the state of the node to the visited set.
        visited.add(tuple(map(tuple, node.state)))
        # The function generates all possible moves from the current state using the moves function, and for each move, it creates a new child node. If the state of the child node has not already been visited, the child node is added to the priority queue with its f-score as the priority value.
        for move in moves(node.state):
            if tuple(map(tuple, move)) not in visited:
                child = Node(move, node.g+1, node)
                queue.put((child.f(), child))


# Define the puzzle solver function
# This line defines the solve_puzzle function that takes a 2D list representing the start state of the puzzle as input.
def solve_puzzle(start_state):
    '''
    This function solves the puzzle from the given start state using the A* search algorithm.
    It takes a 2D list representing the start state as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    This function creates a Node object from the given start_state and passes it to a_star() to solve the puzzle.
    The time and space complexity of this function is the same as the a_star function.
    '''
    start = Node(start_state)  # This line creates a Node object from the given start_state by calling the Node class constructor with start_state as the state parameter. The g and parent parameters are not specified, so they default to 0 and None respectively.
    path = a_star(start)  # This line calls the a_star function with the start Node object as the argument. The a_star function returns the optimal path from the start state to the goal state if a solution is found, otherwise it returns None. The path variable is assigned the result of this function call.
    # This line returns the path variable, which contains either the optimal path from the start state to the goal state or None if a solution is not found.
    return path


# Initialize Pygame
pygame.init()
# This line creates a window for the game with a specified width and height. WIDTH and HEIGHT are constants defined earlier in the code.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# This line sets the caption of the window to "3x3 Sliding Puzzle", which is the name of the game.
pygame.display.set_caption("3x3 Sliding Puzzle")
# This line creates a Clock object, which can be used to keep track of time in the game loop. The clock object is used to limit the frame rate and ensure that the game runs smoothly.
clock = pygame.time.Clock()

# Define the tile class


class Tile:
    '''
    This class represents a tile in the puzzle. 
    It takes the x and y coordinates of the tile and its value as input
    The time complexity of the Tile class is O(1) for each of its methods, since the operations performed do not depend on the size of the puzzle. The space complexity is also O(1), since each tile object stores only a few attributes that do not scale with the size of the puzzle.
    '''

    def __init__(self, x, y, value):
        '''
        This is the constructor method that initializes a new tile object with the given x and y coordinates and value. The rect attribute of the tile is created as a pygame.Rect object with the given coordinates and dimensions calculated as WIDTH//3 and HEIGHT//3, respectively.
        ): This function initializes a Tile object with x and y coordinates and a value, and creates a Rect object. The time complexity is O(1) since it simply assigns values to variables. Space complexity is O(1).
        '''
        self.rect = pygame.Rect(x, y, WIDTH//3, HEIGHT//3)
        self.value = value

    '''
     draw method to draw the tile on the Pygame window. 
     The time complexity of this class is O(1) and 
     the space complexity is O(1) to store the tile information.
    '''

    def draw(self, surface):
        '''
        This method draws the tile on a given surface, which is typically the Pygame window. It first sets the color variable to WHITE if the tile's value is 0, otherwise it sets it to GRAY. If the tile's value is not 0, it draws a rectangle around the tile's rect with a thickness of 1 pixel using pygame.draw.rect(). It then fills the tile's rect with the appropriate color. Finally, if the tile's value is not 0, it renders the value as text using pygame.font.SysFont() with a font size of 50, and blits it onto the surface at the center of the tile's rect.
        '''
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


# Define the draw function
# This is a function definition for draw_board, which takes in an input state, representing the current state of the puzzle.
def draw_board(state):
    '''
    This function draws the entire puzzle board on the screen, by creating a Tile object for each tile in the input state and calling its draw() method. 
    Its time complexity is O(n^2), since it creates a Tile object for each tile, and its space complexity is O(n^2), since it stores all the Tile objects in memory.
    '''
    for i in range(3):  # This sets up a nested loop to iterate through each row and column of the puzzle.
        for j in range(3):
            # For each tile, a new Tile object is created with a position determined by the row i and column j. The WIDTH and HEIGHT are the dimensions of the window on which the game is displayed, and // is used to perform integer division. The state[i][j] value is passed to the Tile constructor to determine the number displayed on the tile.
            tile = Tile(j*WIDTH//3, i*HEIGHT//3, state[i][j])
            # The draw() method is called on the Tile object to draw it onto the screen. The screen variable represents the Pygame window on which the game is displayed.
            tile.draw(screen)


def main():
    '''
    The main function initializes the Pygame window and sets up the starting state of the puzzle. 
    It then calls the solve_puzzle function to solve the puzzle and displays the solution on the Pygame window.
    The time complexity of the main function is determined by the time complexity of the solve_puzzle function.
    The space complexity of the main function is determined by the space complexity of the solve_puzzle function.
    Additionally, the main function uses Pygame to display the solution on the screen, so it also uses some additional space for Pygame resources such as the screen and font objects. 
    However, this space usage is negligible compared to the space used by the solve_puzzle function.
    The main loop of the function runs indefinitely until the user closes the window, so the space complexity of the function could be up to O(b^d) if the solution is not found, where b is the branching factor and d is the depth of the search tree. However, the time complexity depends on how long the user chooses to keep the window open.
    The main function itself contains a simple loop that runs indefinitely until the user closes the window, so its time complexity is constant, or O(1), since the number of iterations is not determined by the input size.
    '''

    # Define the starting state of the puzzle
    #start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    start_state = [[1, 2, 3], [0, 7, 8], [4, 5, 6], ]
    # Solve the puzzle
    # This line calls the solve_puzzle() function to solve the puzzle using the start_state as the initial state. The resulting path is stored in the path variable.
    path = solve_puzzle(start_state)

    if path is not None:  # This if-else statement checks if a solution was found by the solve_puzzle() function. If a solution was found (path is not None), the code prints "Solution found!" to the console and draws the puzzle to the Pygame window. The for loop iterates through each state in the path list and calls the draw_board() function to draw the puzzle on the Pygame window. The pygame.display.update() function updates the display to show the new state of the puzzle, and the time.sleep(1) function adds a delay of one second between each state to slow down the animation. If no solution was found, the code prints "No solution found." to the console
        print("Solution found!")
        # Draw the puzzle
        for state in path:
            draw_board(state)
            pygame.display.update()
            time.sleep(1)
    else:
        print("No solution found.")

    # Wait for the window to be closed
    while True:  # Finally, this while loop waits for the user to close the Pygame window by clicking the close button. When the close button is clicked, the loop exits and the pygame.quit() function is called to exit the Pygame window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == '__main__':
    main()
'''
The if __name__ == '__main__': line ensures that the main() function is only called when the script is run as the main program, and not when it is imported into another script.
'''


''''
In this code, g(n) is represented by the instance variable g of the Node class. It is calculated as the path cost from the initial state to node n.

In the Node class, g is initialized to 0 for the start node, and for each child node, it is incremented by 1 to account for the cost of moving to that node.

For example, when we create the start node in the solve_puzzle function, we pass the initial state to the Node constructor without specifying a value for g. Since this is the start node, we set g to 0 by default:

scss
Copy code
start = Node(start_state)
When we create a child node in the moves function, we pass the parent node and the new state to the Node constructor, and we set g to the parent's g plus 1, since moving to the child node incurs a cost of 1:

scss
Copy code
child = Node(move, node.g+1, node)
So in this way, the path cost from the start node to each node in the search tree is represented by the g value of that node.

The Manhattan distance is calculated by summing the absolute differences between the row and column indices of two tiles, for each tile in the puzzle, excluding the blank tile.

In the heuristic function of the code you provided, the calculation of the Manhattan distance is done using the following code:
python
Copy code
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j]-1, 3)
                distance += abs(x-i) + abs(y-j)
    return distance
The function loops through each tile in the puzzle represented by the 2D list state, and for each tile that is not the blank tile, it calculates the row and column indices of the tile in the solved puzzle, using the formula x, y = divmod(state[i][j]-1, 3).

The divmod function takes the value of the tile and subtracts 1 (since the tiles are numbered from 1 to 8), and then divides the result by 3. This gives the row index x and the column index y of the tile in the solved puzzle, since the solved puzzle is represented by the list GOAL_STATE.

Finally, the Manhattan distance is calculated by summing the absolute differences between the current row and column indices of the tile and its indices in the solved puzzle, using the expression distance += abs(x-i) + abs(y-j).



Yes, the code is consistent. The A* algorithm is both admissible and consistent because the heuristic function satisfies the conditions of both admissibility and consistency. The admissibility condition means that the heuristic never overestimates the actual cost to reach the goal state. The consistency condition means that the heuristic satisfies the triangle inequality, which is that the heuristic value of any node plus the cost of reaching a neighbor must be less than or equal to the heuristic value of that neighbor. In the code, the heuristic function calculates the Manhattan distance between the current state and the goal state, which satisfies both admissibility and consistency conditions.



heuristic(state): Time complexity is O(1) because it performs a constant number of operations regardless of the size of the state. Space complexity is also O(1) because it only stores a single integer value.

moves(state): Time complexity is O(1) because it performs a constant number of operations regardless of the size of the state. Space complexity is O(1) because it only stores a list of up to 4 new states.

a_star(start): Time complexity depends on the search algorithm's performance, but in the worst case, it has a time complexity of O(b^d), where b is the branching factor and d is the depth of the shallowest goal node. Space complexity is also O(b^d) because it stores all the nodes generated during the search.

solve_puzzle(start_state): This function just wraps the A* algorithm call, so its time and space complexities are the same as those of a_star(start).

Tile(x, y, value): Time complexity is O(1) because it performs a constant number of operations regardless of the size of the state. Space complexity is O(1) because it only stores the tile position and value.

draw_board(state): Time complexity is O(n^2) because it has to iterate over every tile in the 3x3 state. Space complexity is O(1) because it only stores a single tile object at a time.
'''
