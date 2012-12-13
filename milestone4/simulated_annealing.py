'''NAMES OF THE AUTHOR(S):
Benoit Daccache
Christopher Castermane'''

import time
from utils import *
from search import *
from state import *
from tsp_problem import *
from ioutils import *

class SimulatedAnnealing:

    def start(filename):
        dist_matrix,nbr_cities = IOUtils.parse_to_matrix(filename)
            
        a = time.time()
        tsp = TSPProblem(State(nbr_cities, dist_matrix))
        node = simulated_annealing(tsp)
        print(node.state)
        print("Cost :",node.state.dist_cost())
        print("Nbr of steps :",node.step)
        print("Time :",round(time.time()-a, 3),"s")


if __name__ == "__main__":
    r = SimulatedAnnealing.start(sys.argv[1])

