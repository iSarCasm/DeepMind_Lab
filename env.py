import numpy as np
import hex_helpers as hh
import copy

def player(state):
    return state['current_move']

def opponent(player):
    if player == 1:
        return 2
    else:
        return 1

# PLAYER, STATE -> legal MOVES
def moves(player, state):
    board = state['board']
    size = len(board)
    pcells = hh.player_cells(player, board)
    moves = [{'type': 'skip', 'player': player}]
    for cell in pcells:
        one_step_cells = hh.neighbours(cell[0], cell[1], size, dist=1)
        one_step_cells = hh.available_cells(one_step_cells, board)
        for c1 in one_step_cells:
            moves.append({ 'type': 'add', 'player': player, 'fx': cell[0], 'fy': cell[1], 'tx': c1[0], 'ty': c1[1] })
        if state['jumps'][player-1] > 0:
            two_step_cells = hh.neighbours(cell[0], cell[1], size, dist=2) - set(one_step_cells)
            two_step_cells = hh.available_cells(two_step_cells, board)
            for c2 in two_step_cells:
                moves.append({ 'type': 'jump', 'player': player, 'fx': cell[0], 'fy': cell[1], 'tx': c2[0], 'ty': c2[1] })
    return moves

# STATE, MOVE -> STATE
def apply_move(move, state):
    new_state = copy.deepcopy(state)
    board = new_state['board']
    size = len(board)
    player = move['player']
    opponent = 1 if player == 2 else 2

    if new_state['current_move'] != player:
        raise ValueError('Not your move')

    if move['type'] != 'skip':
        fx = move['fx']
        fy = move['fy']
        tx = move['tx']
        ty = move['ty']

        if board[fy][fx] != player:
            raise ValueError('Wrong player made move')
        if board[ty][tx] == -1:
            raise ValueError('Forbidden cell')

        if move['type'] == 'add':
            state['adds'][player-1]+=1
            if state['adds'][player-1] == 2:
                state['adds'][player-1] = 0
                state['jumps'][player-1] += 1

            board[ty][tx] = player
            nbrs = hh.neighbours(tx, ty, size)
            for cell in nbrs:
                x = cell[0]
                y = cell[1]
                if board[y][x] == opponent:
                    board[y][x] = player
        elif move['type'] == 'jump':
            if new_state['jumps'][player-1] < 1:
                raise ValueError('Not enough jumps')

            board[fy][fx] = 0
            board[ty][tx] = player
            new_state['jumps'][player-1] -= 1
            nbrs = hh.neighbours(tx, ty, size)
            for cell in nbrs:
                x = cell[0]
                y = cell[1]
                if board[y][x] == opponent:
                    board[y][x] = player

    new_state['current_move'] = opponent
    return new_state

# STATE -> boolean
def is_done(state):
    return len(moves(1, state)) == 1 or len(moves(2, state)) == 1

# STATE -> score NUMBER
def score(player, state):
    board = state['board']
    b = np.array(board)
    unique, counts = np.unique(b, return_counts=True)
    d = dict(zip(unique, counts))
    return d.get(player, 0)