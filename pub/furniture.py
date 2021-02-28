""" Definition of Furniture classes """
from thing import Thing


##############################################################################
class Table(Thing):
    """ Definition of a Table - immobile Thing """
    def __init__(self, pub, name="Table", pos=None):
        super().__init__(pub, name, pos)
        self.repr = "T"
        self.all_positions = set()

    def add_position(self, pos):
        """ Add the squares that the table actually takes up """
        self.all_positions.add(pos)

    def positions(self):
        """ Return all the squares that the table takes up """
        return self.all_positions


##############################################################################
class Chair(Thing):
    """ Definition of a Chair - immobile Thing """
    def __init__(self, pub, name="Chair", pos=None):
        super().__init__(pub, name, pos)
        self.repr = "h"
        self.occupant = None
        self.permeable = True

    def sit_down(self, occ):
        """ Occupy the chair """
        self.occupant = occ
        self.permeable = False

    def get_up(self):
        """ Relinquish the chair """
        self.occupant = None
        self.permeable = True

# EOF
