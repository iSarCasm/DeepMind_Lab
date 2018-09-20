import gym
import generic_env
import min_generic_env
from random import randint
from baselines import deepq

def callback(lcl, _glb):
    #TODO:figure out what score is "solved game"
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 0.9
    # is_solved = False
    return is_solved

env = gym.make('MinGenericEnv-v1')
act = deepq.learn(
    env,
    network='mlp',
    lr=5e-3, #1e-3
    total_timesteps=20000,
    exploration_fraction=0.98,
    exploration_final_eps=0.0,
    print_freq=5,
    callback=callback,
    buffer_size=50000, # 50000
    learning_starts=100,
    prioritized_replay=True, #False
    batch_size=128 #32
)
print("\n=====\nSaving model to generic_env_model.pkl\n=====\n")
act.save("generic_env_model.pkl")