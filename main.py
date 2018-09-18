from minimax_agent import MinimaxAgent
from random_agent import RandomAgent
import env
import numpy as np
import hex_helpers as hh
import game

board = [
    [-1, -1, 1, 0, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, 0, 0, -1, -1],
    [-1,  0, 0, 0, 0, 0, 0,  0, -1],
    [ 1,  0, 0, 0, 0, 0, 0,  0, -1],
    [ 0,  0, 0, 0, 0, 0, 0,  0,  0],
    [ 0,  0, 0, 0, 0, 0, 0,  0, -1],
    [-1, -1,-1, 0, 0, 0, 0,  0, -1],
    [-1,  0,-1, 0, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, 0, 2, -1, -1]
]

board2 = [
    [-1, 1, 0, 2, -1],
    [0, -1, 0, 0, -1],
    [2, 0, 0, 0, 1],
    [0, 0, 0, -1, -1],
    [-1, 1, 0, 2, -1]
]

state = {
    'board': board2,
    'jumps': [0, 0],
    'adds': [1, 1],
    'current_move': 1
}

agent1 = RandomAgent(1)
agent2 = MinimaxAgent(2, ply=3)

game.play_game(state, agent1, agent2, debug=True)