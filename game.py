import numpy as np
import env

def play_game(state, agent1, agent2, debug=False):
    while True:
        if debug == 2:
            print(np.array(state['board']))
        move = 0
        if state['current_move'] == 1:
            move = agent1.select_move(state, debug=debug)
        else:
            move = agent2.select_move(state, debug=debug)

        state = env.apply_move(move, state)
        if debug:
            print(env.is_done(state))

        if env.is_done(state):
            s1 = env.score(1, state)
            s2 = env.score(2, state)
            if debug:
                print('Game finished. Scores are {} - {}'.format(s1, s2))
            if s1 > s2:
                if debug:
                    print('Player 1 won!')
                return { 'winner': 1, 'score1': s1, 'score2': s2 }
            elif s1 < s2:
                if debug:
                    print('Player 2 won!')
                return { 'winner': 2, 'score1': s1, 'score2': s2 }
            else:
                if debug:
                    print('Tie!')
                return { 'winner': 0, 'score1': s1, 'score2': s2 }