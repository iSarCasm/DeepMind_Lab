import numpy as np
import copy


state_example = {
    "all_map": [],
    "field_size": 12,
    "base": {"x": 3, "y": 4},
    "rovers": [
        {
            "id": 1,
            "x": 3,
            "y": 3,
            "energy": 30,
            "load": [],
            "processed": False,
            "area": [
                [{"terrain":1,"objects":[]},{"terrain":2,"objects":[]},{"terrain":2,"objects":[]}],
                [{"terrain":3,"objects":[]},{"terrain":1,"objects":[11]},{"terrain":1,"objects":[]}],
                [{"terrain":1,"objects":[]},{"terrain":3,"objects":[]},{"terrain":1,"objects":[]}]
            ]
        }
    ]
}


move_example = [{
  "rover_id":1,
  "action_type":"move",
  "dx":1,
  "dy":-1
}]


TERRAIN = {
  "UNKNOWN": 0,
  "PLAIN": 1,
  "HILLS": 2,
  "RIVER": 3,
  "CRATER": 4,
  "MOUNTAIN": 5, # unpassable
  "BASE": 6
}

OBJECTS = {
  "BASE": 10,
  "ROVER": 11,
  "HOLE": 4
}

PROBABILITIES = {
  "RESOURCES.RAREEARTH": 0.1,
  "RESOURCES.METAL": 0.3,
  "RESOURCES.HYDRATES": 0.5,
  "RESOURCES.URANIUM": 0.7,
  "RESOURCES.BASE": 0,
}


# # PLAYER, STATE -> legal MOVES
def moves(players, state):
    all_moves = []
    for player in players:
        moves = []
        dig = { "rover_id": player, "action_type": "dig" }
        charge = { "rover_id": player, "action_type": "charge" }

    return_moves = []
    if len(all_moves) == 2:
        for m1 in all_moves[0]:
            for m2 in all_moves[1]:
                complex_move = [m1, m2]
                return_moves.append(complex_move)
    else:
        return_moves = all_moves[0]
    
    return return_moves

def move_moves(player, state):
    



