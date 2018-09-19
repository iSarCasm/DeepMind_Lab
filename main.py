import gym
import generic_env
from random import randint
from baselines import deepq

def callback(lcl, _glb):
    #TODO:figure out what score is "solved game"
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved

env = gym.make('GenericEnv-v1')
# env = gym.make('CartPole-v0')
# env = gym.make('FrozenLake-v0')
act = deepq.learn(
    env,
    network='mlp',
    lr=1e-3,
    total_timesteps=100000,
    buffer_size=50000,
    exploration_fraction=0.999999,
    exploration_final_eps=0.002,
    print_freq=500,
    callback=callback,
    batch_size=32,
    learning_starts=100
)
'''
for _ in range(100):
    action = randint(0, env.action_space.n - 1)
    print("PLAYER 1 DOING:",action)
    observation, reward, done, _ = env.step(action,debug=1)
    print("CURRENT REWARD:",reward)
    if done:
        print("\n=====\nGAME IS OVER NOW\n=====\n")
        break
'''