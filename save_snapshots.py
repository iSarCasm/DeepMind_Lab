#DOESN'T WORK YET

import gym
import generic_env
from random import randint
from baselines import deepq

env = gym.make('GenericEnv-v1')
iterator = 0
act = deepq.learn(
    env,
    network='mlp',
    lr=1e-3,
    total_timesteps=1000,
    buffer_size=50000,
    exploration_fraction=0.1,
    exploration_final_eps=0.02,
    print_freq=10,
    callback=None,
    load_path=None
)
while True:
    model_file_name = ("generic_env_model_" + str(iterator) + ".pkl")
    print("\n=====\nSaving model to ", model_file_name, "\n=====\n")
    act.save(model_file_name)
    iterator = iterator + 1
    act.load_act(model_file_name)