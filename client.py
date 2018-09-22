#!/usr/bin/env python3

import json
import time
import sys
import random

from random_agent import RandomAgent
from state import State

random.seed
#f = open("python.log", "w")
while True:
    inputStr = input()
    state = State(inputStr)
    agent = RandomAgent(1)
    move = agent.select_move(state)
    print("move selected")
    print(move)
    #f.write(inputStr+'\n')
    choice = random.randrange(8)
    if (choice > 3):
        choice = choice + 1
    dx = choice % 3 - 1
    dy = choice / 3 - 1
    move = [{'rover_id': 1, 'action_type': 'move', 'dx': dx, 'dy': dy}]
    str = json.dumps(move)
#    f.write('send string\n')
#    f.write(str+'\n')
    sys.stdout.write(str + "\n")
    sys.stdout.flush()
    # time.sleep(1)
