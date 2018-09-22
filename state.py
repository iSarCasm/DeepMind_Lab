import json
import time
import numpy

class State:
    #do reset before using(?)
    saved_map = None

    def __init__(self, inputStr):
        self.state = json.loads(inputStr)
        if self.state["command"] == "reset" or State.saved_map == None:
            self.reset()
        curx = self.state["data"]["rovers"][0]["x"]
        cury = self.state["data"]["rovers"][0]["y"]
        # TODO:respect rover_id
        # update saved_map
        for xdef in range(-1, 1):
            for ydef in range(-1, 1):
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
                saved_map[diffx][diffy] = self.state["data"]["rovers"][0]["area"][xdef+1][ydef+1].copy()

    def reset(self):
        saved_map = numpy.zeros(shape=(self.state["data"]["FIELD_SIZE"], self.state["data"]["FIELD_SIZE"]))
