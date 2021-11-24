
import csv

class Call:
    def __init__(self, _time, _src, _dest, _state, _elvIndx):

        self.time = float(_time)
        self.src = int(_src)
        self.dest = int(_dest)
        self.state = int(_state)
        self.elvIndx = int(_elvIndx)

