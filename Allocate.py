import csv
import queue
import math
import sys

from Building import *
import json
from Elevator import *
from Call import *


class Allocate:

    def __init__(self, buildingJson, callCsv):
        self.building = Building(buildingJson)
        self.calls = []
        with open(callCsv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.calls.append(Call(line[1], line[2], line[3], line[4], line[5]))

    def fastes_to_floor(self, call) -> int:
        tempEvTime = []  # holds the results of each elevator
        tup = [0, 1000000, 0]  # holds the: elevID, the elev time for the call, the flag of the list
        for elv in self.building.elevators:
            # if call UP
            if (call.src < call.dest):
                tup = self.fastest_to_up_calls(call, elv)
                tempEvTime.append(tup)

            # if call DOWN
            else:
                tup = self.fastest_to_down_calls(call, elv)
                tempEvTime.append(tup)

        minTime = [1000, 10000, 1000]
        # minTime = tempEvTime[0]
        for i in tempEvTime:
            print(i, "  for i in tempEvTime all")
            if minTime[1] > i[1]:
                minTime = i
        if (minTime[2] == 0):
            self.building.elevators[minTime[0]].addToCurr(call, minTime[1])
        elif (minTime[2] == 1):
            self.building.elevators[minTime[0]].addToWaitingUp(call, minTime[1])
        elif (minTime[2] == -1):
            self.building.elevators[minTime[0]].addToWaitingDown(call, minTime[1])

        # call to function which update the lists of the chosen elevator
        self.listsUpdate(minTime[0])

        return minTime[0]

    def fastest_to_up_calls(self, call: Call, elv: Elevator):
        tup = [0, 1000000, 0]  # holds the: elevID, the elev time for the call, the flag of the list
        #     if elv UP
        if (elv.flag == UP):
            # if didnt pass -> currStops:
            if (elv.pos < call.src):
                currStopsInx = 0
                if len(elv.currStops) == 0:
                    myTime = elv.tag + elv.speed * (abs(call.src - elv.pos))
                    tup = [elv.id, myTime, 0]
                    return tup

                while currStopsInx < (len(elv.currStops)):
                    if (elv.currStops[currStopsInx].floor < call.src):
                        currStopsInx += 1
                    else:
                        myTime = max(elv.currStops[currStopsInx - 1].actualTime,
                                     elv.currStops[currStopsInx - 1].callTime)
                        myTime += elv.tag + elv.speed * (call.src - elv.currStops[currStopsInx - 1].floor)
                        tup = [elv.id, myTime, 0]
                        print("tup = [elv.id, myTime, 1]")
                        return tup
            # else: passed -> WLUp
            else:
                currStopsInx = 0
                if len(elv.waitingUp) == 0:
                    last = elv.currStops[len(elv.currStops) - 1]
                    myTime = max(last.actualTime, last.callTime)
                    myTime += elv.tag + elv.speed * (abs(call.src - elv.pos))
                    tup = [elv.id, myTime, 1]
                    return tup
                while currStopsInx < len(elv.waitingUp):
                    if (elv.waitingUp[currStopsInx].floor < call.src):
                        currStopsInx += 1
                    else:

                        myTime = max(elv.waitingUp[currStopsInx].actualTime,
                                     elv.waitingUp[currStopsInx].callTime)
                        myTime += elv.tag + elv.speed * (call.src - elv.waitingUp[currStopsInx].floor)
                        tup = [elv.id, myTime, 1]
                        print("tup = [elv.id, myTime, 1]")
                        return tup


        # if elv DOWN -> waitingUp
        else:
            if len(elv.waitingUp) == 0:
                myTime = elv.tag + elv.speed * (abs(call.src - elv.currStops[-1]))
                tup = [elv.id, myTime, 1]
                return tup
            currStopsInx = 0
            while currStopsInx < len(elv.waitingUp):
                if (elv.waitingUp[currStopsInx].floor > call.src):
                    currStopsInx += 1
                else:
                    myTime = max(elv.waitingUp[currStopsInx].actualTime,
                                 elv.waitingUp[currStopsInx].callTime)
                    myTime += elv.tag + elv.speed * (call.src - elv.waitingUp[currStopsInx].floor)
                    tup = [elv.id, myTime, 1]
                    print("tup = [elv.id, myTime, 1]")
                    return tup

    def fastest_to_down_calls(self, call: Call, elv: Elevator):
        # if elv DOWN
        if (elv.flag == DOWN):
            # if didnt pass the call yet -> crrStops
            if (elv.pos > call.src):
                if len(elv.currStops) == 0:
                    myTime = elv.tag + elv.speed * (abs(call.src - elv.pos))
                    tup = [elv.id, myTime, 0]
                    return tup
                currStopsInx = 0
                while currStopsInx < len(elv.currStops):
                    if (elv.currStops[currStopsInx].floor > call.src):
                        currStopsInx += 1
                    else:
                        myTime = max(elv.currStops[currStopsInx].actualTime,
                                     elv.currStops[currStopsInx].callTime)
                        myTime += elv.tag + elv.speed * (elv.currStops[currStopsInx].floor - call.src)
                        tup = [elv.id, myTime, 0]
                        print("tup = [elv.id, myTime, 1]")
                        return tup

            # else: passed -> WLDown
            else:
                if len(elv.waitingDown) == 0:
                    myTime = elv.tag + elv.speed * (abs(call.src - elv.pos))
                    tup = [elv.id, myTime, -1]
                    return tup
                currStopsInx = 0
                while currStopsInx < len(elv.waitingDown):
                    if (elv.waitingDown[currStopsInx].floor > call.src):
                        currStopsInx += 1
                    else:
                        myTime = max(elv.waitingDown[currStopsInx].actualTime,
                                     elv.waitingDown[currStopsInx].callTime)
                        myTime += elv.tag + elv.speed * (elv.waitingDown[currStopsInx].floor - call.src)
                        tup = [elv.id, myTime, -1]
                        print("tup = [elv.id, myTime, 1]")
                        return tup
        # elv down -> WLDown
        else:
            if len(elv.waitingDown) == 0:
                myTime = elv.tag + elv.speed * (abs(call.src - elv.pos))
                tup = [elv.id, myTime, -1]
                return tup
            currStopsInx = 0
            while currStopsInx < len(elv.waitingDown):
                if (elv.waitingDown[currStopsInx].floor < call.src):
                    currStopsInx += 1
                else:
                    myTime = max(elv.waitingDown[currStopsInx].actualTime,
                                 elv.waitingDown[currStopsInx].callTime)
                    myTime += elv.tag + elv.speed * (call.src - elv.waitingDown[currStopsInx].floor)
                    # the list contains: elevIndex, the real time to call src , down=-1.
                    tup = [elv.id, myTime, -1]
                    print("tup = [elv.id, myTime, 1]")
                    return tup

    # function which update all the elevators lists
    def listsUpdate(self, elvIndex: int):
        elev = self.building.elevators[elvIndex]
        currStopsInx = 0
        if len(self.building.elevators[elvIndex].currStops) == 0:
            return
        startTime = max(elev.currStops[0].actualTime, elev.currStops[0].callTime)
        time = 0
        floor = elev.currStops[0].floor

        # updating the curr list
        for i in range(1, len(elev.currStops)):  # goes from i=0 to i=currStops.size-2
            #  tags ect
            #  updating time = max actualTime callTime
            timetoNextFloor = elev.tag + elev.speed * abs(elev.currStops[i].floor - floor)
            floor = elev.currStops[i].floor
            time += max(timetoNextFloor, elev.currStops[i].callTime)
            elev.currStops[i].actualTime = time
        if elev.flag == UP:
            for i in range(1, len(elev.waitingDown)):  # goes from i=0 to i=currStops.size-2
                #  tags ect
                #  updating time = max actualTime callTime
                timetoNextFloor = elev.tag + elev.speed * abs(elev.waitingDown[i].floor - floor)
                floor = elev.waitingDown[i].floor
                time += max(timetoNextFloor, elev.waitingDown[i].callTime)
                elev.waitingDown[i].actualTime = time
            for i in range(1, len(elev.waitingUp)):  # goes from i=0 to i=currStops.size-2
                #  tags ect
                #  updating time = max actualTime callTime
                timetoNextFloor = elev.tag + elev.speed * abs(elev.waitingUp[i].floor - floor)
                floor = elev.waitingUp[i].floor
                time += max(timetoNextFloor, elev.currStops[i].callTime)
                elev.waitingUp[i].actualTime = time
        # flag == DOWN
        else:
            for i in range(1, len(elev.waitingUp)):  # goes from i=0 to i=currStops.size-2
                #  tags ect
                #  updating time = max actualTime callTime
                timetoNextFloor = elev.tag + elev.speed * abs(elev.waitingUp[i].floor - floor)
                floor = elev.waitingUp[i].floor
                time += max(timetoNextFloor, elev.waitingUp[i].callTime)
                elev.waitingUp[i].actualTime = time
            for i in range(1, len(elev.waitingDown)):  # goes from i=0 to i=currStops.size-2
                #  tags ect
                #  updating time = max actualTime callTime
                timetoNextFloor = elev.tag + elev.speed * abs(elev.waitingDown[i].floor - floor)
                floor = elev.waitingDown[i].floor
                time += max(timetoNextFloor, elev.waitingDown[i].callTime)
                elev.waitingDown[i].actualTime = time

        # when to insert up and down in currrstops
        while currStopsInx < (len(elev.waitingDown)):
            if (elev.flag == UP):
                # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                # elev.currStops[currStopsInx][FloorDetailsUp]
                currStopsInx += 1
            # else:
            # elev.currStops[currStopsInx][FloorDetailsDown()]

    # In this method there are 3 goals:
    # 1-update each list times.
    # 2-update the flags and the lists.
    # 3-update the pos and stop in the calls floors
    # the function run each 0.1 sec and updates the data
    def update(self, JUMP, globalTime):
        # loop over all the elevators
        for elv in self.building.elevators:
            # if the currstops list isEmpty -> change the flag value and update the
            # currstops list
            if (len(elv.currStops) == 0):
                if (elv.flag == UP):
                    elv.flag = DOWN
                    elv.currStops = elv.waitingDown  # if it works well
                else:
                    elv.flag = UP
                    elv.currStops = elv.waitingUp

            # updating the elev pos and the currStops list if we stop
            # the elv up
            if (elv.flag == UP):
                newPos = elv.pos + elv.speed * JUMP
                #
                if (math.ceil(newPos) - math.ceil(elv.pos) == 0):
                    elv.pos = newPos
                # we passed a floor
                else:
                    if (elv.currStops[0] == math.floor(newPos)):
                        elv.pos = math.floor(newPos)
                        if globalTime >= max(elv.currStops[0].actualTime, elv.currStops[0].callTime):
                            elv.currStops.remove(elv.currStops[0])
                    else:
                        elv.pos = newPos

            # the elv is down
            else:
                newPos = elv.pos - elv.speed * JUMP
                if (math.ceil(newPos) - math.ceil(elv.pos) == 0):
                    elv.pos = newPos
                # we changed the beginning number of the floor
                else:
                    # if we have to stop there
                    if (elv.currStops[0] == math.ceil(newPos)):
                        elv.pos = math.ceil(newPos)
                        if globalTime >= max(elv.currStops[0].actualTime, elv.currStops[0].callTime):
                            elv.currStops.remove(elv.currStops[0])
