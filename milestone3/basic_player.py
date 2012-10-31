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
        for i in board.get_actions():
            print("successsor")
            yield (i, (board.clone().play_action(i), player))
            



    def cutoff(self, state, depth):
        print("cutoff")
        board, player = state
        return board.is_finished()

    def evaluate(self, state):
        print("evaluate")
        board, player = state
        return board.get_score()

    def play(self, percepts, step, time_left):
        print("play")
        if step % 2 == 0:
            player = -1
        else:
            player = 1
        state = (Board(percepts), player)
        return minimax.search(state, self)


if __name__ == "__main__":
    player_main(AlphaBetaPlayer())
