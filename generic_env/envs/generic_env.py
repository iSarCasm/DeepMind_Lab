import numpy as np
import hex_helpers as hh
import copy
import gym
import time
from gym import spaces

#TODO:stop hardcoding the player
#TODO:generate boards randomly
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

defaultState = {
    'board': board2,
    'jumps': [0, 0],
    'adds': [1, 1],
    'current_move': 1
}
state = defaultState

#AGENT IS ALWAYS PLAYER 1
class GenericEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Tuple([spaces.Discrete(2), spaces.Discrete(2)])
        self.action_space = moves(1, state)
        #TODO: set box shape to actual board size
        self.observation_space = spaces.Tuple([
            spaces.Box(low=-1, high=2, shape=(50,50), dtype=int),
            spaces.Box(low=-1, high=2, shape=(50,50), dtype=int)
        ])
        
        self.observation_space = state['board'] #is this right
        self.reward_range = [0, 25*25] #score is reward???
        self.metadata = self.metadata #???
        
        #opposition AI
        self.enemyAI = MinimaxAgent(2, ply=1)
        return
    def step(self, action, debug=0):
        global state
        
        state = apply_move(action, state)
        #Greedy AI processing
        move = self.enemyAI.select_move(state, debug)
        state = apply_move(move, state)
        if debug:
            print(is_done(state))
        reward = score(1, state)
        done = is_done(state)
        self.action_space = moves(1, state)
        self.observation_space = state['board']

        return self.observation_space, reward, done, 0
    def reset(self):
        state = defaultState
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
            space.
        """
        return self.observation_space
    def render(self, mode='human', close=False):
        return

#TODO:Put in a different module???(can't right now because of circular dependency)
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
        all_my_moves = moves(2, cstate)
        actions = []

        for m in all_my_moves:
            self.states_evaluated += 1
            new_state = apply_move(m, cstate)
            scores = self.minimax(new_state, self.ply-1)
            actions.append({ 'action': m, 'score': scores, 'immediate_score': score(self.player, new_state)})
        best_action = max(actions, key=lambda p: (p['score'], p['immediate_score']))
        return best_action['action']

    def minimax(self, state, depth=-1):
        player = self.player
        if is_done(state) or depth == 0:
            return score(player, state)
        else:
            actions = moves(2, state)
            scores = []
            for a in actions:
                self.states_evaluated += 1
                s = apply_move(a, state)
                scores.append(self.minimax(s, depth=depth-1))

            if player == self.player:
                maximum = np.argmax(scores)
                return scores[maximum]
            else:
                minimum = np.argmin(scores)
                return scores[minimum]
            
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
    pcells = hh.player_cells(player, board)
    moves = [{'type': 'skip', 'player': player}]
    for cell in pcells:
        one_step_cells = hh.neighbours(cell[0], cell[1], board, dist=1)
        one_step_cells = hh.available_cells(one_step_cells)
        for c1 in one_step_cells:
            moves.append({ 'type': 'add', 'player': player, 'fx': cell[0], 'fy': cell[1], 'tx': c1[0], 'ty': c1[1] })
        if state['jumps'][player-1] > 0:
            two_step_cells = hh.neighbours(cell[0], cell[1], board, dist=2) - set(one_step_cells)
            two_step_cells = hh.available_cells(two_step_cells)
            for c2 in two_step_cells:
                moves.append({ 'type': 'jump', 'player': player, 'fx': cell[0], 'fy': cell[1], 'tx': c2[0], 'ty': c2[1] })
    return moves

# STATE, MOVE -> STATE
def apply_move(move, state):
    new_state = copy.deepcopy(state)
    board = new_state['board']
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
            nbrs = hh.neighbours(tx, ty, board)
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
            nbrs = hh.neighbours(tx, ty, board)
            for cell in nbrs:
                x = cell[0]
                y = cell[1]
                if board[y][x] == opponent:
                    board[y][x] = player

    new_state['current_move'] = opponent
    return new_state

# STATE -> boolean
def is_done(state):
    return len(moves(1, state)) == 1 and len(moves(2, state)) == 1

# STATE -> score NUMBER
def score(player, state):
    board = state['board']
    b = np.array(board)
    unique, counts = np.unique(b, return_counts=True)
    d = dict(zip(unique, counts))
    return d.get(player, 0)