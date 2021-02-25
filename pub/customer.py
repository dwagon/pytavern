""" Customer """
import random

from coord import Coord
from person import Person


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.demands = {}
        self.satisfaction = 9
        self.target = None
        self.repr = 'C'

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        # Thirsty
        if not self.demands.get('amount', 0):
            self.generate_demand(tick)
            self.satisfaction -= 1
        # Satisfied
        if not self.satisfaction:
            self.target = Coord(0, 0)
            print(f"{self} had enough")
        else:
            # Move away from the door
            if self.pos == Coord(0, 0):
                self.target = self.pub.free_location()
        if self.target:
            route = list(self.pub.find_route(self.pos, self.target))
            if len(route) <= 1:
                if self.target == Coord(0, 0):
                    return False
                else:
                    self.target = None
            else:
                self.pub.move(self, route[1])
                self.pos = route[1]
        return True

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        return grab

    ##########################################################################
    def generate_demand(self, tick):
        """ Generate new demand for something """
        self.demands = {'time': tick, 'amount': random.randint(1, 3)}

# EOF