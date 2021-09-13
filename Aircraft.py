from Coordinate import Coordinate
import threading
import copy


class Aircraft:
    __slots__ = ("id", "currCoordinate", "targetCoordinates", "trackCoordinates", "trackMaxLength", "_lock")

    def __init__(self, id):
        self.id = id
        self.currCoordinate = None
        # (临时目标坐标，最终目标坐标)
        self.targetCoordinates = [None, None]
        # 轨迹坐标，相邻元素间隔时间为基本时间单元
        self.trackCoordinates = ([], [], [])
        self.trackMaxLength = None
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
        assert z >= 0
        self.setTmpTargetCoordinateByObj(Coordinate(x, y, z))

    def setTmpTargetCoordinateByObj(self, coordinate):
        if not isinstance(coordinate, Coordinate):
            raise ValueError("coordinate must be a object of Coordinate!")
        assert coordinate.z >= 0
        self.targetCoordinates[0] = coordinate

    def getTmpTargetCoordinate(self):
        return self.targetCoordinates[0]

    def setFinalTargetCoordinate(self, x, y, z):
        assert z >= 0
        self.setFinalTargetCoordinateByObj(Coordinate(x, y, z))

    def setFinalTargetCoordinateByObj(self, coordinate):
        if not isinstance(coordinate, Coordinate):
            raise ValueError("coordinate must be a object of Coordinate!")
        assert coordinate.z >= 0
        self.targetCoordinates[1] = coordinate

    def getFinalTargetCoordinate(self):
        return self.targetCoordinates[1]

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
            return
        self._lock.acquire()
        try:
            if len(self.trackCoordinates[0]) > 1:
                self.trackCoordinates[0].pop(0)
                self.trackCoordinates[1].pop(0)
                self.trackCoordinates[2].pop(0)
        finally:
            self._lock.release()

    def getTrackCoordinates(self):
        self._lock.acquire()
        try:
            return copy.deepcopy(self.trackCoordinates)
        finally:
            self._lock.release()
