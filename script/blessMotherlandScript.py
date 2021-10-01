import json

import numpy as np

from ImageUtils import miningPoint

if __name__ == '__main__':
    imagePath = "data/image/%s.png"
    fonts = ["祝", "福", "祖", "国"]
    designFilePath = "data/design/blessMotherland.json"

    customDimension = (80, 80)
    xAxisPointNum = 20
    yAxisPointNum = 20
    pointsArr = []

    for font in fonts:
        imageName = imagePath % font
        pointsArr.append(miningPoint(imageName, customDimension, xAxisPointNum, yAxisPointNum))

    maxCount = 0
    for points in pointsArr:
        currCount = np.sum(points)
        if currCount > maxCount:
            maxCount = currCount

    startCoordinates = []
    targetCoordinatesArr = []
    xAxisNumInStart = 10
    baseZ = 20
    for points in pointsArr:
        currTargetCoordinates = []
        for x in range(xAxisPointNum):
            for y in range(yAxisPointNum):
                if points[x][y] == 1:
                    currTargetCoordinates.append((0, y * 3, (xAxisPointNum - x) * 3 + baseZ))
        if len(currTargetCoordinates) < maxCount:
            increaseCount = maxCount - len(currTargetCoordinates)
            for i in range(increaseCount):
                currTargetCoordinates.append((i % xAxisNumInStart * 4, i // xAxisNumInStart * 4, 0))
        targetCoordinatesArr.append(currTargetCoordinates)

    for i in range(maxCount):
        startCoordinates.append((i % xAxisNumInStart * 4, i // xAxisNumInStart * 4, 0))

    design = {"start": startCoordinates, "target": targetCoordinatesArr}
    with open(designFilePath, "w") as f:
        json.dump(design, f)
