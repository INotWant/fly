class Coordinate:
    # z 表示海拔，必须大于等于 0
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-8 and abs(self.y - other.y) < 1e-8 and abs(self.z - other.z) < 1e-8

    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)

    def getCoordinate(self):
        return self.x, self.y, self.z

    def setCoordinate(self, x, y, z):
        assert z > 0
        self.x = x
        self.y = y
        self.z = z

    def setCoordinateByObj(self, coordinate):
        if isinstance(coordinate, Coordinate):
            self.setCoordinate(coordinate.x, coordinate.y, coordinate.z)
        else:
            raise ValueError("coordinate must be a object of Coordinate!")
