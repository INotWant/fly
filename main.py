import json

from Aircraft import Aircraft
from Controller import Controller

if __name__ == '__main__':
    distanceThreshold = 2
    designPath = "data/design/heart.json"
    # designPath = "data/design/double_heart.json"
    # designPath = "data/design/font_2.json"
    with open(designPath, "r") as f:
        design = json.load(f)
    startCoordinates = design["start"]
    targetCoordinates = design["target"]

    aircrafts = []
    for i in range(len(startCoordinates)):
        aircraft = Aircraft(i)
        startCoordinate = startCoordinates[i]
        targetCoordinate = targetCoordinates[i]
        aircraft.setCurrCoordinate(startCoordinate[0], startCoordinate[1], startCoordinate[2])
        aircraft.setFinalTargetCoordinate(targetCoordinate[0], targetCoordinate[0], targetCoordinate[2])
        aircrafts.append(aircraft)

    controller = Controller(distanceThreshold, aircrafts, t=0.05, v=8)
    controller.start()
