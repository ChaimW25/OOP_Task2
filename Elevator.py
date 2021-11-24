import json
from queue import PriorityQueue
from Call import *

UP = True
DOWN = False


class Elevator:
    def __init__(self, _id, _speed, _minFloor, _maxFloor, _closeTime, _openTime, _startTime, _stopTime, _startingFloor):
        self.id = _id
        self.speed = _speed
        self.minFloor = _minFloor
        self.maxFloor = _maxFloor
        self.closeTime = _closeTime
        self.openTime = _openTime
        self.startTime = _startTime
        self.stopTime = _stopTime
        self.flag = UP
        # self.currStops = PriorityQueue()
        # self.waitingUp = PriorityQueue()
        # self.waitingDown = PriorityQueue()
        self.currStops = []
        self.waitingUp = []
        self.waitingDown = []
        self.pos = _startingFloor
        self.tag = _openTime + _closeTime + _startTime + _stopTime

    # def getPos(self, _currTime):
    # distance = self.currStops-_currTime
    # if (self.flag==UP):
    #     return _currTime[0]- floorDis(distance)
    # else:
    #     return _currTime[0]+ floorDis(distance)

    # def floorDis (_distance):
    # dis= (int)(_distance/(self.openTime+self.closeTime+self.startTime+self.stopTime+self.speed))

    # def addToCurr(self, call: Call, _actualTime):
    #     if self.flag == UP:
    #         self.currStops.put(FloorDetailsUp(call.src, _actualTime, call.time))
    #         self.currStops.put(FloorDetailsUp(call.dest))
    #     else:
    #         self.currStops.put(FloorDetailsDown(call.src, _actualTime, call.time))
    #         self.currStops.put(FloorDetailsDown(call.dest))
    def addToCurr(self, call: Call, _actualTime):
        if self.flag == UP:
            self.currStops.append(FloorDetailsUp(call.src, _actualTime, call.time))
            self.currStops.append(FloorDetailsUp(call.dest))
            self.currStops.sort(key=lambda fd: fd.floor)
        else:
            self.currStops.append(FloorDetailsDown(call.src, _actualTime, call.time))
            self.currStops.append(FloorDetailsDown(call.dest))
            self.currStops.sort(reverse=True,key=lambda fd: fd.floor)

    # def addToWaitingUp(self, call: Call, _actualTime):
    #     self.waitingUp.put(FloorDetailsUp(call.src, _actualTime, call.time))
    #     self.waitingUp.put(FloorDetailsUp(call.dest))
    def addToWaitingUp(self, call: Call, _actualTime):
        self.waitingUp.append(FloorDetailsUp(call.src, _actualTime, call.time))
        self.waitingUp.append(FloorDetailsUp(call.dest))
        self.currStops.sort(key=lambda fd: fd.floor)

    #
    # def addToWaitingDown(self, call: Call, _actualTime):
    #     self.waitingDown.put(FloorDetailsDown(call.src, _actualTime, call.time))
    #     self.waitingDown.put(FloorDetailsDown(call.dest))

    def addToWaitingDown(self, call: Call, _actualTime):
        self.waitingDown.append(FloorDetailsDown(call.src, _actualTime, call.time))
        self.waitingDown.append(FloorDetailsDown(call.dest))
        self.currStops.sort(reverse=True, key=lambda fd: fd.floor)


# we need to check if the acT make sa
class FloorDetailsUp:
    def __init__(self, _floor, _actualTime=0, _calltime=0):
        self.floor = _floor
        self.actualTime = _actualTime
        self.callTime = _calltime

    def __lt__(self, other):
        return self.floor < other.floor


class FloorDetailsDown(FloorDetailsUp):
    # def __init__(self, _floor, _actualTime=0, _callTime=0):
    #     self.floor = _floor
    #     self.actualTime = _actualTime
    #     self.callTime = _callTime

        # override
        def __lt__(self, other):
            return self.floor > other.floor
