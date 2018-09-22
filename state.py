import json
import time
import numpy

class State:
    #do reset before using(?)
    saved_map = None
    score = 0
    def __init__(self, inputStr):
        self.state = json.loads(inputStr)
        if self.state["command"] == "reset" or saved_map == None:
            self.reset()
        curx = self.state["rovers"]["x"]
        cury = self.state["rovers"]["y"]
        # TODO:respect rover_id
        # update saved_map
        for xdef in range(-1, 1):
            for ydef in range(-1, 1):
                #wrap map
                diffx = curx+xdef
                diffy = cury+ydef
                mapsize = self.state["field_size"]-1
                if diffx < 0:
                    diffx = mapsize
                if diffx > mapsize:
                    diffx = 0
                if diffy < 0:
                    diffy = mapsize
                if dify > mapsize:
                    diffy = 0
                saved_map[diffx][diffy] = self.state["rovers"]["area"][xdef+1][ydef+1].copy()

    def reset(self):
        saved_map = numpy.zeros(shape=(self.state["field_size"], self.state["field_size"]))
        score = 0

    def score(self, state):
        #reward for being next to unexplored territory

        #reward for standing on resource

        #reward for returning to base(with 3 resources)

        return 1
