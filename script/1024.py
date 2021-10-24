import json

from ImageUtils import miningPoint

if __name__ == '__main__':
    imageName = "data/image/1024.png"
    designFilePath = "data/design/1024.json"
    customDimension = (40, 80)
    xAxisPointNum = 20
    yAxisPointNum = 40
    points = miningPoint(imageName, customDimension, xAxisPointNum, yAxisPointNum)

    count = 0
    startCoordinates = []
    targetCoordinates = []
    baseZ = 20
    for x in range(xAxisPointNum):
        for y in range(yAxisPointNum):
            if points[x][y] == 1:
                count = count + 1
                targetCoordinates.append((0, y * 3, (xAxisPointNum - x) * 3 + baseZ))

    xAxisNumInStart = 10
    for i in range(count):
        startCoordinates.append((i % xAxisNumInStart * 4, i // xAxisNumInStart * 4, 0))

    targetCoordinatesArr = [targetCoordinates]
    design = {"start": startCoordinates, "target": targetCoordinatesArr}
    with open(designFilePath, "w") as f:
        json.dump(design, f)
