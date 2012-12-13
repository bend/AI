from copy import deepcopy
import math
import random
import sys
from utils import *

class State:
    def __init__(self, nbr_cities, dist_matrix):
        self.dist_matrix = dist_matrix
        self.nbr_cities = int(nbr_cities)
        
        self.list = []
        #departure_city = random.randint(0, int(nbr_cities)-1)
        departure_city = 13
        last_city = departure_city
        
        for i in range(self.nbr_cities):
            if i > 0:
                actual_dist = sys.float_info.max
                
                for j in range(self.nbr_cities):
                    if self.list[i-1] > j:
                        dist = dist_matrix[self.list[i-1]][j]
                    else:
                        dist = dist_matrix[j][self.list[i-1]]
                        
                    if dist < actual_dist and j not in self.list:
                        actual_dist = dist
                        last_city = j
                        
            self.list.append(last_city)
            
        print(self)
        print("Cost :",self.dist_cost())
            

###########################################       
    def __hash__(self):
        s = ""
        for x in range(0, len(self.list)):
            s+=self.list[x]
        return hash(s)
            

###########################################       
    def __eq__(self, state):
        return hash(self) == hash(state)

###########################################       
    def __str__(self):
        s = ""
        for x in range(0, len(self.list)-1):
            s += str(self.list[x]) + '->'
        s += str(self.list[len(self.list)-1])
        return s
            
        
###########################################
    def swap_city(self, city1, city2):
        new_state = deepcopy(self)
        tmp = new_state.list[city1]
        new_state.list[city1] = new_state.list[city2]
        new_state.list[city2] = tmp
        return new_state
        
    def dist_cost(self):
        total_cost = 0
        for i in range(len(self.list)-1):
            if self.list[i] > self.list[i+1]:
                dist = self.dist_matrix[self.list[i]][self.list[i+1]]
            else:
                dist = self.dist_matrix[self.list[i+1]][self.list[i]]
            total_cost += dist
        
        # Close the loop : dist from last element to first
        list_len = len(self.list)-1
        if self.list[list_len] > self.list[0]:
            dist = self.dist_matrix[self.list[list_len]][self.list[0]]
        else:
            dist = self.dist_matrix[self.list[0]][self.list[list_len]]
        total_cost += dist
        
        return total_cost