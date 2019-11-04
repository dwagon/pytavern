""" A supply of something """
from thing import Thing


##############################################################################
class Supply(Thing):
    """ Definition of supply """
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.amount = 0
        self.repr = 'S'

# EOF
