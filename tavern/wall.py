""" Wall definition """
from .thing import Thing


##############################################################################
class Wall(Thing):
    """ Wall - try not to walk through them"""
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.category = 'structure'
        self.permeable = False

    @property
    def repr(self):
        """ Return the representation of the wall """
        val = "?"
        if self.pos.x == 0:
            if self.pos.y == 0 or self.pos.y == self.tavern.size_y - 1:
                val = "+"
            else:
                val = "|"
        elif self.pos.x == self.tavern.size_x - 1:
            if self.pos.y == 0 or self.pos.y == self.tavern.size_y - 1:
                val = "+"
            else:
                val = "|"
        elif self.pos.y == 0:
            val = "-"
        elif self.pos.y == self.tavern.size_y - 1:
            val = "-"
        return val

# EOF
