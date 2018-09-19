import numpy as np
import random

class StateGenerator:
    @staticmethod
    def generate(size=5):
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

        # N rows with 2 edge cells + Two rows top and bottom
        # points = (size - 2) * 2 + (size - mid_point) * 2
        # player_points = [0] * points
        # player_points[0:5] = [1, 1, 1, 2, 2, 2]
        # previous = -1
        # for y in range(size):
        #     for x in range(size):
        #         current = state[y][x]
        #         if y == 0:
        #             if player_points[x] != 0:
        #                 state[y][x] = player_points[x]
        #         elif y == (size-1):

        #         else:



print(StateGenerator.generate(size=10))