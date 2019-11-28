""" Stool definition """
from .thing import Thing


##############################################################################
class Stool(Thing):
    """ Stool - what customers sit on """
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.repr = '#'
        self.occupied = False
        self.category = 'furniture'

# EOF
