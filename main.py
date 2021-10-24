import json

from Aircraft import Aircraft
from Controller import Controller

if __name__ == '__main__':
    distanceThreshold = 0.05
    # designPath = "data/design/heart.json"
    # designPath = "data/design/double_heart.json"
    # designPath = "data/design/font_2.json"
    # designPath = "data/design/blessMotherland.json"
    designPath = "data/design/1024.json"
    with open(designPath, "r") as f:
        design = json.load(f)
    startCoordinates = design["start"]
    targetCoordinatesArr = design["target"]

    aircrafts = []
    for i in range(len(startCoordinates)):
        aircraft = Aircraft(i)
        startCoordinate = startCoordinates[i]
        aircraft.setCurrCoordinate(startCoordinate[0], startCoordinate[1], startCoordinate[2])
        for j in range(len(targetCoordinatesArr)):
            targetCoordinate = targetCoordinatesArr[j][i]
            aircraft.addFinalTargetCoordinate(targetCoordinate[0], targetCoordinate[1], targetCoordinate[2])
        aircrafts.append(aircraft)

    controller = Controller(distanceThreshold, aircrafts, singleMovementDistance=1)
    controller.start()
