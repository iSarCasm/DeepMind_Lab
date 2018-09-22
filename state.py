import json
import time

class State:
    def __init__(self, inputStr):
        self.state = json.loads(inputStr)