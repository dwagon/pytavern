""" A supply of something """
import colorama
from thing import Thing


##############################################################################
class Supply(Thing):
    """ Definition of supply """
    def __init__(self, pub, name, pos, kind, amount=20):
        super().__init__(pub, name, pos)
        self.amount = amount
        self.kind = kind
        self.permeable = True

    ##########################################################################
    def repr(self):
        """ Mutable representation """
        if self.amount:
            col = colorama.Fore.GREEN
        else:
            col = colorama.Fore.RED
        return f'{col}S'

    ##########################################################################
    def desc_line(self):
        """ Status line """
        if self.amount:
            col = colorama.Fore.GREEN
        else:
            col = colorama.Fore.RED
        out = f"{col}{self.name} {self.kind} {self.amount} @{self.pos}"
        return out

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
        print(f"{self} {self.amount} of supplies left")
        return grab

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        pass

# EOF
