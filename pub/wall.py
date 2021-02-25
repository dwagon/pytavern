""" Definition of Wall base class """
from thing import Thing


##############################################################################
class Wall(Thing):
    """ Definition of a Wall - immobile Thing """
    def __init__(self, pub, pos):
        super().__init__(pub, "Wall", pos)
        self.repr = "#"

# EOF
