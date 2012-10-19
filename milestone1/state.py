from copy import deepcopy
CONST_WIDTH = 4
CONST_HEIGHT = 5

class State:
    
    def __init__(self, grid):
        self.grid = grid

###########################################       
    def __hash__(self):
        i=1
        m={"0":0}
        res = 0
        mult = 1
        for line in self.grid:
            for x in line: 
                if x not in m:
                    m[x]=i
                    i+=1
                res= res + m[x]*mult
                mult = mult*10
        return res


###########################################       
    def __eq__(self, state):
        return self.__hash__() == state.__hash__()

###########################################       
    def __str__(self):
        """Prints the State"""
        s= ""
        for y in range(0,CONST_HEIGHT):
            for x in range(0,CONST_WIDTH):
                s+=self.grid[x][y]
                s+=" "
            s+="\n"
        return s
        
###########################################       
    def successor(self, x, y, action):
        return self.move(x, y, action) # Return the new possible state, created after making the action

###########################################       
    def move_cell(self, x1, y1, x2, y2):
        """Swap cell x1,y1 with cell x2,y2
        cell on x1,y1 is always an empty cell (0)"""
        self.grid[x1][y1] = self.grid[x2][y2]
        self.grid[x2][y2] = "0"
        
###########################################       
    def can_move_top(self, x, y):
        """Check if we can move the empty cell up, by checking if there is 
        no border up, or an other empty cell. If the action can be done, it 
        returns the direction and the size of the cell which is on top of 
        the empty cell we want to move.
        "dir" can be -1, 0, or 1. If -1, it means the block up to the empty cell
        continues on left. If 1, it continues on the right. If 0, it can only 
        continues up, or be one cell-size.
        "size" defines the size of the block up to the empty cell.
        It can be equal to 1 or 2"""
        cell_value = self.grid[x][y-1]
        dir = 0
        size = 1
        
        if y-2 >= 0 and self.grid[x][y-2] == cell_value:
            size = 2
            
        if x+1 < CONST_WIDTH and self.grid[x+1][y-1] == cell_value: # continues right
            if self.grid[x+1][y] != "0":
                return [False]
            return [True, 1, size]
        
        if x > 0 and self.grid[x-1][y-1] == cell_value: # continues left
            if self.grid[x-1][y] != "0":
                return [False]
            return [True, -1, size]
            
        if not (x+1 < CONST_WIDTH and self.grid[x+1][y-1] == cell_value) and not (x > 0 and self.grid[x-1][y-1] == cell_value): # 1-size cell
            return [True, 0, size]
            
        return [False]
        
###########################################       
    def move_top(self, x, y, dir, size):
        self.move_cell(x, y, x, y-size)
        if dir != 0:
            self.move_cell(x+dir, y, x+dir, y-size)

###########################################       
    def can_move_bottom(self, x, y):
        """Exact same function that can_move_top(..), except that it will 
        check for border down to the empty cell, and not up"""
        cell_value = self.grid[x][y+1]
        dir = 0
        size = 1
        
        if y+2 < CONST_HEIGHT and self.grid[x][y+2] == cell_value:
            size = 2
            
        if x+1 < CONST_WIDTH and self.grid[x+1][y+1] == cell_value: # continues right
            if self.grid[x+1][y] != "0":
                return [False]
            return [True, 1, size]
        
        if x > 0 and self.grid[x-1][y+1] == cell_value: # continues left
            if self.grid[x-1][y] != "0":
                return [False]
            return [True, -1, size]
            
        if not (x+1 < CONST_WIDTH and self.grid[x+1][y+1] == cell_value) and not (x > 0 and self.grid[x-1][y+1] == cell_value): # 1-size cell
            return [True, 0, size]
            
        return [False]
        
###########################################       
    def move_bottom(self, x, y, dir, size):
        self.move_cell(x, y, x, y+size)
        if dir != 0:
            self.move_cell(x+dir, y, x+dir, y+size)

###########################################       
            
    def can_move_left(self, x, y):
        """Difference with can_move_top/bottom(..) :
        "dir" can be -1, 0, or 1. If -1, it means the block left to the empty cell
        continues up. If 1, it continues down. If 0, it can only 
        continues left, or be one cell-size."""
        cell_value = self.grid[x-1][y]
        dir = 0
        size = 1
        
        if x-2 >= 0 and self.grid[x-2][y] == cell_value:
            size = 2
            
        if y+1 < CONST_HEIGHT and self.grid[x-1][y+1] == cell_value: # continues bottom
            if self.grid[x][y+1] != "0":
                return [False]
            return [True, 1, size]
        
        if y > 0 and self.grid[x-1][y-1] == cell_value: # continues top
            if self.grid[x][y-1] != "0":
                return [False]
            return [True, -1, size]
            
        if not (y+1 < CONST_HEIGHT and self.grid[x-1][y+1] == cell_value) and not (y > 0 and self.grid[x-1][y-1] == cell_value): # 1-size cell
            return [True, 0, size]
            
        return [False]
        
###########################################       
    def move_left(self, x, y, dir, size):
        self.move_cell(x, y, x-size, y)
        if dir != 0:
            self.move_cell(x, y+dir, x-size, y+dir)

###########################################       
    def can_move_right(self, x, y):
        """Exact same function that can_move_left(..), except that it will 
        check for border down to the empty cell, and not up"""
        cell_value = self.grid[x+1][y]
        dir = 0
        size = 1
        if x+2 < CONST_WIDTH and self.grid[x+2][y] == cell_value:
            size = 2
            
        if y+1 < CONST_HEIGHT and self.grid[x+1][y+1] == cell_value: # continues bottom
            if self.grid[x][y+1] != "0":
                return [False]
            return [True, 1, size]
        
        if y > 0 and self.grid[x+1][y-1] == cell_value: # continues top
            if self.grid[x][y-1] != "0":
                return [False]
            return [True, -1, size]
            
        if not (y+1 < CONST_HEIGHT and self.grid[x+1][y+1] == cell_value) and not (y > 0 and self.grid[x+1][y-1] == cell_value): # 1-size cell
            return [True, 0, size]
            
        return [False]
        
###########################################       
    def move_right(self, x, y, dir, size):
        self.move_cell(x, y, x+size, y)
        if dir != 0:
            self.move_cell(x, y+dir, x+size, y+dir)

###########################################       
    """Returns the next state, after executing an action (top, bottom, ...)
    with an empty cell (represented by "0" on the grid, located by "x" and "y" variables)
    It returns None if trying a non-authorized action (moving on a border or on another empty cell)"""
    def move(self, x, y, action):
        """Returns the next state, after executing an action (top, bottom, ...)
        with an empty cell (represented by "0" on the grid, located by "x" and "y"
        variables). It returns None if trying a non-authorized action (moving on
        a border or on another empty cell). Otherwise it moves the empty cell(s)
        accordingly to the desired action."""
        new_state = State(deepcopy(self.grid))
        if action == "top":
            move_infos = new_state.can_move_top(x, y)
            if move_infos[0] == True:
                dir = move_infos[1] # If block continues Left == -1, Right == 1
                size = move_infos[2] # size == 1 or 2, depending on the block size
                    
                new_state.move_top(x, y, dir, size)
            else:
                return None
                
        elif action == "bottom":
            move_infos = new_state.can_move_bottom(x, y)
            if move_infos[0] == True:
                dir = move_infos[1] # If block continues Left == -1, Right == 1
                size = move_infos[2] # size == 1 or 2, depending on the block size
                    
                new_state.move_bottom(x, y, dir, size)
            else:
                return None
                
        elif action == "left":
            move_infos = new_state.can_move_left(x, y)
            if move_infos[0] == True:
                dir = move_infos[1] # If block continues Top == -1, Bottom == 1
                size = move_infos[2] # size == 1 or 2, depending on the block size
                    
                new_state.move_left(x, y, dir, size)
            else:
                return None
                
        elif action == "right":
            move_infos = new_state.can_move_right(x, y)
            if move_infos[0] == True:
                dir = move_infos[1] # If block continues Top == -1, Bottom == 1
                size = move_infos[2] # size == 1 or 2, depending on the block size
                    
                new_state.move_right(x, y, dir, size)
            else:
                return None
                
        return new_state

