""" Customer """
import random

from .coord import Coord
from .person import Person


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.demands = {'amount': 0, 'time': 0}
        self.satisfaction = 9
        self.target = None
        self.repr = 'C'
        self.mode = 'go_stool'

    ##########################################################################
    def turn(self):
        """ Time passing """
        return self.move(self.pick_target, self.sit)

    ##########################################################################
    def sit(self):
        """ Sit down at the stool """
        if self.mode != 'go_stool':
            return True
        for stl in self.tavern.stools:
            if self.target == stl.pos and not stl.occupied:
                stl.occupied = True
                self.mode = 'drink'
                self.generate_demand()
                self.pos = self.target
                print(f"{self} sat on {stl}")
                break
        else:
            self.target = None
        return True

    ##########################################################################
    def pick_target(self):
        """ Pick where to go """
        # Still Thirsty
        if self.mode == 'drink':
            return self.pos
        # Satisfied
        if not self.satisfaction:
            self.mode = 'go_home'
            print(f"{self} had enough")
            for stl in self.tavern.stools:
                if stl.pos == self.pos:
                    stl.occupied = False
            return Coord(0, 0)
        # Just arrived
        if self.mode == 'go_stool':
            if not self.target:
                random.shuffle(self.tavern.stools)
                for stl in self.tavern.stools:
                    if not stl.occupied:
                        return stl.pos
        return None

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        self.satisfaction -= 1
        return grab

    ##########################################################################
    def generate_demand(self):
        """ Generate new demand for something """
        self.demands = {'time': self.tavern.time, 'amount': random.randint(1, 3)}

# EOF
