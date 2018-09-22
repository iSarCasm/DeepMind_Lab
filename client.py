#!/usr/bin/env python3

import json
import time
import sys
import random

from random_agent import RandomAgent
from strategy_agent import StrategyAgent
from state import State
def llog(strs):
    print(strs, file=open("/home/sarcasm/workspace/DeepMind_Lab/client.log", "a"))

random.seed
#f = open("python.log", "w")
while True:
    inputStr = input()
    state = State(inputStr)
    # state = json.loads(inputStr)
    # agent = RandomAgent([1])
    # move = [agent.select_move(state)]
    agent = StrategyAgent(1)
    move = agent.select_move(state)
    llog("move selected")
    llog(move)
    # f.write(inputStr+'\n')
    # choice = random.randrange(8)
    # if (choice > 3):
    #     choice = choice + 1
    # dx = choice % 3 - 1
    # dy = choice / 3 - 1
    # move = [{'rover_id': 1, 'action_type': 'move', 'dx': -1, 'dy': -1}]
    str = json.dumps(move)
#    f.write('send string\n')
#    f.write(str+'\n')
    sys.stdout.write(str + "\n")
    sys.stdout.flush()
    # time.sleep(1)
