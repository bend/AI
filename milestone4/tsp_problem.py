from search import *
from state import *

class TSPProblem(Problem):

    """Returns all differents states obtained by swapping 2 points in the path."""
    def successor(self, state):
        list_size = len(state.list)
        for i in range(list_size):
            for j in range(list_size):
                if i<j: # avoid identical swaps
                    yield ((i,j),state.swap_city(i,j))
        
        
    def value(self, state):
        return -state.dist_cost()
        
        
        