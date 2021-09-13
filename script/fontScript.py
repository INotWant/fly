import json

from ImageUtils import miningPoint

if __name__ == '__main__':
    no = 2
    imageName = "data/font_%s.png" % no
    designFilePath = "data/design/font_%s.json" % no
    customDimension = (80, 80)
    xAxisPointNum = 20
    yAxisPointNum = 20
    points = miningPoint(imageName, customDimension, xAxisPointNum, yAxisPointNum)

    count = 0
    startCoordinates = []
    targetCoordinates = []
    baseZ = 20
    for x in range(xAxisPointNum):
        for y in range(yAxisPointNum):
            if points[x][y] == 1:
                count = count + 1
                targetCoordinates.append((y * 3, 0, (xAxisPointNum - x) * 3 + baseZ))

    xAxisNumInStart = 10
    for i in range(count):
        startCoordinates.append((i % xAxisNumInStart * 4, i // xAxisNumInStart * 4, 0))

    design = {"start": startCoordinates, "target": targetCoordinates}
    with open(designFilePath, "w") as f:
        json.dump(design, f)
