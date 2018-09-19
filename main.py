import gym
import generic_env
from random import randint
from baselines import deepq

def callback(lcl, _glb):
    #TODO:figure out what score is "solved game"
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved

env = gym.make('GenericEnv-v1')
act = deepq.learn(
    env,
    network='mlp',
    lr=1e-3,
    total_timesteps=100000,
    buffer_size=50000,
    exploration_fraction=0.1,
    exploration_final_eps=0.02,
    print_freq=10,
    callback=callback
)
print("\n=====\nSaving model to generic_env_model.pkl\n=====\n")
act.save("generic_env_model.pkl")