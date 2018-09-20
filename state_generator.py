import numpy as np
import random
import math

def generate_state(size=5):
    board = np.zeros((size, size))
    rock_chance = 0.035
    mid_point = size // 5 + 1
    for y in range(size):
        dist = abs(y - mid_point)
        left_rocks = dist // 2
        right_rocks = dist - left_rocks
        for x in range(size):
            left = x
            right = size - x - 1
            if left < left_rocks:
                board[y][x] = -1
            elif right < right_rocks:
                board[y][x] = -1
            else:
                if random.random() <= rock_chance:
                    board[y][x] = -1
                elif random.random() <= 0.15:
                    board[y][x] = 1
                elif random.random() <= 0.15:
                    board[y][x] = 2
    state = {
        'board': board,
        'jumps': [0, 0],
        'adds': [1, 1],
        'current_move': 1
    }
    return state

"""
This is what makes sense to show to an agent
"""
def observation_from_state(state):
    observation = []
    board = np.array(state['board']).flatten()
    jumps = np.array(state['jumps'])
    adds = np.array(state['adds'])
    observation.extend(board)
    observation.extend(jumps)
    observation.extend(adds)
    observation.append(state['current_move'])
    # CURRENT OBSERVATION: [-1, 1, 0, 2, -1, 0, -1, 0, 2, -1, 2, 0, 0, 0, 2, 0, 0, 0, -1, -1, -1, 1, 1, 1, -1, 0, 0, 1, 1]
    return tuple(observation)


def state_from_observation(observation):
    size = int(math.sqrt(len(observation) - 5))
    board = []
    for y in range(size):
        line = []
        for x in range(size):
            line.append(observation[x + y*size])
        board.append(line)

    state = {
        'board': board,
        'jumps': list(observation[-5:-3]),
        'adds': list(observation[-3:-1]),
        'current_move': observation[-1]
    }
    return state