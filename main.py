import gym
import generic_env

env = gym.make('GenericEnv-v1')
for _ in range(20):
    if len(env.action_space)>1:
        observation, reward, done, _ = env.step(env.action_space[1])
    else:
        observation, reward, done, _ = env.step(env.action_space[0])
    print(reward)
