import env
import copy
import time
import numpy as np
import pprint

class MinimaxAgent:
    def __init__(self, player, ply=1):
        self.player = player
        self.opponent = 1 if player == 2 else 2
        self.ply = ply
        self.states_evaluated = 0
        self.actions_taken = 0
        self.actions = []

    def select_move(self, state, debug=False):
        self.states_evaluated = 0
        t1 = time.time()
        if debug:
            print('Agent {} making move...'.format(self.player))

        cstate = copy.deepcopy(state)
        action = self.alphabeta(cstate, self.ply, -1e10, 1e10, True)

        if debug:
            if debug == 2:
                print(action)
            print('States evalueated - {}'.format(self.states_evaluated))
            print('Time taken: {}'.format(time.time() - t1))
        # print(action)
        return action

    def alphabeta(self, state, depth, alpha, beta, maximizingPlayer):
        if env.is_done(state) or depth == 0:
            return env.score(self.player, state)

        if maximizingPlayer:
            value = -1e10
            actions = env.moves(self.player, state)
            for a in actions:
                self.states_evaluated += 1
                new_state = env.apply_move(a, state)
                score = self.alphabeta(new_state, depth-1, alpha, beta, False)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:
                  break
            return value
        else:
            value = 1e10
            actions = env.moves(self.opponent, state)
            for a in actions:
                self.states_evaluated += 1
                new_state = env.apply_move(a, state)
                score = self.alphabeta(new_state, depth-1, alpha, beta True)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta then
                  break
            return value