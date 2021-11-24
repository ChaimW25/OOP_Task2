from Building import *
from Allocate import *
from Elevator import *
from Call import *

# fileName - file name of the temporary csv file
def writeToCsvFile(call: Call, fileName: str, elevID: int):
    # open the file in the a mode
    with open(fileName, 'a', newline="") as file_csv:
        # create the csv writer
        writer = csv.writer(file_csv)
        temp_arr = []
        temp_arr.append("Elevator call")
        temp_arr.append(call.time)
        temp_arr.append(call.src)
        temp_arr.append(call.dest)
        # the call has been received (1)
        temp_arr.append(1)
        temp_arr.append(elevID)
        # write a row to the csv file
        writer.writerow(temp_arr)


if __name__ == '__main__':
    bJson = "building/B4.json"
    cCsv = "calls/Calls_d.csv"
    outputCsv = "output/output.csv"
    a = Allocate(bJson, cCsv)
    # for i in range(0, a.calls[len(a.calls)-1].time+120, 0.1):

    # kastach -----------------------
    for call in a.calls:
        writeToCsvFile(call, outputCsv, 0)
    # kastach -----------------------


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
        # print(i)
        # updateElevPos()
        i += JUMP

