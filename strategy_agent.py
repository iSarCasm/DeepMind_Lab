import mars_env
import copy
import time
import numpy as np

class StrategyAgent:
    def __init__(self, player):
        self.player = player

    def select_move(self, state):
        self.state = state
        self.x, self.y = state.position_for_rover(self.player)
        if hasEnegrgy():
            if load() < 3:
                if onMineral():
                    return dig()
                elif foundMineral():
                    return go_to_mineral()
                else
                    return explore()
            else:
                return go_to_base()
        else:
            return charge()

    def foundMineral(self):
        self.mx, self.my = self.state.search_for_minerals()
        return self.mx != None

    def hasEnergy(self):
        self.state.energy > 0

    def load(self):
        return len(self.state.load_for_rover(self.player))

    def onMineral(self):
        if self.state.onHole(self.x, self.y):
            return False
        else:
            return True

    def explore(self):
        moves = mars_env.move_moves(self.player)
        r = random.randint(0, len(moves)-1)
        return moves[r]
    
    def go_to_base(self):
        return go_to(self.state.base_x, self.state.base_y)

    def go_to_mineral(self):
        return go_to(self.mx, self.my)

    def go_to(self, x, y):
        dx = x - self.x
        dx = max(1, min(-1, dx))
        dy = y - self.y
        dy = max(1, min(-1, dy))
        return { "rover_id": player, "action_type": "move", "dx": dx, "dy": dy }

    def dig(self):
        self.mx = None
        self.my = None
        return { "rover_id": self.player, "action_type": "dig" }

    def charge(self):
        return { "rover_id": self.player, "action_type": "charge" }

