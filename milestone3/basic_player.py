#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from sarena import *
import minimax


class AlphaBetaPlayer(Player, minimax.Game):

    """Sarena Player.

    A state is a tuple (b, p) where p is the player to make a move and b
    the board.

    """

    def successors(self, state):
        board, player = state
        next_player = -player
        for i in board.get_actions():
            yield(i, (board.clone().play_action(i), next_player))
            

    def cutoff(self, state, depth):
        board, player = state
        return board.is_finished()

    def evaluate(self, state):
        board, player = state

        return board.get_score()
                

    def play(self, percepts, step, time_left):
        if step % 2 == 0:
            player = -1
        else:
            player = 1
        state = (Board(percepts), player)
        self.step = step
        self.time_left = time_left
        print(time_left)
        return minimax.search(state, self, True)


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
