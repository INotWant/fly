import json

from ImageUtils import miningPoint

if __name__ == '__main__':
    imageName = "data/image/heart.png"
    # imageName = "data/image/double_heart.png"
    customDimension = (100, 100)
    xAxisPointNum = 20
    yAxisPointNum = 20

    points = miningPoint(imageName, customDimension, xAxisPointNum, yAxisPointNum)
    # 针对 heart 人工修正
    points[3][17] = 0
    points[3][18] = 1
    points[3][18] = 1
    points[5][19] = 1
    points[9][19] = 1
    points[11][18] = 1
    points[12][16] = 0
    points[11][3] = 0
    points [11][17] = 0

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
    with open("data/design/heart.json", "w") as f:
    # with open("data/design/double_heart.json", "w") as f:
        json.dump(design, f)
