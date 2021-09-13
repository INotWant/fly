import math

import numpy as np

from Coordinate import Coordinate


def calculateDirectionVector(coordinate1, coordinate2):
    """
    方向向量 = (x2 - x1, y2 - y1, z2 - z1) / √((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)
    """
    if not (isinstance(coordinate1, Coordinate) and isinstance(coordinate2, Coordinate)):
        raise ValueError("coordinate1/coordinate2 must be a object of Coordinate!")
    distance = math.sqrt(sum((
        math.pow(coordinate2.x - coordinate1.x, 2),
        math.pow(coordinate2.y - coordinate1.y, 2),
        math.pow(coordinate2.z - coordinate1.z, 2),
    )))
    if distance < 1e-8:
        return Coordinate(0, 0, 0)
    x = (coordinate2.x - coordinate1.x) / distance
    y = (coordinate2.y - coordinate1.y) / distance
    z = (coordinate2.z - coordinate1.z) / distance
    return Coordinate(x, y, z)


def calculateEndPoint(startCoordinate, directionVector, t):
    if not (isinstance(startCoordinate, Coordinate) and isinstance(directionVector, Coordinate)):
        raise ValueError("startCoordinate/directionVector must be a object of Coordinate!")
    x = startCoordinate.x + t * directionVector.x
    y = startCoordinate.y + t * directionVector.y
    z = startCoordinate.z + t * directionVector.z
    return Coordinate(x, y, z)


def isOnTheLine(coordinate1, coordinate2, coordinate3):
    """
    检查坐标3是否在坐标1和坐标2组成的线段内
    注：已知三点共线
    :param coordinate1: 坐标1
    :param coordinate2: 坐标2
    :param coordinate3: 坐标3
    :return: 若在返回 True，否则返回 False
    """
    xMax = max(coordinate1.x, coordinate2.x)
    xMin = min(coordinate1.x, coordinate2.x)
    yMax = max(coordinate1.y, coordinate2.y)
    yMin = min(coordinate1.y, coordinate2.y)
    zMax = max(coordinate1.z, coordinate2.z)
    zMin = min(coordinate1.z, coordinate2.z)
    if xMax >= coordinate3.x >= xMin:
        if yMax >= coordinate3.y >= yMin:
            if zMax >= coordinate3.z >= zMin:
                return True
    return False


def calculateTheNearestDistanceFor2PathWithinSpecialTime(
        startCoordinate1, directionVector1,
        startCoordinate2, directionVector2,
        end=1):
    """
    运动路径1：(x1, y1, z1) + t*(a1, b1, c1)
    运动路径2：(x2, y2, z2) + t*(a2, b2, c2)
    距离的平方：((x1-x2) + t*(a1-a2))**2 + ((y1-y2) + t*(b1-b2))**2 + ((z1-z2) + t*(c1-c2))**2
    :param startCoordinate1: 起始坐标1 (x1, y1, z1)
    :param directionVector1: 方向向量1 (a1, b1, c1)
    :param startCoordinate2: 起始坐标2 (x2, y2, z2)
    :param directionVector2: 方向向量2 (a2, b2, c2)
    :param end: 时间区间 (0, end]
    :return: 时间区间 (0, end] 内，两点间的最近距离
    """
    if not (isinstance(startCoordinate1, Coordinate) and isinstance(startCoordinate2, Coordinate)):
        raise ValueError("startCoordinate1/2 must be a object of Coordinate!")
    if not (isinstance(directionVector1, Coordinate) and isinstance(directionVector2, Coordinate)):
        raise ValueError("directionVector1/2 must be a object of Coordinate!")
    a1, b1, c1 = directionVector1.getCoordinate()
    a2, b2, c2 = directionVector2.getCoordinate()
    x1, y1, z1 = startCoordinate1.getCoordinate()
    x2, y2, z2 = startCoordinate2.getCoordinate()
    a = math.pow(a1 - a2, 2) + math.pow(b1 - b2, 2) + math.pow(c1 - c2, 2)
    b = 2 * (x1 - x2) * (a1 - a2) + 2 * (y1 - y2) * (b1 - b2) + 2 * (z1 - z2) * (c1 - c2)
    c = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    # 二次元的系数为 0 的情况
    if abs(a) < 1e-8:
        return math.sqrt(c if b > 0 else b * end + c)
    mid = -b / (2 * a)
    if end < mid:
        ret = a * math.pow(end, 2) + b * end + c
    elif 0 > mid:
        ret = c
    else:
        ret = c - b ** 2 / (4 * a)
    return math.sqrt(ret)


def calculateTheNearestDistanceFor1PathWithinSpecialTime(
        startCoordinate1, directionVector1,
        startCoordinate2,
        end=1):
    """
    运动路径1：(x1, y1, z1) + t*(a1, b1, c1)
    第二点不动：(x2, y2, z2)
    :param startCoordinate1: 起始坐标1 (x1, y1, z1)
    :param directionVector1: 方向向量1 (a1, b1, c1)
    :param startCoordinate2: 起始坐标2 (x2, y2, z2)
    :param end: 时间区间 (0, end]
    :return: 时间区间 (0, end] 内，两点间的最近距离
    """
    return calculateTheNearestDistanceFor2PathWithinSpecialTime(
        startCoordinate1, directionVector1,
        startCoordinate2, Coordinate(0, 0, 0),
        end)


def calculateVectorAngle(vector1, vector2):
    """
    求两个向量间的夹角
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 夹角 [0-180]
    """
    x = np.array((vector1.x, vector1.y, vector1.z))
    y = np.array((vector2.x, vector2.y, vector2.z))
    lx, ly = np.sqrt(x.dot(x)), np.sqrt(y.dot(y))
    cosAngle = x.dot(y) / (lx * ly)
    return np.arccos(cosAngle) * 180 / np.pi
