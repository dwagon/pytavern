""" Customer """
import random

from coord import Coord
from person import Person


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, x, y):
        super().__init__(pub, name, x, y)
        self.demands = {}
        self.satisfaction = 9
        self.target = None
        self.repr = 'C'

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if not self.demands.get('amount', 0):
            self.generate_demand(tick)
            self.satisfaction -= 1
        if not self.satisfaction:
            self.target = Coord(0, 0)
            print(f"{self} had enough")
        if self.target:
            route = list(self.pub.find_route(self, self.target))
            if len(route) <= 1:
                return False
            self.pub.move(self, route[1])
            self.x, self.y = route[1]
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
