import numpy as np
import hex_helpers as hh
import copy
import gym
import time
import copy
from functools import lru_cache
from state_generator import observation_from_state, state_from_observation


#AGENT IS ALWAYS PLAYER 1
AGENT_ID = 1
OPPENENT_ID = 2
# STATE -> all moves including illegal
# TODO: only all possible adds and jumps. Right now it includes jumps and adds between ANY cells
def all_moves(state):
    board = state['board']
    board_size = len(board)
    moves = [] #[{'type': 'skip'}]
    for fy in range(board_size):
      for fx in range(board_size):
        one_step_cells = hh.neighbours(fx, fy, board_size, dist=1)
        for c1 in one_step_cells:
            # MOVE [TYPE, FX, FY, TX, TY]
            moves.append(('add', fx, fy, c1[0], c1[1]))

        two_step_cells = hh.neighbours(fx, fy, board_size, dist=2) - set(one_step_cells)
        for c2 in two_step_cells:
            # MOVE [TYPE, FX, FY, TX, TY]
            moves.append(('jump', fx, fy, c2[0], c2[1]))

    return moves

# PLAYER, STATE -> current legal MOVES
# @lru_cache(maxsize=32000)
def legal_moves(player, observation, all = True, is_jump = False):
    state = state_from_observation(observation)
    board = state['board']
    board_size = len(board)
    pcells = hh.player_cells(player, board)
    # MOVE [TYPE, FX, FY, TX, TY]
    moves = [('skip', 0, 0, 0, 0)]
    for cell in pcells:
        one_step_cells = hh.neighbours(cell[0], cell[1], board_size, dist=1)
        one_step_cells = hh.available_cells(one_step_cells, board)
        if (all or not is_jump):
            for c1 in one_step_cells:
                # MOVE [TYPE, FX, FY, TX, TY]
                moves.append(('add', cell[0], cell[1], c1[0], c1[1]))
        if (all or is_jump):
            if state['jumps'][player-1] > 0:
                two_step_cells = hh.neighbours(cell[0], cell[1], board_size, dist=2) - set(one_step_cells)
                two_step_cells = hh.available_cells(two_step_cells, board)
                for c2 in two_step_cells:
                    # MOVE [TYPE, FX, FY, TX, TY]
                    moves.append(('jump', cell[0], cell[1], c2[0], c2[1]))
    # print(legal_moves.cache_info())
    return moves


# STATE, PLAYER, MOVE -> STATE, MOVE_ERROR
@lru_cache(maxsize=32000)
def apply_move(move, player, observation):
    global AGENT_ID
    new_state = state_from_observation(observation)
    board = new_state['board']
    board_size = len(board)
    opponent = 1 if player == 2 else 2
    current_move = new_state['current_move']
    invalid_move = False
    for _ in range(1):
        if current_move != player:
            raise ValueError('Not your move')

        move_type = move[0]
        if move_type != 'skip':
            fx = move[1]
            fy = move[2]
            tx = move[3]
            ty = move[4]

            if board[fy][fx] != player:
                #only ai moves can be wrong, agent is just punished
                if player == AGENT_ID:
                    invalid_move = True
                    break
                else:
                    raise ValueError('Player made move not from his cell')
            if board[ty][tx] != 0:
                if player == AGENT_ID:
                    invalid_move = True
                    break
                else:
                    raise ValueError('Forbidden cell')


            if move_type == 'add':
                new_state['adds'][player-1]+=1
                if new_state['adds'][player-1] == 2:
                    new_state['adds'][player-1] = 0
                    new_state['jumps'][player-1] += 1

                board[ty][tx] = player
                nbrs = hh.neighbours(tx, ty, board_size)
                for cell in nbrs:
                    x = cell[0]
                    y = cell[1]
                    if board[y][x] == opponent:
                        board[y][x] = player
            elif move_type == 'jump':
                if new_state['jumps'][player-1] < 1:
                    if player == AGENT_ID:
                        invalid_move = True
                        break
                    else:
                        raise ValueError('Not enough jumps')

                board[fy][fx] = 0
                board[ty][tx] = player
                new_state['jumps'][player-1] -= 1
                nbrs = hh.neighbours(tx, ty, board_size)
                for cell in nbrs:
                    x = cell[0]
                    y = cell[1]
                    if board[y][x] == opponent:
                        board[y][x] = player

    new_state['current_move'] = opponent
    new_observation = observation_from_state(new_state)
    # print(apply_move.cache_info())
    return new_observation, invalid_move

# STATE -> boolean
@lru_cache(maxsize=32000)
def is_done(observation):
    return len(legal_moves(1, observation)) == 1 or len(legal_moves(2, observation)) == 1

@lru_cache(maxsize=32000)
def winner(current_player, observation):
    if is_done(observation):
        opponent = 1 if current_player == 2 else 2
        score_me = score(current_player, observation)
        scope_op = score(opponent, observation)
        if score_me == scope_op:
            return 0
        elif scope_op > score_me:
            return -1
        else:
            return +1
    else:
        return 0

# STATE -> score NUMBER
@lru_cache(maxsize=32000)
def score(player, observation):
    state = state_from_observation(observation)
    board = state['board']
    b = np.array(board)
    unique, counts = np.unique(b, return_counts=True)
    d = dict(zip(unique, counts))
    return d.get(player, 0)

@lru_cache(maxsize=32000)
def current_player(observation):
    state = state_from_observation(observation)
    return state['current_move']
