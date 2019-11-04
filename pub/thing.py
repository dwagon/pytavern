""" Generic Base Class for something that exists in space and time """


class Thing:
    """ Define a thing """
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} @ {self.x}, {self.y}"

# EOF
