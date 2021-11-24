import csv
from random import random, randint
from Call import *


# the function with a simple test
# make sure the files are empty (the tmp one and the output one) in the test we erase them

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

# /////////////////
# //////TEST//////
# ///////////////

calls = []
callCsv = 'Calls_b.csv'

csvfileName = "csv_file.csv"
# deleting this files
open(csvfileName, 'w').close()

with open(callCsv, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        calls.append(Call(line[1], line[2], line[3], line[4], line[5]))
for call in calls:
    writeToCsvFile(call, csvfileName, randint(1, 8))

with open(csvfileName, 'r') as csv_file:
    csv_reader_fix = csv.reader(csv_file)
    for line in csv_reader_fix:
        print(line)
