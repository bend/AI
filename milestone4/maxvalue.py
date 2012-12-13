'''NAMES OF THE AUTHOR(S):
Benoit Daccache
Christopher Castermane'''

import time
import sys
from utils import *
from search import *
from state import *
from tsp_problem import *
from ioutils import *

class MaxValue:

    def start(filename):
        dist_matrix,nbr_cities = IOUtils.parse_to_matrix(filename)
        a = time.time()
        tsp = TSPProblem(State(nbr_cities, dist_matrix))
        node = MaxValue.max_value(tsp, 100)
        print(node.state)
        print("Cost :",node.state.dist_cost())
        print("Nbr of steps :",node.step)
        print("Time :",round(time.time()-a, 3),"s")
        
    def max_value(problem, limit=100):        
        current = LSNode(problem, problem.initial, 0)
        best = current
        
        for step in range(limit):
            for i in list(current.expand()):
                if i.value() > best.value():
                    best = i
                    best_step = step
            current = best
            print(step, -current.value())
        return best

if __name__ == "__main__":
    r = MaxValue.start(sys.argv[1])

