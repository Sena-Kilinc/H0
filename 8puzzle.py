'''
This project solves 8-Puzzle Game using A* Search Algorithm.
The 8 puzzle game is a sliding puzzle that consists of a 3x3 grid with eight numbered tiles and one empty space. Empty represented as 0.
The objective of the game is to rearrange the tiles from their initial scrambled positions to reach a specific target configuration:
1 2 3
4 5 6
7 8 0
@ Sena Kılınç 20191701033
'''

from queue import PriorityQueue

# The goal state for the game as 2D List
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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
        Time complexity: O(1) - Constant. 
        Space complexity: O(1) - Constant. 
        '''
        self.state = state # Current state
        self.g = g # Cost to reach current state
        self.h = heuristicManhattan(state) # Estimated cost to reach the goal state
        self.parent = parent # Parent node

    def f(self):
        '''
        The f method returns the sum of g and h, where h is the estimated cost to reach the goal state using the heuristic function. 
        This is the cost function used by the search algorithm to determine which nodes to explore first.
        Time complexity: O(1) - Constant. 
        Space complexity: O(1) - Constant. 
        '''
        return self.g + self.h

    def __lt__(self, other):
        '''
        The lt method is used to define the comparison operator for Node objects. With this objects can use the < operator.
        It returns True if the f value of this node is less than the f value of the other node. 
        This is used to maintain a priority queue of nodes to explore, where nodes with lower f values are explored first. 
        Time complexity: O(1) - Constant. 
        Space complexity: O(1) - Constant. 
        '''
        return self.f() < other.f()

def heuristicManhattan(state):
    '''
    This function computes the Manhattan distance heuristicManhattan for the given state.
    It takes a 2D list representing the puzzle state as input and returns an integer representing the heuristic cost.
    Time complexity: O(n^2) Quadratic, where n is the size of the puzzle (n=3).
    Space complexity: O(1) Constant, since the function uses a constant amount of memory.
    '''
    distance = 0 # This variable will be used to keep track of the Manhattan distance heuristic of the given puzzle state.
    # These nested loops iterate over each element of the 2D list state, from state[0][0] to state[2][2]
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # If the element is not equal to zero, it means that the current tile is not the empty tile, and we need to compute its Manhattan distance heuristic.
                index = state[i][j] -1 # Index represents the position of the tile in a flattened representation of the puzzle state.
                goalRow = index // 3   # Goal row of the tile
                goalCol = index % 3   # Goal column of the tile
                distance += abs(i-goalRow) + abs(j-goalCol) # This line calculates the Manhattan distance between the current tile's current position and its goal position
    return distance # Total Manhattan distance heuristic for the puzzle state

def actions(state):
    '''
    This function generates all possible actions that can be made from a given state in the 8-Puzzle Problem.
    It takes a 2D list representing the puzzle state as input and returns a list of all possible successor states.
    Time complexity: O(n^2) Quadratic.
    Space complexity: O(n^2) Quadratic.
    '''
    i = None # row
    j = None # column
    for i in range(3): # In nested loop the program finds the row i and column j of the empty cell represented by 0.
        for j in range(3):
            if state[i][j]==0:
                break
        if state[i][j]==0:
            break
    possibleActions = [] # Initialized an empty list for storing new states that can be reached by moving the empty cell in different directions.
    for row, col in ((0, 1), (1, 0), (0, -1), (-1, 0)): # To iterate over pairs that represent directions which empty cell can move: right,up,left,down.
        if 0 <= i + row < 3 and 0 <= j + col < 3: # checks for the empty tile's actions without going out of bounds.
            newState=[] # to create new state which copies each row.
            for rowX in state:
                newRow=[]  # to create row list.
                for element in rowX:
                    newRow.append(element) # insert each element to the row list.
                newState.append(newRow) # insert row list to the state list.
            # This is a swap line for moving the empty cell in the given direction.
            newState[i][j], newState[i + row][j + col] = newState[i + row][j + col], newState[i][j]
            possibleActions.append(newState) # To append the new state to the list of possibleActions.
    return possibleActions # this list will contain all the new states that can be reached by moving the empty cell in different directions.

def aStarSearch(start):
    '''
    This function implements the A* search algorithm.
    It takes a start node as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    The function uses a priority queue to keep track of the frontier and a set to keep track of the visited nodes.
    Time complexity: O(b^d) - Exponential. In the worst case, where b is the branching factor and d is the depth of the solution, the algorithm explores all possible states in the search space.
    Space complexity: O(b^d) - Exponential. The algorithm keeps track of all visited states, and the priority queue can store up to b^d nodes in the worst case.
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
        for action in actions(node.state):
            if tuple(map(tuple, action)) not in visited: #If the state of the child node has not already been visited
                child = Node(action, node.g+1, node) # assigning move (state), cost to reach the child node from the start node, and node as parent node
                queue.put((child.f(), child)) # the child node is added to the priority queue with its f-score as the priority value


def solve_puzzle(start_state):
    '''
    This function solves the puzzle from the given start state using the A* search algorithm.
    It takes a 2D list representing the start state as input and returns the path from the start state to the goal state if a solution is found, otherwise returns None.
    This function creates a Node object from the given start_state and passes it to a_star() to solve the puzzle.
    Time complexity: O(b^d) - Exponential. The time complexity is the same as aStarSearch(start) since it calls that function.
    Space complexity: O(b^d) - Exponential. The space complexity is the same as aStarSearch(start) since it calls that function.
    '''
    start = Node(start_state)  # This line creates a Node object from the given start_state by calling the Node class constructor with start_state as the state parameter. The g and parent parameters are not specified, so they default to 0 and None respectively.
    path = aStarSearch(start)  # The path variable is assigned the result of this function call.
    return path # This line returns the path variable, which contains either the optimal path from the start state to the goal state or None if a solution is not found.


def print_board(state):
    '''
    This functions is for printing the puzzle board state.
    Time complexity: O(n^2).
    Space complexity: O(n^2).
    '''
    # These nested loops iterate over each element of the 2D list state
    for i in range(3):
        for j in range(3):
            print(state[i][j], end=' ') #  # Print the value at the current cell
        print() # print a new line after each row

def main():
    '''
    The main function calls the solve_puzzle function to solve the puzzle and prints the solution.
    The time complexity of the main function is determined by the time complexity of the solve_puzzle function.(O(b^d))
    The space complexity of the main function is determined by the space complexity of the solve_puzzle function.(O(b^d))

    '''
    start_state = [[1, 2, 3], [0, 7, 8], [4, 5, 6]] # Set the initial state of the puzzle
    path = solve_puzzle(start_state) # Solve the puzzle and get the solution path
    if path is not None: # Checks if a solution was found by the solve_puzzle() function. If a solution was found (path is not None)
        print("Solution found!") # The code prints "Solution found!" to the console.
        print("Number of steps:",len(path)-1) # Print the number of steps in the solution path
        # Print the puzzle states in the solution path
        for state in path:
            print_board(state) # Print the current puzzle state
            print("*********") # Print a separator line
    else: # If no solution was found
        print("No solution found.") # the code prints "No solution found."

if __name__ == '__main__':
    '''
    The if __name__ == '__main__': line ensures that the main() function is only called when the script is run as the main program, and not when it is imported into another script.
    '''
    main() # Call the main function to start the program
