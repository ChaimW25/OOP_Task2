import csv
import queue

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

        # for elv in self.building.elevators:
        #     # both up and in the way
        #     if (elv.flag == UP and call.src < call.dest and elv.currStops[0] < call.src):
        #         for floor in elv.currStops:
        #             if (floor < call.src):
        #                 continue
        #             else:
        #                 break

            # we need to put the actual call in the elev
        return fastesElev

    def update(self):
        for elv in self.building.elevators:
            if (len(elv.currStops)==0):
                if (elv.flag == UP):
                    elv.flag = DOWN
                    elv.currStops = elv.waitingDown
                else:
                    elv.flag = UP
                    elv.currStops = elv.waitingUp

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
