'''NAMES OF THE AUTHOR(S):
Benoit Daccache
Christopher Castermane'''

from search import *
from state import *


######################  Implement the search #######################

class PuzzleProblem(Problem):
    """Contains the initial State"""
    
    def __init__(self,init):
        """Open and put the grid in 2d array"""
        f = open(init, 'r')
        j = 0
        grid = [[None for x in range(CONST_HEIGHT)] for y in range(CONST_WIDTH)]
        for line in f:
            i = 0
            for word in line.split():
                grid[i][j] = word
                i+=1
            j+=1
        self.initial = State(grid)

###################################################   
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        if state.grid[1][4] == "1" and state.grid[2][4] == "1":
            return True
        return False

###################################################   
    def get_empty_cells(self, state):
        """Return a sequence of the coordinates of the empty cells
        (represented by 0)"""
        for y in range(0,CONST_HEIGHT):
            for x in range(0,CONST_WIDTH):
                if state.grid[x][y] == "0":
                    yield [x,y]
        
###################################################   
    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        
        # Search for empty cells
        empty_cells = self.get_empty_cells(state)
        
        for i in empty_cells:
            x = i[0]
            y = i[1]
            
            # Move the empty cell top if possible
            # Make sure we don't move an empty cell on another empty cell, 
            # and check for the limit of the grid
            if y > 0 and state.grid[x][y-1] != "0":
                new_state = state.successor(x, y, "top")
                if new_state is not None :
                    yield("top", new_state)
            
            # Move the empty cell bottom if possible
            if y+1 < CONST_HEIGHT and state.grid[x][y+1] != "0":
                new_state = state.successor(x, y, "bottom")
                if new_state is not None:
                    yield("bottom", new_state)
            
            # Move the empty cell left if possible
            if x > 0 and state.grid[x-1][y] != "0":
                new_state = state.successor(x, y, "left")
                if new_state is not None:
                    yield("left", new_state)

            # Move the empty cell right if possible
            if x+1 < CONST_WIDTH and state.grid[x+1][y] != "0":
                new_state = state.successor(x, y, "right")
                if new_state is not None:
                    yield("right", new_state)

###################### Launch the search #########################
problem=PuzzleProblem(sys.argv[1])
node=breadth_first_graph_search(problem)
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assume that the __str__ function of states output the correct format

    
###############################
###        BENCHMARK        ###
###############################
#puzzles = ["init1.txt", "init2.txt", "init3.txt", "init4.txt","init5.txt", "init6.txt", "init7.txt", "init8.txt","init9.txt", "init10.txt"]
#total_time = time.time()
#total_movements = 0
#for puzzle in puzzles:
#    PuzzleProblem.nodes_explored = 0
#    problem=PuzzleProblem("benchs\\"+puzzle)
#    a = time.time()
#    node=depth_first_graph_search(problem)
#    b = round(time.time()-a, 3)
#    path=node.path()
#    path.reverse()
#    i = 0
#    for n in path:
#        #print(n.state) #assume that the __str__ function of states output the correct format
#        i+=1
#    total_movements += i
#    print()
#    print("Best Solution for",puzzle)
#    print("--------------------------")
#    print(i,"Movements to do")
#    print("Solution found in",b,"s")
#    print("Total nodes explored :",PuzzleProblem.nodes_explored)
#    print()
#print("----------------------------------------")
#print("Benchmark finished.")
#print("Total time :",round(time.time()-total_time, 3),"s")
#print("Total movements :",total_movements)
