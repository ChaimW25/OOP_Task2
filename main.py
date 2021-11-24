from Building import *
from Allocate import *
from Elevator import *
from Call import *
from CSVfun import *

if __name__ == '__main__':
    bJson = "B5.json"
    cCsv = "Calls_d.csv"
    outputCsv = "output/output.csv"
    a = Allocate(bJson, cCsv)
    # for i in range(0, a.calls[len(a.calls)-1].time+120, 0.1):
    timeToEnd = a.calls[len(a.calls) - 1].time + 120
    i = 0
    indexC = 0
    # this while emulate the time passing by
    JUMP = 0.1
    while i < timeToEnd:

        if a.calls[indexC].time <= i:
            elvIndex = a.fastes_to_floor(a.calls[indexC])
            # we need to add this indexElv to the output file
            writeToCsvFile(a.calls[indexC], outputCsv, elvIndex)
            indexC += 1
        a.update(JUMP, i)
        print(i)
        # updateElevPos()
        i += JUMP

