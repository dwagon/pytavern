""" Door definition """
from .thing import Thing


##############################################################################
class Door(Thing):
    """ Door - Walls you can walk through"""
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.repr = 'D'
        self.category = 'structure'
        self.permeable = True

# EOF
