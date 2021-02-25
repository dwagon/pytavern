""" Definition of Furniture classes """
from thing import Thing


##############################################################################
class Table(Thing):
    """ Definition of a Table - immobile Thing """
    def __init__(self, pub, name="Table", pos=None):
        super().__init__(pub, name, pos)
        self.repr = "T"

# EOF
