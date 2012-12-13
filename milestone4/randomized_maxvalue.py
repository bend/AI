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

class RandomizedMaxValue:
    
    def start(filename):
        dist_matrix,nbr_cities = IOUtils.parse_to_matrix(filename)
        a = time.time()
        tsp = TSPProblem(State(nbr_cities, dist_matrix))
        node = RandomizedMaxValue.randomized_max_value(tsp, 100)
        print(node.state)
        print("Cost :",node.state.dist_cost())
        print("Nbr of steps :",node.step)
        print("Time :",round(time.time()-a, 3),"s")
        
    def randomized_max_value(problem, limit=100):
        current = LSNode(problem, problem.initial, 0)
        best = current
        for step in range(limit):
            best_list = []
            
            for i in list(current.expand()):
                best_list.append([i.value(),i])
                
            best_list = sorted(best_list, key=lambda b: b[0], reverse=True)
            
            best_list = best_list[:5]
            tmp = random.choice(best_list)
            
            current = tmp[1]
            if tmp[0] > best.value():
                best = current
            print(step, -current.value())
            
        return best

if __name__ == "__main__":
    r = RandomizedMaxValue.start(sys.argv[1])

