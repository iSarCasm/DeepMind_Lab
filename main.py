import gym
import generic_env

env = gym.make('GenericEnv-v1')
for _ in range(100):
    if len(env.action_space)>1:
        print("PLAYER 1 DOING:",env.action_space[1])
        observation, reward, done, _ = env.step(env.action_space[1],debug=1)
    else:
        print("PLAYER 1 DOING:",env.action_space[0])
        observation, reward, done, _ = env.step(env.action_space[0],debug=1)
    print("CURRENT REWARD:",reward)
    if done:
        print("\n=====\nGAME IS OVER NOW\n=====\n")
        break
