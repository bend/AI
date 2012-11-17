#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import math

from sarena import *
import minimax
import heapq
import time

SUCC_LIM =30 #Take approx. 1/3 of the successors

class SuperPlayer(Player, minimax.Game):
    step            = 0
    max_depth       = 3
    old_max_depth   = 1
    start_time      = 0
    time_slot       = 0
    time_left       = 0


    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    Board:

        [TYPE:3(classical)|4(Return), [Couleu_bas, Couleur_haut]*4]
        Couleur = 0 == pas de pion

    """

    def successors(self, state):
        """ Returns actions ordered by evaluation depending of MIN/MAX score to prune more with aplha beta
            We Also leave only SUCC_LIM actions per depth 
        """
        board, player = state
        heap = []
        i = 0
        # Get the next player
        next_player = -player
        for action in board.get_actions():
            new_board = board.clone().play_action(action)
            i+=1
            score = self.evaluate((new_board, next_player))
            if(self.player == player): # if MAX
                # heap sorts descending to ascending, so we invert the score
                heapq.heappush(heap, (-score, (action, (new_board, next_player))))
            else: # if MIN
                # heap sorts ascending to descending so we invert the score
                heapq.heappush(heap, (score, (action, (new_board, next_player))))
        if i > SUCC_LIM:
            i = SUCC_LIM 
        
        for x in range(i):
            yield heapq.heappop(heap)[1] # yield value without the key       

    def cutoff(self, state, depth):
        # Faut se baser sur le temps restant, la depth, 
        # Au debut il faut mettre une depth < que a la fin
        board, player = state
        play_time = time.time() - self.start_time 
        if depth > 0 and self.step < 2:
            return True
        #print("play time is ", play_time, "depth is ",depth, "md : ",self.max_depth)
        return (play_time >= self.time_slot) or board.is_finished() or self.max_depth == depth

    def evaluate(self, state):
        board, player = state
        score = board.get_score()
        old_score = score
        # Do not evaluate this before step 2 because it won't happen
        if self.step < 2:
            return score
        # If We have non moveable complete tower with player's color 
        # Increment score
        for i,j,tower in board.get_towers():
            if not board.is_tower_movable(i,j):
                h = board.get_height(board.m[i][j])
                if tower[4][1] == 1:
                    score+=8
                elif tower[4][1] == -1: #Check if oponent has full towers
                    score-=8
                # Check Right
                elif h == 3:
                    #test if the tower is not surrounded by any chip
                    if tower[h][1] == 1 and\
                    self.check_right(board,i,j) == None and \
                    self.check_left(board, i, j) == None and \
                    self.check_up(board, i, j) == None and \
                    self.check_down(board, i, j) == None:
                        score+=h
                    else: #Check if a near chip is from oponent because we can suppose that he will counter this move
                        left = self.left(board, i, j)
                        right = self.right(board, i,j)
                        up = self.up(board, i,j)
                        down = self.down(board, i,j)
                        if (left != None and board.get_height(left) == 1 and left[1][1] == -1) or \
                        (right != None and board.get_height(right) == 1 and right[1][1] == -1) or\
                        (up != None and board.get_height(up) == 1 and up[1][1] == -1) or\
                        (down != None and board.get_height(down) == 1 and down[1][1] == -1):
                            score-=h

            else: #Tower is movable
                if tower[4][1] == 1: #Tower can be reversed
                    if tower[1][0] == 1: #Reversing tower will give us points and is the only possible move
                        score+=4
                    elif tower[1][0] == -1: #Reversing the tower will give points to the opponent
                        score-=4
        return score

    def check_right(self,board, i,j):
        """ Checks whether the right cell is empty of not
            returns None if there are to tiles on the cell or if out of bounds
            returns True if there is a tile on the cell
        """
        if j+1 < board.columns:
            if board.get_height(board.m[i][j+1]) == 0:
                return None
            else:
                return True
        else:
            return None
    
    def left(self, board, i, j):
        """ Get the left tile 
            Return None if no tile
        """
        if j+1 < board.columns:
            return board.m[i][j+1]
        else:
            return None

    def check_left(self, board,i,j):
        """ Checks whether the left cell is empty of not
            returns None if there are to tiles on the cell or if out of bounds
            returns True if there is a tile on the cell
        """
        if j > 0:
            if board.get_height(board.m[i][j-1]) == 0:
                return None
            else:
                return True
        else:
            return None

    def right(self, board, i, j):
        """ Get the right  tile
            Return None if no tile
        """
        if j > 0:
            return board.m[i][j-1]
        else:
            return None


    def check_up(self, board,i, j):
        """ Checks whether the upper cell is empty of not
            returns None if there are to tiles on the cell or if out of bounds
            returns True if there is a tile on the cell
        """
        if i > 0:
            if board.get_height(board.m[i-1][j]) == 0:
                return None
            else:
                return True
        else:
            return None
    
    def up(self, board, i, j):
        """ Get the up tile 
            Return None if no tile
        """
        if i > 0:
            return board.m[i-1][j]
        else:
            return None

    def check_down(self, board,i, j):
        """ Checks whether the down cell is empty of not
            returns None if there are to tiles on the cell or if out of bounds
            returns True if there is a tile on the cell
        """
        if i+1 < board.rows:
            if board.get_height(board.m[i+1][j]) == 0:
                return None
            else:
                return True
        else:
            return None
    
    def down(self, board, i, j):
        """ Get the down tile 
            Return None if no tile
        """
        if i+1 < board.rows:
            return board.m[i+1][j]
        else:
            return None

    def play(self, percepts, step, time_left):
        
        ###BENCH

        #return self.eval_speed(percepts,step,time_left);

        if step % 2 == 0:
            player = -1 # Red
        else:
            player = 1  #Yellow
        # Game is new reset vars 
        if step == 1 or step == 2:
            self.step            = 0
            self.max_depth       = 4
            self.start_time      = 0
            self.time_slot       = 0
            self.time_left       = 0

        state = (Board(percepts), player)
        self.player = player
        self.step = step
        self.time_left = time_left
        self.start_time = time.time()
        i = 15 - step #15 because we rarely have more than 15 steps to compute for a player
        if i <=0:
            i = 1
        self.time_slot = math.floor(time_left / (i))  # Time_left / Number of steps left (approx.)
        return minimax.search(state, self, True)


if __name__ == "__main__":
     player_main(SuperPlayer())
