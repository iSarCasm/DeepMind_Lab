import gym
import generic_env
from random import randint
from baselines import deepq

def callback(lcl, _glb):
    #TODO:figure out what score is "solved game"
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    is_solved = False
    return is_solved

env = gym.make('GenericEnv-v1')
act = deepq.learn(
    env,
    network='mlp',
    lr=1e-5, #1e-3
    total_timesteps=300000,
    exploration_fraction=1,
    exploration_final_eps=0.0,
    print_freq=500,
    checkpoint_path="checkpoint.pkl",
    # load_path="generic_env_model.pkl",
    callback=callback,
    buffer_size=50000, # 50000
    learning_starts=1000,
    prioritized_replay=True, #False
    batch_size=256 #32
)
print("\n=====\nSaving model to generic_env_model.pkl\n=====\n")
act.save("generic_env_model.pkl")