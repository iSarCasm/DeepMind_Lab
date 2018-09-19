import numpy as np
import hex_helpers as hh
import copy
import gym
import time
import copy


#AGENT IS ALWAYS PLAYER 1
AGENT_ID = 1
OPPENENT_ID = 2
# STATE -> all moves including illegal
# TODO: only all possible adds and jumps. Right now it includes jumps and adds between ANY cells
def all_moves(state):
    board = state['board']
    height = len(board)
    width = len(board[0])
    moves = [{'type': 'skip'}]
    for fy in range(height):
      for fx in range(width):
        one_step_cells = hh.neighbours(fx, fy, board, dist=1)
        for c1 in one_step_cells:
          moves.append({ 'type': 'add', 'fx': fx, 'fy': fy, 'tx': c1[0], 'ty': c1[1] })

        two_step_cells = hh.neighbours(fx, fy, board, dist=2) - set(one_step_cells)
        for c2 in two_step_cells:
            moves.append({ 'type': 'jump', 'fx': fx, 'fy': fy, 'tx': c2[0], 'ty': c2[1] })

    return moves

# PLAYER, STATE -> current legal MOVES
def legal_moves(player, state):
    board = state['board']
    pcells = hh.player_cells(player, board)
    moves = [{'type': 'skip'}]
    for cell in pcells:
        one_step_cells = hh.neighbours(cell[0], cell[1], board, dist=1)
        one_step_cells = hh.available_cells(one_step_cells)
        for c1 in one_step_cells:
            moves.append({ 'type': 'add', 'fx': cell[0], 'fy': cell[1], 'tx': c1[0], 'ty': c1[1] })
        if state['jumps'][player-1] > 0:
            two_step_cells = hh.neighbours(cell[0], cell[1], board, dist=2) - set(one_step_cells)
            two_step_cells = hh.available_cells(two_step_cells)
            for c2 in two_step_cells:
                moves.append({ 'type': 'jump', 'fx': cell[0], 'fy': cell[1], 'tx': c2[0], 'ty': c2[1] })
    return moves


# STATE, PLAYER, MOVE -> STATE, MOVE_ERROR
def apply_move(move, player, state):
    global AGENT_ID
    new_state = copy.deepcopy(state)
    board = new_state['board']
    opponent = 1 if player == 2 else 2
    current_move = new_state['current_move']
    new_state['current_move'] = opponent
    if current_move != player:
        raise ValueError('Not your move')

    if move['type'] != 'skip':
        fx = move['fx']
        fy = move['fy']
        tx = move['tx']
        ty = move['ty']

        if board[fy][fx] != player:
            #only ai moves can be wrong, agent is just punished
            if player == AGENT_ID:
                return new_state, True
            else:
                raise ValueError('Player made move not from his cell')
        if board[ty][tx] == -1:
            if player == AGENT_ID:
                return new_state, True
            else:
                raise ValueError('Forbidden cell')


        if move['type'] == 'add':
            state['adds'][player-1]+=1
            if state['adds'][player-1] == 2:
                state['adds'][player-1] = 0
                state['jumps'][player-1] += 1

            board[ty][tx] = player
            nbrs = hh.neighbours(tx, ty, board)
            for cell in nbrs:
                x = cell[0]
                y = cell[1]
                if board[y][x] == opponent:
                    board[y][x] = player
        elif move['type'] == 'jump':
            if new_state['jumps'][player-1] < 1:
                if player == AGENT_ID:
                    return new_state, True
                else:
                    raise ValueError('Not enough jumps')

            board[fy][fx] = 0
            board[ty][tx] = player
            new_state['jumps'][player-1] -= 1
            nbrs = hh.neighbours(tx, ty, board)
            for cell in nbrs:
                x = cell[0]
                y = cell[1]
                if board[y][x] == opponent:
                    board[y][x] = player

    return new_state, False

# STATE -> boolean
def is_done(state):
    return len(legal_moves(1, state)) == 1 or len(legal_moves(2, state)) == 1

# STATE -> score NUMBER
def score(player, state):
    board = state['board']
    b = np.array(board)
    unique, counts = np.unique(b, return_counts=True)
    d = dict(zip(unique, counts))
    return d.get(player, 0)

def current_player(state):
    return state['current_move']

def current_opponent(player):
    if player == 1:
        return 2
    else:
        return 1