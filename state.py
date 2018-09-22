import json
import time
import numpy

class State:
    #do reset before using(?)
    saved_map = []

    def __init__(self, inputStr):
        self.state = json.loads(inputStr)
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

    def reset(self, inputStr):
        saved_map = numpy.zeros(shape=(self.state["field_size"], self.state["field_size"]))

