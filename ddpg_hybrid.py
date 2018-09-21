import numpy as np

import gym
from gym import wrappers
import min_generic_env

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.processors import WhiteningNormalizerProcessor
from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess


class MujocoProcessor(WhiteningNormalizerProcessor):
    def process_action(self, action):
        return np.clip(action, -1., 1.)


ENV_NAME = 'MinGenericEnv-v1'
gym.undo_logger_setup()


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model.
actor = Sequential()
actor.add(Flatten(input_shape=env.observation_space.shape))
actor.add(Dense(400))
actor.add(Activation('relu'))
actor.add(Dense(300))
actor.add(Activation('relu'))
actor.add(Dense(nb_actions))
actor.add(Activation('tanh'))
print(actor.summary())

action_input = Input(shape=(nb_actions,), name='action_input')
observation_input = Input(shape=env.observation_space.shape, name='observation_input')
flattened_observation = Flatten()(observation_input)
x = Dense(400)(flattened_observation)
x = Activation('relu')(x)
x = Concatenate()([x, action_input])
x = Dense(300)(x)
x = Activation('relu')(x)
x = Dense(1)(x)
x = Activation('linear')(x)
critic = Model(inputs=[action_input, observation_input], outputs=x)
print(critic.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=100000, window_length=1)
random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.1)
agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=1000, nb_steps_warmup_actor=1000,
                  random_process=random_process, gamma=.99, target_model_update=1e-3,
                  processor=MujocoProcessor())
agent.compile([Adam(lr=1e-4), Adam(lr=1e-3)], metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
agent.fit(env, nb_steps=50000, visualize=False, verbose=1)

# After training is done, we save the final weights.
agent.save_weights('ddpg_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
agent.test(env, nb_episodes=40, visualize=True, nb_max_episode_steps=200)

# Interval 1 (0 steps performed)
# 10000/10000 [==============================] - 199s 20ms/step - reward: -1.1052
# 2748 episodes - episode_reward: -4.022 [-10.000, 1.000] - loss: 1.109 - mean_absolute_error: 1.042 - mean_q: -3.342

# Interval 2 (10000 steps performed)
# 10000/10000 [==============================] - 216s 22ms/step - reward: -0.3925
# 2234 episodes - episode_reward: -1.757 [-10.000, 1.000] - loss: 1.057 - mean_absolute_error: 1.085 - mean_q: -2.325

# Interval 3 (20000 steps performed)
# 10000/10000 [==============================] - 217s 22ms/step - reward: -0.3698
# 2245 episodes - episode_reward: -1.647 [-10.000, 1.000] - loss: 1.079 - mean_absolute_error: 1.095 - mean_q: -1.944

# Interval 4 (30000 steps performed)
# 10000/10000 [==============================] - 217s 22ms/step - reward: -0.3036
# 2194 episodes - episode_reward: -1.384 [-10.000, 1.000] - loss: 1.091 - mean_absolute_error: 1.097 - mean_q: -1.686

# Interval 5 (40000 steps performed)
# 10000/10000 [==============================] - 220s 22ms/step - reward: -0.3091
# done, took 1069.012 seconds
# Testing for 40 episodes ...
# Episode 1: reward: -10.000, steps: 9
# Episode 2: reward: 1.000, steps: 8
# Episode 3: reward: -10.000, steps: 5
# Episode 4: reward: -10.000, steps: 5
# Episode 5: reward: 1.000, steps: 7
# Episode 6: reward: -1.000, steps: 10
# Episode 7: reward: -10.000, steps: 1
# Episode 8: reward: -1.000, steps: 3
# Episode 9: reward: 1.000, steps: 9
# Episode 10: reward: 1.000, steps: 1
# Episode 11: reward: 1.000, steps: 1
# Episode 12: reward: -1.000, steps: 10
# Episode 13: reward: 1.000, steps: 1
# Episode 14: reward: 1.000, steps: 6
# Episode 15: reward: -1.000, steps: 6
# Episode 16: reward: -1.000, steps: 10
# Episode 17: reward: 1.000, steps: 1
# Episode 18: reward: -10.000, steps: 10
# Episode 19: reward: -10.000, steps: 1
# Episode 20: reward: 1.000, steps: 1
# Episode 21: reward: 1.000, steps: 9
# Episode 22: reward: -10.000, steps: 6
# Episode 23: reward: 1.000, steps: 9
# Episode 24: reward: 1.000, steps: 1
# Episode 25: reward: -10.000, steps: 1
# Episode 26: reward: 1.000, steps: 8
# Episode 27: reward: 1.000, steps: 1
# Episode 28: reward: 1.000, steps: 1
# Episode 29: reward: -10.000, steps: 4
# Episode 30: reward: -1.000, steps: 7
# Episode 31: reward: 1.000, steps: 8
# Episode 32: reward: 1.000, steps: 1
# Episode 33: reward: 1.000, steps: 1
# Episode 34: reward: 1.000, steps: 6
# Episode 35: reward: 1.000, steps: 1
# Episode 36: reward: 1.000, steps: 7
# Episode 37: reward: -1.000, steps: 6
# Episode 38: reward: 1.000, steps: 1
# Episode 39: reward: 1.000, steps: 3
# Episode 40: reward: 1.000, steps: 4
