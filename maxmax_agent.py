import mars_env
import copy
import time
import numpy as np
import pprint

class MaxmaxAgent:
    def __init__(self, players, ply=1):
        self.players = players
        self.ply = ply
        self.states_evaluated = 0

    def select_move(self, state, debug=False):
        self.states_evaluated = 0
        t1 = time.time()
        if debug:
            print('Agent {} making move...'.format(self.player))

        cstate = copy.deepcopy(state)
        action, reward = self.maxmax(cstate, self.ply, -1e10, None)

        if debug:
            if debug == 2:
                print([action, reward])
            print('States evalueated - {}'.format(self.states_evaluated))
            print('Time taken: {}'.format(time.time() - t1))
        # print(action)
        return action

    def maxmax(self, state, depth, maxv, selected_action):
        if depth == 0:
            return [selected_action, state.score()]

        all_my_moves = mars_env.moves(self.player, state)
        
        selected_action = None
        for m in all_my_moves:
            new_state = mars_env.apply_move(a, state)
            score = maxmax(state, depth-1)
            if score > maxv:
                maxv = score
                selected_action = m

    def look_forward(self, state):
        all_my_moves = env.moves(self.player, state)
        self.actions = []

        for m in all_my_moves:
            self.states_evaluated += 1
            new_state = env.apply_move(m, state)
            score = self.minimax(new_state, self.ply-1, False)
            self.actions.append({ 'action': m, 'score': score, 'immediate_score': env.score(self.player, new_state)})
        self.actions = sorted(self.actions, key=lambda p: (p['score'], p['immediate_score']))
        print(self.actions)
        best_action = self.actions[-1]
        return best_action['action']

    def minimax(self, state, depth, maximizingPlayer):
        # print("{}: {} {}".format(self.ply, depth, maximizingPlayer))
        if env.is_done(state) or depth == 0:
            return env.score(self.player, state)

        if maximizingPlayer:
            value = -1e10
            actions = env.moves(self.player, state)
            for a in actions:
                self.states_evaluated += 1
                new_state = env.apply_move(a, state)
                score = self.minimax(new_state, depth-1, False)
                value = max(value, score)
            return value
        else:
            value = 1e10
            actions = env.moves(self.opponent, state)
            for a in actions:
                self.states_evaluated += 1
                new_state = env.apply_move(a, state)
                score = self.minimax(new_state, depth-1, True)
                value = min(value, score)
            return value