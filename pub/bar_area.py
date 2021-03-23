""" Definition of Bar base class """
from thing import Thing


##############################################################################
class Bar(Thing):
    """ Definition of a Bar - immobile Thing """
    def __init__(self, pub, pos):
        super().__init__(pub, "Bar", pos)
        self.repr = "O"

# EOF
