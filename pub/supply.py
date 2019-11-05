""" A supply of something """
from thing import Thing


##############################################################################
class Supply(Thing):
    """ Definition of supply """
    def __init__(self, pub, name, x, y):
        super().__init__(pub, name, x, y)
        self.amount = 99
        self.repr = 'S'

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
