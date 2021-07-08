""" A supply of something """
from .thing import Thing


##############################################################################
class Supply(Thing):
    """ Definition of supply """
    def __init__(self, tavern, name, pos, supplytype):
        super().__init__(tavern, name, pos)
        self.amount = 99
        self.repr = '^'
        self.supplytype = supplytype
        self.category = 'installation'

    ##########################################################################
    def take(self, desired_amount):
        """ Take some of the supply """
        if self.amount >= desired_amount:
            grab = desired_amount
        else:
            grab = min(desired_amount, self.amount)
        self.amount -= grab
        return grab

# EOF
