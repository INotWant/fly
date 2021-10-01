from collections import Iterable

from Coordinate import Coordinate
import threading
import copy


class Aircraft:
    __slots__ = (
    "id", "currCoordinate", "tmpTargetCoordinate", "targetCoordinates", "trackCoordinates", "trackMaxLength", "_lock")

    def __init__(self, id, trackMaxLength=None):
        self.id = id
        self.currCoordinate = None
        # 临时目标坐标
        self.tmpTargetCoordinate = None
        # 最终目标坐标集
        self.targetCoordinates = []
        # 轨迹坐标，相邻元素间隔时间为基本时间单元
        self.trackCoordinates = ([], [], [])
        self.trackMaxLength = trackMaxLength
        # 多线程锁，使获取的 trackCoordinates 最新
        self._lock = threading.Lock()

    def setCurrCoordinate(self, x, y, z):
        self.currCoordinate = Coordinate(x, y, z)
        self.trackCoordinates[0].append(x)
        self.trackCoordinates[1].append(y)
        self.trackCoordinates[2].append(z)

    def setCurrCoordinateByObj(self, coordinate):
        if isinstance(coordinate, Coordinate):
            self.currCoordinate = coordinate
        else:
            raise ValueError("coordinate must be a object of Coordinate!")

    def setTmpTargetCoordinate(self, x, y, z):
        self.setTmpTargetCoordinateByObj(Coordinate(x, y, z))

    def setTmpTargetCoordinateByObj(self, coordinate):
        if not isinstance(coordinate, Coordinate):
            raise ValueError("coordinate must be a object of Coordinate!")
        self.tmpTargetCoordinate = coordinate

    def getTmpTargetCoordinate(self):
        return self.tmpTargetCoordinate

    def addFinalTargetCoordinate(self, x, y, z):
        self.addFinalTargetCoordinateByObj(Coordinate(x, y, z))

    def addFinalTargetCoordinateByObj(self, coordinate):
        if not isinstance(coordinate, Coordinate):
            raise ValueError("coordinate must be a object of Coordinate!")
        self.targetCoordinates.append(coordinate)

    def setFinalTargetCoordinatesByObj(self, coordinates):
        if not isinstance(coordinates, Iterable):
            raise ValueError("coordinates must be iterable!")
        for coordinate in coordinates:
            self.addFinalTargetCoordinateByObj(coordinate)

    def getFinalTargetCoordinates(self):
        return self.targetCoordinates

    def getFinalTargetCoordinate(self):
        if len(self.targetCoordinates) == 0:
            return None
        return self.targetCoordinates[0]

    def popFinalTargetCoordinate(self):
        if len(self.targetCoordinates) == 0:
            return None
        return self.targetCoordinates.pop(0)

    def isArriveTargetCoordinate(self):
        if self.currCoordinate is None or self.getFinalTargetCoordinate() is None:
            return False
        return self.currCoordinate == self.getFinalTargetCoordinate()

    def addTrackCoordinate(self):
        """
        每隔基本时间单元 t 调一次
        """
        coordinate = self.getTmpTargetCoordinate()
        self._lock.acquire()
        try:
            self.trackCoordinates[0].append(coordinate.x)
            self.trackCoordinates[1].append(coordinate.y)
            self.trackCoordinates[2].append(coordinate.z)
            if not self.trackMaxLength is None and len(self.trackCoordinates[0]) > self.trackMaxLength:
                self.trackCoordinates[0].pop(0)
                self.trackCoordinates[1].pop(0)
                self.trackCoordinates[2].pop(0)
        finally:
            self._lock.release()

    def deleteOneTrackCoordinate(self):
        if len(self.trackCoordinates[0]) == 1:
            return False
        self._lock.acquire()
        try:
            if len(self.trackCoordinates[0]) > 1:
                self.trackCoordinates[0].pop(0)
                self.trackCoordinates[1].pop(0)
                self.trackCoordinates[2].pop(0)
                return True
        finally:
            self._lock.release()

    def getTrackCoordinates(self):
        self._lock.acquire()
        try:
            return copy.deepcopy(self.trackCoordinates)
        finally:
            self._lock.release()
