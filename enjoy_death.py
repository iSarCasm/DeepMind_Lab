import gym
import generic_env
import generic_env_helpers
from random import randint
from baselines import deepq

env = gym.make('GenericEnv-v1')
act = deepq.learn(env, network='mlp', total_timesteps=0, load_path="generic_env_model.pkl")

obs, done = env.reset(), False
episode_rew = 0
while not done:
    obs, rew, done, _ = env.step(act(obs)[0])
    print("p1:", generic_env_helpers.score(1, env.state), "\t\t\tp2:", generic_env_helpers.score(2, env.state))
print("Score:", rew)
print("\nBoard\n",env.state['board'])