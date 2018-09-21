import numpy as np
import gym
import min_generic_env

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


ENV_NAME = 'MinGenericEnv-v1'
# ENV_NAME = 'FrozenLake-v0'
# ENV_NAME = 'CartPole-v0'


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model regardless of the dueling architecture
# if you enable dueling network in DQN , DQN will build a dueling network base on your model automatically
# Also, you can build a dueling network by yourself and turn off the dueling network in DQN.
model = Sequential()
model.add(Flatten(input_shape=env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions, activation='linear'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
# enable the dueling network
# you can specify the dueling_type to one of {'avg','max','naive'}
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

# After training is done, we save the final weights.
dqn.save_weights('duel_dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=25, visualize=False)


# RESULTS
# Training for 50000 steps ...
# Interval 1 (0 steps performed)
#    11/10000 [..............................] - ETA: 4:17 - reward: -3.5455/usr/local/lib/python3.5/dist-packages/rl/memory.py:39: UserWarning: Not enough entries to sample without replacement. Consider increasing your warm-up phase to avoid oversampling!
#   warnings.warn('Not enough entries to sample without replacement. Consider increasing your warm-up phase to avoid oversampling!')
# 10000/10000 [==============================] - 198s 20ms/step - reward: -0.3854
# 2195 episodes - episode_reward: -1.756 [-10.000, 1.000] - loss: 1.862 - mean_absolute_error: 2.777 - mean_q: -1.182

# Interval 2 (10000 steps performed)
# 10000/10000 [==============================] - 239s 24ms/step - reward: -0.2436
# 2189 episodes - episode_reward: -1.113 [-10.000, 1.000] - loss: 1.489 - mean_absolute_error: 2.976 - mean_q: -0.873

# Interval 3 (20000 steps performed)
# 10000/10000 [==============================] - 361s 36ms/step - reward: -0.2335
# 2176 episodes - episode_reward: -1.073 [-10.000, 1.000] - loss: 1.392 - mean_absolute_error: 3.157 - mean_q: -0.740

# Interval 4 (30000 steps performed)
# 10000/10000 [==============================] - 201s 20ms/step - reward: -0.1890
# 2135 episodes - episode_reward: -0.885 [-10.000, 1.000] - loss: 1.322 - mean_absolute_error: 3.174 - mean_q: -0.731

# Interval 5 (40000 steps performed)
# 10000/10000 [==============================] - 201s 20ms/step - reward: -0.2184
# done, took 1198.635 seconds
# Testing for 25 episodes ...
# Episode 1: reward: -1.000, steps: 10
# Episode 2: reward: -1.000, steps: 6
# Episode 3: reward: -1.000, steps: 6
# Episode 4: reward: 1.000, steps: 1
# Episode 5: reward: 1.000, steps: 1
# Episode 6: reward: 1.000, steps: 1
# Episode 7: reward: 1.000, steps: 10
# Episode 8: reward: 1.000, steps: 1
# Episode 9: reward: 1.000, steps: 1
# Episode 10: reward: 1.000, steps: 1
# Episode 11: reward: -1.000, steps: 7
# Episode 12: reward: 1.000, steps: 1
# Episode 13: reward: 1.000, steps: 9
# Episode 14: reward: -1.000, steps: 5
# Episode 15: reward: 1.000, steps: 2
# Episode 16: reward: 1.000, steps: 1
# Episode 17: reward: 1.000, steps: 9
# Episode 18: reward: -1.000, steps: 8
# Episode 19: reward: 1.000, steps: 8
# Episode 20: reward: 1.000, steps: 1
# Episode 21: reward: 1.000, steps: 10
# Episode 22: reward: 1.000, steps: 7
# Episode 23: reward: -1.000, steps: 9
# Episode 24: reward: -1.000, steps: 6
# Episode 25: reward: 1.000, steps: 1