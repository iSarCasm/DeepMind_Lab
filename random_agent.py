import mars_env
import copy
import numpy as np
import random

random.seed

class RandomAgent:
    def __init__(self, player):
        self.player = player

    def select_move(self, state, debug=False):
        if debug:
            print('Agent {} making move...'.format(self.player))
        action = self.look_forward(state)
        if debug:
            print(action)
        return action

    def look_forward(self, state):
        state = copy.deepcopy(state)
        all_my_moves = mars_env.moves(self.player, state)
        r = random.randint(0, len(all_my_moves)-1)
        return all_my_moves[r]