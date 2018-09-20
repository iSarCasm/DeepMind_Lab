import numpy as np
import hex_helpers as hh
import copy
import gym
import time
import copy
from gym import spaces
from minimax_agent import MinimaxAgent
from hybrid_minimax_agent import HybridMinimaxAgent
from generic_env_helpers import apply_move, all_moves, is_done, score, winner, AGENT_ID, OPPENENT_ID
from state_generator import generate_state, observation_from_state

class MinGenericEnv(gym.Env):
    def __init__(self):
        global OPPENENT_ID
        global AGENT_ID
        self.metadata = "useless crap"
        self.enemyAI = MinimaxAgent(OPPENENT_ID, ply=1)
        self.innerAI = HybridMinimaxAgent(AGENT_ID, ply=1)
        self.reset()

    """
    Resets the state of the environment and returns an initial observation.
    Returns: observation (object): the initial observation of the
        space.
    """
    def reset(self):
        # self.state = copy.deepcopy(defaultState)
        self.state = generate_state(size = 10)
        self.update_spaces()
        self.observation = observation_from_state(self.state)
        self.reward = 0
        return self.observation

    def step(self, action, debug=0):

        is_jump = action == 1

        move = self.innerAI.select_move(self.observation, is_jump=is_jump, debug = debug)
        if move[0] == 'skip':
            return self.observation, -10, True, 0
        self.observation, mv_error = apply_move(move, AGENT_ID, self.observation)
        if debug:
            print(self.state)
        #Greedy AI processing
        move = self.enemyAI.select_move(self.observation, debug)
        self.observation, _ = apply_move(move, OPPENENT_ID, self.observation)
        done = is_done(self.observation)
        self.reward = winner(AGENT_ID, self.observation)
        if(mv_error == True):
            done = True
            self.reward = -20
        if debug:
            print(done)
        # self.action_space = moves(1, self.state) - THIS SHOULD BE STATIC I BELIEVE
        return self.observation, self.reward, done, 0

    """
    We dont use this crap
    """
    def render(self, mode='human', close=False):
        return

    # "PRIVATE" methods

    def update_spaces(self):
        height = len(self.state['board'])
        width = len(self.state['board'][0])
        self.action_space = spaces.Discrete(2) # number of actions from 0 to all_moves.size
        self.observation_space = spaces.Box(low=-1.0, high=10.0, shape=(1,height * height + 5), dtype=np.int8)
        self.reward_range = [-1, 1]