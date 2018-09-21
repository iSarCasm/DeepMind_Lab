import numpy as np
import hex_helpers as hh
import copy
import gym
import time
import copy
from gym import spaces
from minimax_agent import MinimaxAgent
from generic_env_helpers import apply_move, all_moves, is_done, score, AGENT_ID, OPPENENT_ID
from state_generator import generate_state, observation_from_state

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

WRONG_MOVE_PUNISHMENT = -20
class GenericEnv(gym.Env):
    def __init__(self):
        global OPPENENT_ID
        self.metadata = "useless crap"
        self.enemyAI = MinimaxAgent(OPPENENT_ID, ply=1)
        self.reset()

    """
    Resets the state of the environment and returns an initial observation.
    Returns: observation (object): the initial observation of the
        space.
    """
    def reset(self):
        # self.state = copy.deepcopy(defaultState)
        self.state = generate_state(size = 5)
        self.update_spaces()
        self.all_moves = all_moves(self.state)
        self.observation = observation_from_state(self.state)
        return self.observation

    def step(self, action, debug=0):
        if debug:
            print(self.state)
        move = self.action_to_move(action)
        self.observation, mv_error = apply_move(move, AGENT_ID, self.observation)
        if debug:
            print(self.state)
        #Greedy AI processing
        move = self.enemyAI.select_move(self.observation, debug)
        self.observation, _ = apply_move(move, OPPENENT_ID, self.observation)
        reward = score(AGENT_ID, self.observation)
        done = is_done(self.observation)
        if(mv_error == True):
            done = True
            reward = WRONG_MOVE_PUNISHMENT
        if debug:
            print(done)
        # self.action_space = moves(1, self.state) - THIS SHOULD BE STATIC I BELIEVE
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

    def update_spaces(self):
        height = len(self.state['board'])
        width = len(self.state['board'][0])
        # self.action_space = moves(1, state) THIS SHOULD BE FIXED-SIZE SOMEHOW - ALL POSSIBLE/IMPOSSIBLE MOVEs
        # The RL agent cant use our `moves` because it can work only with
        # static action_space shape and static observation_space shape
        # Long array of all possible moves for this board (including illegal) - (see `all_moves` func).
        moves_count = len(all_moves(self.state))
        # print('Move count: ', moves_count)
        self.action_space = spaces.Discrete(moves_count) # number of actions from 0 to all_moves.size
        # board value range from -(1 to 2) = (0 to 3) = 3
        # but adds from 0 to 1
        # and jump 0 to Inf
        # so let it be 5. Also see `observation_from_state`
        self.observation_space = spaces.Box(low=-1.0, high=10.0, shape=(1,height * height + 5), dtype=np.int8) # spaces.Discrete(5)
        self.reward_range = [WRONG_MOVE_PUNISHMENT, -WRONG_MOVE_PUNISHMENT] #score is reward???