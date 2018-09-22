import mars_env
import copy
import time
import numpy as np
import random
from state import State

def llog(strs):
    print(strs, file=open("/home/sarcasm/workspace/DeepMind_Lab/client3.log", "a"))

class StrategyAgent:
    def __init__(self, player):
        self.player = player

    def select_move(self, state):
        self.state = state
        llog(State.saved_map)
        self.x, self.y = state.rover_position(self.player)
        llog("agent at ({}, {})".format(self.x, self.y))
        if self.hasEnergy():
            if self.load() < 3:
                if self.onMineral():
                    return self.dig()
                elif self.foundMineral():
                    return self.go_to_mineral()
                else:
                    return self.explore()
            else:
                return self.go_to_base()
        else:
            return self.charge()

    def foundMineral(self):
        self.mx, self.my = self.state.search_for_mineral(2)
        if self.mx == None:
            self.mx, self.my = self.state.search_for_mineral(3)
        return self.mx != None

    def hasEnergy(self):
        return self.state.energy > 0

    def load(self):
        return len(self.state.load_on_rover(self.player))

    def onMineral(self):
        return not self.state.onHole(self.x, self.y) and not self.state.onBase(self.x, self.y)

    def explore(self):
        llog("Exploring")
        moves = mars_env.move_moves(self.player)
        r = random.randint(0, len(moves)-1)
        return moves[r]
    
    def go_to_base(self):
        llog("Go to base")
        return self.go_to(self.state.base_x, self.state.base_y)

    def go_to_mineral(self):
        llog("Go to mineral {} {}".format(self.mx, self.my))
        return self.go_to(self.mx, self.my)

    def go_to(self, x, y):
        dx = self.resetrict(x - self.x)
        dy = self.resetrict(y - self.y)
        return { "rover_id": self.player, "action_type": "move", "dx": dx, "dy": dy }

    def resetrict(self, p):
        if p > 1:
            return 1
        elif p < -1:
            return -1
        else:
            return p

    def dig(self):
        llog("dig")
        self.mx = None
        self.my = None
        return { "rover_id": self.player, "action_type": "dig" }

    def charge(self):
        llog("charge")
        return { "rover_id": self.player, "action_type": "charge" }

