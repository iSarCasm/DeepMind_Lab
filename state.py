import json
import time
import numpy

def llog(strs):
    print(strs, file=open("/home/sarcasm/workspace/DeepMind_Lab/client3.log", "a"))

class State:
    #do reset before using(?)
    saved_map = None
    def __init__(self, inputStr):
        self.state = json.loads(inputStr)
        self.base_x = self.state["data"]["base"]["x"]
        self.base_y = self.state["data"]["base"]["y"]
        self.energy = self.state["data"]["rovers"][0]["energy"]
        if State.saved_map is None:
            self.reset()
        if self.state["command"] == "reset":
            State.saved_map = None
        for rover_id in range(0, len(self.state["data"]["rovers"])):
            curx = self.state["data"]["rovers"][rover_id]["x"]
            cury = self.state["data"]["rovers"][rover_id]["y"]
            # TODO:respect rover_id
            # update saved_map
            llog("\n")
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
                    if "area" in self.state["data"]["rovers"][rover_id]:
                        llog("Save to map {} at ({}, {})".format(self.state["data"]["rovers"][rover_id]["area"][xdef+1][ydef+1], diffx, diffy))
                        State.saved_map[diffx][diffy] = self.state["data"]["rovers"][rover_id]["area"][ydef+1][xdef+1].copy()

    def reset(self):
        # State.saved_map = numpy.zeros(shape=(self.state["data"]["FIELD_SIZE"], self.state["data"]["FIELD_SIZE"]))
        size = self.state["data"]["FIELD_SIZE"]
        State.saved_map = [[{"terrain":0,"objects":[]} for i in range(size)] for j in range(size)]

    def score(self, state):
        #reward for being next to unexplored territory
        #if neighbours(state["data"]["x"],state["data"]["y"]):

        #reward for standing on resource

        #reward for returning to base(with 3 resources)

        return 1

    def this_cell(self,x,y):
        return State.saved_map[x][y]

    def rover_position(self, id=0):
        return [self.state["data"]["rovers"][id-1]["x"], self.state["data"]["rovers"][id-1]["y"]]

    def onHole(self, x, y):
        return 4 in State.saved_map[x][y]["objects"]#OBJECTS["HOLE"]

    def onBase(self, x, y):
        return 10 in State.saved_map[x][y]["objects"]#OBJECTS["HOLE"]

    def load_on_rover(self, rover_id):
        return self.state["data"]["rovers"][rover_id-1]["load"]

    def search_for_mineral(self, mineral_id):
        for x in range(0, self.state["data"]["FIELD_SIZE"]):
            for y in range(0, self.state["data"]["FIELD_SIZE"]):
                if State.saved_map[x][y]["terrain"] == mineral_id and not self.onHole(x, y) :
                    return [x, y]
        return [None, None]

    def mountain_error(self):
        return "1" in self.state["data"]["errors"]

    def closest_terrain_to_rover(self, terrain_type, rover_id, ignore_holes=True):
        leastdist = 1000
        mapsize = self.state["data"]["FIELD_SIZE"]
        ux = self.state["data"]["rovers"][rover_id]["x"]
        uy = self.state["data"]["rovers"][rover_id]["y"]
        for x in range(0, mapsize):
            for y in range(0, mapsize):
                if State.saved_map[x][y]["terrain"] == terrain_type:
                    if not ignore_holes and 4 in State.saved_map["objects"]:
                        #find if this terrain is closer than last found
                        diff_x = abs(ux-x)
                        diff_y = abs(uy-y)
                        if max(diff_x, diff_y) < leastdist:
                            saved_x = x
                            saved_y = y
                            leastdist = max(x, y)
        return [savedx, savedy]
