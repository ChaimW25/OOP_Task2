import json

from Elevator import *


class Building:
    def __init__(self, buildingJson):
        data = json.loads(buildingJson)
        self.minFloor = data['_minFloor']
        self.maxFloor = data['_maxFloor']
        self.elevators = []

        for i in data['_elevators']:
            self.elevators.append(
                Elevator(i['_id'], i['_speed'], i["_minFloor"], i["_maxFloor"], i["_closeTime"], i["_openTime"],
                         i["_startTime"], i["_stopTime"]))

# Serializing json and
# Writing json file


# Product deserializedProduct = JsonConvert.DeserializeObject<Product>(output);
