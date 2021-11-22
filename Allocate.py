import csv
import queue
import math
from Building import *
import json
from Elevator import *
from Call import *


class Allocate:

    def __init__(self, buildingJson, callCsv, outputCsv):
        self.building = Building(buildingJson)
        self.calls = []
        with open(callCsv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.calls.append(Call(line[1], line[2], line[3], line[4], line[5]))

        # creates 2 lists of elevators
        self.upElv = []
        self.downElv = []
        # pq = PQueueUp()
        # for elevator in pq:
        #     if elevator % 2 == 0:
        #         self.upElv.append(elevator)
        #     else:
        #         self.downElv.append(elevator)

    def fastes_to_floor(self, call) -> int:
        fastesElev = 0
        tempEvTime = []

        for elv in self.building.elevators:
            # if call UP
            if (call.src < call.dest):
                #     if elv UP
                if (elv.flag == UP):
                    #         if didnt pass -> currStops:
                    if (elv.pos < call.src):
                        currStopsInx = 0
                        while currStopsInx < (elv.currStops.qsize()):
                            if (elv.currStops[currStopsInx].floor < call.src):
                                currStopsInx += 1
                            else:
                                myTime = max(elv.currStops[currStopsInx - 1].actualTime,
                                             elv.currStops[currStopsInx - 1].callTime)
                                myTime += elv.tag + elv.speed * (call.src - elv.currStops[currStopsInx - 1].floor)
                                tup = [elv.id, myTime, 0]
                                tempEvTime.append(tup)
                                # end the while
                                currStopsInx = elv.currStops.qsize()
                    # else: passed -> WLUp
                    else:
                        currStopsInx = 0
                        while currStopsInx < (elv.waitingUp.qsize()):
                            if (elv.waitingUp[currStopsInx].floor < call.src):
                                currStopsInx += 1
                            else:
                                myTime = max(elv.waitingUp[currStopsInx - 1].actualTime,
                                             elv.waitingUp[currStopsInx - 1].callTime)
                                myTime += elv.tag + elv.speed * (call.src - elv.waitingUp[currStopsInx - 1].floor)
                                tup = [elv.id, myTime, 1]
                                tempEvTime.append(tup)
                                # end the while
                                currStopsInx = elv.waitingUp.qsize()


                # if elv DOWN -> waitingUp
                else:
                    currStopsInx = 0
                    while currStopsInx < (elv.waitingUp.qsize()):
                        if (elv.waitingUp[currStopsInx].floor > call.src):
                            currStopsInx += 1
                        else:
                            myTime = max(elv.waitingUp[currStopsInx - 1].actualTime,
                                         elv.waitingUp[currStopsInx - 1].callTime)
                            myTime += elv.tag + elv.speed * (call.src - elv.waitingUp[currStopsInx - 1].floor)
                            tup = [elv.id, myTime, 1]
                            tempEvTime.append(tup)
                            # end the while
                            currStopsInx = elv.waitingUp.qsize()

            # if call DOWN
            else:
                # if elv DOWN
                if (elv.flag == DOWN):
                    # if didnt pass the call yet -> crrStops
                    if (elv.pos > call.src):
                        currStopsInx = 0
                        while currStopsInx < (elv.currStops.qsize()):
                            if (elv.currStops[currStopsInx].floor > call.src):
                                currStopsInx += 1
                            else:
                                myTime = max(elv.currStops[currStopsInx - 1].actualTime,
                                             elv.currStops[currStopsInx - 1].callTime)
                                myTime += elv.tag + elv.speed * (elv.currStops[currStopsInx - 1].floor - call.src)
                                tup = [elv.id, myTime, 0]
                                tempEvTime.append(tup)
                                # end the while
                                currStopsInx = elv.currStops.qsize()
                    # else: passed -> WLDown
                    else:
                        currStopsInx = 0
                    while currStopsInx < (elv.waitingDown.qsize()):
                        if (elv.waitingDown[currStopsInx].floor > call.src):
                            currStopsInx += 1
                        else:
                            myTime = max(elv.waitingDown[currStopsInx - 1].actualTime,
                                         elv.waitingDown[currStopsInx - 1].callTime)
                            myTime += elv.tag + elv.speed * (elv.waitingDown[currStopsInx - 1].floor - call.src)
                            tup = [elv.id, myTime, -1]
                            tempEvTime.append(tup)
                            # end the while
                            currStopsInx = elv.waitingDown.qsize()
                # elv down -> WLDown
                else:
                    currStopsInx = 0
                    while currStopsInx < (elv.waitingDown.qsize()):
                        if (elv.waitingDown[currStopsInx].floor < call.src):
                            currStopsInx += 1
                        else:
                            myTime = max(elv.waitingDown[currStopsInx - 1].actualTime,
                                         elv.waitingDown[currStopsInx - 1].callTime)
                            myTime += elv.tag + elv.speed * (call.src - elv.waitingDown[currStopsInx - 1].floor)
                            #the list contains: elevIndex, the real time to call src , down=-1.
                            tup = [elv.id, myTime, -1]
                            tempEvTime.append(tup)
                            # end the while
                            currStopsInx = elv.waitingDown.qsize()

        minTime = tempEvTime[0]
        for tup in tempEvTime:
            if minTime[1] > tup[1]:
                minTime = tup
        if (minTime[2] == 0):
            self.building.elevators[minTime[0]].addToCurr(call, minTime[1])
        elif (minTime[2] == 1):
            self.building.elevators[minTime[0]].addToWaitingUp(call, minTime[1])
        elif (minTime[2] == -1):
            self.building.elevators[minTime[0]].addToWaitingDown(call, minTime[1])

        #call to function which update the lists of the chosen elevator
        listsUpdate (minTime[0])


        return fastesElev

    # function which update all the elevators lists----------missing code!
    def listsUpdate (elvIndex: Elevator):
        currStopsInx = 0
        while currStopsInx < (elvIndex.waitingDown.qsize()):
            if (elvIndex.flag == UP):
                elvIndex.currStops[currStopsInx][FloorDetailsUp]
                currStopsInx += 1
            else:
            elvIndex.currStops[currStopsInx][FloorDetailsDown()]


        #updating the other lists
        for currStop in elvIndex.waitingDown:
        for currStop in elvIndex.waitingUp:
            currStop = max(F)

    #In this method there are 3 goals: 1-update each list times.
    #2-update the flags and the lists. 3-update the pos and stop in the calls floors
    #the function run each 0.1 sec and updates the data
    def update(self):
        #loop all the elevators
        for elv in self.building.elevators:
            #if the currstops list isEmpty -> change the flag value and update the
            #currstops list
            if (len(elv.currStops)==0):
                if (elv.flag == UP):
                    elv.flag = DOWN
                    elv.currStops = elv.waitingDown#if it works well
                else:
                    elv.flag = UP
                    elv.currStops = elv.waitingUp

            #updating the elev pos and the currStops list if we stop
            #the elv up
            if (elv.flag==UP):
                newPos = elv.pos + elv.speed*0.1
                #
                if (math.ceil(newPos) - math.ceil(elv.pos) == 0):
                    elv.pos = newPos
                else:
                    if (elv.currStops[0] == math.floor(elv.pos)):
                        elv.pos = elv.pos = math.floor(elv.pos)
                        elv.currStops.remove(math.floor(elv.pos))
                    else:
                        elv.pos = newPos

            #the elv is down
            else:
                newPos = elv.pos - elv.speed*0.1
                if (math.ceil(newPos) - math.ceil(elv.pos) == 0):
                    elv.pos=newPos
                #we changed the begining number of the floor
                else:
                    #if we have to stop there
                    if(elv.currStops[0]==math.ceil(elv.pos)):
                        elv.pos=math.ceil(elv.pos)
                        elv.currStops.remove(math.ceil(elv.pos))

            # increment the elv to the curr directon
        #   elv.pos = elv.pos + elv.speed*0.1

# fastestElv = self.speedest(self.building.elevators)
#
#     #insert the elevators into the lists
#     for elv in self.building.elevators:
#         fastestElv.put(elv)
#     #if self.building.elevators
#
# def speedest (self, elevators):
#     if(self.__sizeof__()==0)
#         self.upElv.append(elevators)
#     else:
#         for i in range(0, self.size()):
#             if (elevators.priority >= self.q[i].priority):
#                 if (i == (self.size() - 1)):
#                     self.q.insert(i + 1, elevators)
#                 else:
#                         continue
#             else:
#                 self.q.insert(i, elevators)
#
#     fastest =queue.PriorityQueue()


#
# def allocate ()
#
# def fastest_To_Floor()
#
# def update()
