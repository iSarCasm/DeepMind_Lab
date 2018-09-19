import gym
import generic_env
from random import randint

env = gym.make('CartPole-v0')
env.reset()
for _ in range(100):
    action = randint(0, env.action_space.n - 1)
    print("PLAYER DOING: ", action)
    observation, reward, done, _ = env.step(action)
    print("CURRENT OBSERVATION:", observation)
    print("CURRENT REWARD:",reward)
    if done:
        print("\n=====\nGAME IS OVER NOW\n=====\n")
        break
