#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import math

from sarena import *
import minimax
import heapq
import time

LIMIT_OF_SUCC =10

class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    Board:

        [TYPE:3(classical)|4(Return), [Couleu_bas, Couleur_haut]*4]
        Couleur = 0 == pas de pion

    """

    def successors(self, state):
        """must return actions ordered by evaluation depending of MIN/MAX score to prune more with aplha beta"""
        board, player = state
        heap = []
        i = 0
        # Get the next player
        next_player = -player
        print(next_player)
        for action in board.get_actions():
            new_board = board.clone().play_action(action)
            i+=1
            score = self.evaluate((new_board, next_player))
            if(self.player == player): # if MAX
                # heap sorts descending to ascending, so we invert the score
                heapq.heappush(heap, (-score, (action, (new_board, next_player))))
            else: # if MIN
                heapq.heappush(heap, (score, (action, (new_board, next_player))))
        
        if i > LIMIT_OF_SUCC:
            i = LIMIT_OF_SUCC 
        for x in range(i):
            yield heapq.heappop(heap)[1] # yield value without the key       

    def cutoff(self, state, depth):
        #print("cutoff")
        # Faut se baser sur le temps restant, la depth, 
        # Au debut il faut mettre une depth < que a la fin
        board, player = state
        max_depth = 0 + math.floor(self.step/5)
        if depth > max_depth:
            return True
        return board.is_finished()

    def evaluate(self, state):
        #print("evaluate")
        board, player = state
        score = board.get_score()
        if self.step < 2:
            #print("evaluate score ",score)
            return score
        # If We have non moveable complete tower with our color 
        # Increment score
        for i,j,tower in board.get_towers():
            if not board.is_tower_movable(i,j):
                if tower[4] == player:
                    #print("evaluate tower")
                    score+=4
                #test if the tower is not surrounded by any chip
                # Check Right
                if board.get_height(board.m[i][j]) >= 2:
                    if self.check_right(board,i,j) == None and self.check_left(board, i, j) == None and self.check_up(board, i, j) == None and self.check_down(board, i, j) == None:
                        score+=2
                        #print("evaluate check")
                
        #print("evaluate score ",score)
        return score
                

    # Returns True if the cell to the right is occupied, otherwise it returns None
    def check_right(self,board, i,j):
        #print("check right")
        if j+1 < board.columns:
            if board.get_height(board.m[i][j+1]) == 0:
                return None
            else:
                return True
        else:
            return None

    def check_left(self, board,i,j):
        #print("check left")
        if j > 0:
            if board.get_height(board.m[i][j-1]) == 0:
                return None
            else:
                return True
        else:
            return None

    def check_up(self, board,i, j):
        #print("check up")
        if i > 0:
            if board.get_height(board.m[i-1][j]) == 0:
                return None
            else:
                return True
        else:
            return None

    def check_down(self, board,i, j):
        #print("check down")
        if i+1 < board.rows:
            if board.get_height(board.m[i+1][j]) == 0:
                return None
            else:
                return True
        else:
            return None


    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1 # Red
            print("player is red")
        else:
            player = 1  #Yellow
            print("player is yellow")
        state = (Board(percepts), player)
        self.player = player
        self.step = step
        self.time_left = time_left
        return minimax.search(state, self, True)


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
