""" A supply of something """
from thing import Thing


##############################################################################
class Supply(Thing):
    """ Definition of supply """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.amount = 99
        self.repr = 'S'

    ##########################################################################
    def is_empty(self):
        """ Is the supply empty """
        return self.amount == 0

    ##########################################################################
    def take(self, desired_amount):
        """ Take some of the supply """
        if self.amount >= desired_amount:
            grab = desired_amount
        else:
            grab = min(desired_amount, self.amount)
        self.amount -= grab
        print(f"{self.amount} of supplies left")
        return grab

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        pass

# EOF
