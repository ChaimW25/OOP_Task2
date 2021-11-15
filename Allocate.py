import csv

import Building
import json

from Call import *

class Allocate:

    def __init__(self, buildingJson, callCsv, outputCsv):
        self.building = Building(buildingJson)
        self.calls = []
        with open('callCsv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.calls.append(Call(line[1], line[2], line[3], line[4], line[5]))

    def allocate ()
