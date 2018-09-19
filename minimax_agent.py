import copy
import time
import numpy as np
import generic_env_helpers as env


class MinimaxAgent:
    def __init__(self, player, ply=1):
        self.player = player
        self.ply = ply
        self.states_evaluated = 0
        self.actions_taken = 0

    def select_move(self, state, debug=False):
        self.states_evaluated = 0
        t1 = time.time()
        if debug:
            print('Agent {} making move...'.format(self.player))
        action = self.look_forward(state)
        if debug:
            print(action)
            print('States evalueated - {}'.format(self.states_evaluated))
            print('Time taken: {}'.format(time.time() - t1))
        return action

    def look_forward(self, state):
        cstate = copy.deepcopy(state)
        all_my_moves = env.legal_moves(self.player, cstate)
        actions = []

        for m in all_my_moves:
            self.states_evaluated += 1
            new_state, _ = env.apply_move(m, self.player, cstate)
            score = self.minimax(new_state, self.ply-1)
            actions.append({ 'action': m, 'score': score, 'immediate_score': env.score(self.player, new_state)})
        best_action = max(actions, key=lambda p: (p['score'], p['immediate_score']))
        return best_action['action']

    def minimax(self, state, depth=-1):
        player = env.current_player(state)
        if env.is_done(state) or depth == 0:
            return env.score(self.player, state)
        else:
            actions = env.legal_moves(player, state)
            scores = []
            for a in actions:
                self.states_evaluated += 1
                s, _ = env.apply_move(a, state)
                score = self.minimax(s, depth=depth-1)
                scores.append(score)

            if player == self.player:
                maximum = np.argmax(scores)
                return scores[maximum]
            else:
                minimum = np.argmin(scores)
                return scores[minimum]