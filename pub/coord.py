""" Coordinate system """


class OutOfBoundsError(Exception):
    """ Coordinate is out of bounds """
    pass


class Coord:
    """ Coordinate system class """
    def __init__(self, x, y, maxx=999, maxy=999):
        if x < 0 or y < 0 or x > maxx or y > maxy:
            raise OutOfBoundsError
        self.x = x
        self.y = y

    def __eq__(self, a):
        return self.x == a.x and self.y == a.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __repr__(self):
        return f"{self.x}, {self.y}"

# EOF
