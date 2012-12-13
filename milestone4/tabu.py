'''NAMES OF THE AUTHOR(S):
Benoit Daccache
Christopher Castermane'''

import time
from utils import *
from search import *
from state import *
from tsp_problem import *
from ioutils import *

class Tabu:

    def start(filename, tabu_length):
        dist_matrix,nbr_cities = IOUtils.parse_to_matrix(filename)
        a = time.time()
        tsp = TSPProblem(State(nbr_cities, dist_matrix))
        node = Tabu.tabu_search(tsp,tabu_length,100)
        print(node.state)
        print("Cost :",node.state.dist_cost())
        print("Nbr of steps :",node.step)
        print("Time :",round(time.time()-a, 3),"s")

    def tabu_search(problem, length, limit=100):
        length = int(length)
    
        current = LSNode(problem, problem.initial, 0)
        best = current
        tabu_list = []
        
        for step in range(limit):            
            best_list = []
            
            for i in list(current.expand()):
                if i not in tabu_list:
                    best_list.append([i.value(),i])
                
            best_list = sorted(best_list, key=lambda b: b[0], reverse=True)
            
            best_list = best_list[:5]
            current = random.choice(best_list)[1]
            tabu_list.append((current, length))
            
            if current.value() > best.value():
                best = current
            
            if len(tabu_list) > 0:
                new_tabu_list = []
                for i in range(len(tabu_list)):
                    if tabu_list[i][1] > 0:
                        new_tabu_list.append(tabu_list[i])
                        
                    new_length = tabu_list[i][1] - 1
                    tabu_list[i] = (tabu_list[i][0], new_length)
                    
                tabu_list = new_tabu_list
            print(step, -current.value())
                
        return best
                
                

if __name__ == "__main__":
    r = Tabu.start(sys.argv[1], sys.argv[2])

