""" Definition of Door base class """
from thing import Thing


##############################################################################
class Door(Thing):
    """ Definition of a Door - immobile Thing """
    def __init__(self, pub, pos):
        super().__init__(pub, "Door", pos)
        self.repr = "+"
        self.permeable = True

# EOF
