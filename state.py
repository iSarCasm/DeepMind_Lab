import json
import time
import numpy

class State:
    #do reset before using(?)
    saved_map = None
    def __init__(self, inputStr):
        self.state = json.loads(inputStr)
        self.base_x = self.state["data"]["base"]["x"]
        self.base_y = self.state["data"]["base"]["y"]
        self.energy = self.state["data"]["rovers"][0]["energy"]
        if self.state["command"] == "reset" or State.saved_map == None:
            self.reset()
        for rover_id in range(0, self.state["data"]["rovers"].len()):
            curx = self.state["data"]["rovers"][rover_id]["x"]
            cury = self.state["data"]["rovers"][rover_id]["y"]
            # TODO:respect rover_id
            # update saved_map
            for xdef in range(-1, 2):
                for ydef in range(-1, 2):
                    #wrap map
                    diffx = curx+xdef
                    diffy = cury+ydef
                    mapsize = self.state["data"]["FIELD_SIZE"]-1
                    if diffx < 0:
                        diffx = mapsize
                    if diffx > mapsize:
                        diffx = 0
                    if diffy < 0:
                        diffy = mapsize
                    if diffy > mapsize:
                        diffy = 0
                    State.saved_map[diffx][diffy] = self.state["data"]["rovers"][rover_id]["area"][xdef+1][ydef+1].copy()

    def reset(self):
        saved_map = numpy.zeros(shape=(self.state["data"]["FIELD_SIZE"], self.state["data"]["FIELD_SIZE"]))

    def score(self, state):
        #reward for being next to unexplored territory
        #if neighbours(state["data"]["x"],state["data"]["y"]):

        #reward for standing on resource

        #reward for returning to base(with 3 resources)

        return 1

    def this_cell(self,x,y):
        return State.saved_map[x][y]

    def rover_position(self, id=0):
        return [self.state["data"]["rovers"][id]["x"], self.state["data"]["rovers"][id]["y"]]

    def onHole(self, x, y):
        return 4 in State.savedmap[x][y]["objects"]#OBJECTS["HOLE"]

    def load_on_rover(self, rover_id):
        return self.state["data"]["rovers"][rover_id]["load"]

    def search_for_mineral(self, mineral_id):
        for x in range(0, self.state["data"]["FIELD_SIZE"]):
            for y in range(0, self.state["data"]["FIELD_SIZE"]):
                if State.saved_map[x][y]["terrain"] == mineral_id:
                    return [x, y]
        return [None, None]
