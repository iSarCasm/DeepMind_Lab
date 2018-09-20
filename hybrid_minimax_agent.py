import copy
import time
import numpy as np
import generic_env_helpers as env


class HybridMinimaxAgent:
    def __init__(self, player, ply=1):
        self.player = player
        self.ply = ply
        self.states_evaluated = 0
        self.actions_taken = 0

    def select_move(self, observation, is_jump = False, debug=False):
        self.states_evaluated = 0
        t1 = time.time()
        if debug:
            print('Agent {} making move...'.format(self.player))
        action = self.look_forward(observation, is_jump)
        if debug:
            print(action)
            print('States evalueated - {}'.format(self.states_evaluated))
            print('Time taken: {}'.format(time.time() - t1))
        return action

    def look_forward(self, observation, is_jump):
        all_my_moves = env.legal_moves(self.player, observation, all = False, is_jump = is_jump)
        actions = []

        for m in all_my_moves:
            self.states_evaluated += 1
            new_observation, _ = env.apply_move(m, self.player, observation)
            score = self.minimax(new_observation, self.ply-1)
            actions.append({ 'action': m, 'score': score, 'immediate_score': env.score(self.player, new_observation)})
        best_action = max(actions, key=lambda p: (p['score'], p['immediate_score']))
        return best_action['action']

    def minimax(self, observation, depth=-1):
        player = env.current_player(observation)
        if env.is_done(observation) or depth == 0:
            return env.score(self.player, observation)
        else:
            actions = env.legal_moves(player, observation)
            scores = []
            for a in actions:
                self.states_evaluated += 1
                s, _ = env.apply_move(a, observation)
                score = self.minimax(s, depth=depth-1)
                scores.append(score)

            if player == self.player:
                maximum = np.argmax(scores)
                return scores[maximum]
            else:
                minimum = np.argmin(scores)
                return scores[minimum]