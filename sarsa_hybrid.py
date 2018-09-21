import numpy as np
import gym
import min_generic_env


from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents import SARSAAgent
from rl.policy import BoltzmannQPolicy


ENV_NAME = 'MinGenericEnv-v1'

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# SARSA does not require a memory.
policy = BoltzmannQPolicy()
sarsa = SARSAAgent(model=model, nb_actions=nb_actions, nb_steps_warmup=10, policy=policy)
sarsa.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
sarsa.fit(env, nb_steps=50000, visualize=False, verbose=1)

# After training is done, we save the final weights.
sarsa.save_weights('sarsa_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
sarsa.test(env, nb_episodes=30, visualize=True)


# 10000/10000 [==============================] - 135s 13ms/step - reward: -0.5962
# 2327 episodes - episode_reward: -2.562 [-10.000, 1.000] - loss: 2.072 - mean_absolute_error: 3.528 - mean_q: -3.721

# Interval 2 (10000 steps performed)
# 10000/10000 [==============================] - 136s 14ms/step - reward: -0.2802
# 2227 episodes - episode_reward: -1.258 [-10.000, 1.000] - loss: 0.681 - mean_absolute_error: 3.112 - mean_q: -2.055

# Interval 3 (20000 steps performed)
# 10000/10000 [==============================] - 136s 14ms/step - reward: -0.2180
# 2186 episodes - episode_reward: -0.997 [-10.000, 1.000] - loss: 0.386 - mean_absolute_error: 3.216 - mean_q: -1.547

# Interval 4 (30000 steps performed)
# 10000/10000 [==============================] - 136s 14ms/step - reward: -0.2180
# 2098 episodes - episode_reward: -1.039 [-10.000, 1.000] - loss: 0.463 - mean_absolute_error: 3.707 - mean_q: -1.718

# Interval 5 (40000 steps performed)
# 10000/10000 [==============================] - 133s 13ms/step - reward: -0.2122
# done, took 675.619 seconds
# Testing for 30 episodes ...
# Episode 1: reward: 1.000, steps: 1
# Episode 2: reward: 1.000, steps: 2
# Episode 3: reward: -1.000, steps: 8
# Episode 4: reward: 1.000, steps: 1
# Episode 5: reward: -1.000, steps: 8
# Episode 6: reward: 1.000, steps: 1
# Episode 7: reward: 1.000, steps: 1
# Episode 8: reward: -1.000, steps: 6
# Episode 9: reward: -10.000, steps: 1
# Episode 10: reward: 1.000, steps: 8
# Episode 11: reward: -10.000, steps: 8
# Episode 12: reward: 1.000, steps: 4
# Episode 13: reward: 1.000, steps: 1
# Episode 14: reward: 1.000, steps: 1
# Episode 15: reward: -1.000, steps: 3
# Episode 16: reward: 1.000, steps: 1
# Episode 17: reward: 1.000, steps: 1
# Episode 18: reward: -10.000, steps: 1
# Episode 19: reward: -1.000, steps: 9
# Episode 20: reward: 1.000, steps: 1
# Episode 21: reward: 1.000, steps: 7
# Episode 22: reward: 1.000, steps: 10
# Episode 23: reward: -1.000, steps: 9
# Episode 24: reward: 1.000, steps: 1
# Episode 25: reward: 1.000, steps: 1
# Episode 26: reward: -1.000, steps: 11
# Episode 27: reward: 1.000, steps: 7
# Episode 28: reward: 1.000, steps: 1
# Episode 29: reward: -1.000, steps: 8
# Episode 30: reward: -10.000, steps: 5
