from Building import *
from Allocate import *
from Elevator import *
from Call import *

if __name__ == '__main__':
    bJson = "building/B1.json"
    cCsv = "calls/Calls_a.csv"
    outputCsv = "output/output.csv"
    a = Allocate(bJson, cCsv, outputCsv)
    print('')
    # for i in range(0, a.calls[len(a.calls)-1].time+120, 0.1):
    timeToEnd = a.calls[len(a.calls) - 1].time + 120
    i = 0
    indexC = 0
    # this while emulate the time passing by
    while i < timeToEnd:

        if a.calls[indexC].time <= i:
            elvIndex = a.fastes_to_floor(a.calls[indexC])
            # we need to add this indexElv to the output file
        a.update()

        print(i)
        # updateElevPos()
        i += 0.1
        indexC += 1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
#     ll = []
#     tmp: FloorDetailsUp
#     for i in range(10):
#         if i % 2 == 0:
#             tmp = FloorDetailsUp(i, 26, 89)
#         else:
#             tmp = FloorDetailsUp(-i, 26, 89)
#         ll.append(tmp)
#     ll.sort(reverse=True, key=lambda fd: fd.floor)
#     for i in range(len(ll)):
#         a.building.elevators[1].currStops.append(ll[i])
#         print(a.building.elevators[1].currStops[i-1])

    # print(a.building.elevators[1].currStops.append(ll))