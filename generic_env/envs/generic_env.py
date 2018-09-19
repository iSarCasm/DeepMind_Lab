import numpy as np
import hex_helpers as hh
import copy
import gym
import time
import copy
from gym import spaces
from minimax_agent import MinimaxAgent
from generic_env_helpers import apply_move, all_moves, is_done, score

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

#AGENT IS ALWAYS PLAYER 1
AGENT_ID = 1
OPPENENT_ID = 2
class GenericEnv(gym.Env):
    def __init__(self):
        self.metadata = "useless crap"
        self.enemyAI = MinimaxAgent(OPPENENT_ID, ply=1)
        self.reset()

    """
    Resets the state of the environment and returns an initial observation.
    Returns: observation (object): the initial observation of the
        space.
    """
    def reset(self):
        self.state = copy.deepcopy(defaultState)
        self.update_spaces()
        self.all_moves = all_moves(self.state)
        return self.observation_space

    def step(self, action, debug=0):
        move = self.action_to_move(action)
        self.state = apply_move(move, AGENT_ID, self.state)
        #Greedy AI processing
        move = self.enemyAI.select_move(self.state, debug)
        self.state = apply_move(move, OPPENENT_ID, self.state)
        reward = score(AGENT_ID, self.state) - score(OPPENENT_ID, self.state)
        done = is_done(self.state)
        if debug:
            print(done)
        # self.action_space = moves(1, self.state) - THIS SHOULD BE STATIC I BELIEVE
        self.observation = self.observation_from_state()
        return self.observation, reward, done, 0

    """
    We dont use this crap
    """
    def render(self, mode='human', close=False):
        return

    # "PRIVATE" methods

    """
    Not confusing naming at all
    """
    def action_to_move(self, action):
        move = self.all_moves[action]
        return move

    """
    This is what makes sense to show to an agent
    """
    def observation_from_state(self):
        observation = []
        board = np.array(self.state['board']).flatten()
        jumps = np.array(self.state['jumps'])
        adds = np.array(self.state['adds'])
        observation.extend(board)
        observation.extend(jumps)
        observation.extend(adds)
        # CURRENT OBSERVATION: [-1, 1, 0, 2, -1, 0, -1, 0, 2, -1, 2, 0, 0, 0, 2, 0, 0, 0, -1, -1, -1, 1, 1, 1, -1, 0, 0, 1, 1]
        return observation

    def update_spaces(self):
        height = len(self.state['board'])
        width = len(self.state['board'][0])
        # self.action_space = moves(1, state) THIS SHOULD BE FIXED-SIZE SOMEHOW - ALL POSSIBLE/IMPOSSIBLE MOVEs
        # The RL agent cant use our `moves` because it can work only with
        # static action_space shape and static observation_space shape
        # Long array of all possible moves for this board (including illegal) - (see `all_moves` func).
        moves_count = len(all_moves(self.state))
        print('Move count: ', moves_count)
        self.action_space = spaces.Discrete(moves_count) # number of actions from 0 to all_moves.size
        # board value range from -(1 to 2) = (0 to 3) = 3
        # but adds from 0 to 1
        # and jump 0 to Inf
        # so let it be 5. Also see `observation_from_state`
        self.observation_space = spaces.Discrete(5)
        self.reward_range = [-25*25, 25*25] #score is reward???