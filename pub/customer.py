""" Customer """
import random

from person import Person


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, x, y):
        super().__init__(pub, name, x, y)
        self.demands = {}
        self.repr = 'C'

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if not self.demands.get('amount', 0):
            self.generate_demand(tick)

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
