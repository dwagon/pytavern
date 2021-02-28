""" Customer """
import random

from coord import Coord
import person


##############################################################################
class Customer(person.Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.demands = {}
        self.satisfaction = 9
        self.target = None
        self.target_chair = None
        self.chair = None
        self.repr = 'C'
        self.mode = person.CUST_GO_CHAIR

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if self.mode == person.CUST_GO_CHAIR:
            self.target_chair = self.pub.find_empty_chair()
            self.target = self.target_chair.pos
            route = list(self.pub.find_route(self.pos, self.target))
            if len(route) <= 1:     # Arrived
                self.chair = self.target_chair
                self.pos = self.target_chair.pos
                self.chair.sit_down(self)
                self.mode = person.CUST_WAIT_TO_ORDER
                print(f"{self} sat down in {self.chair}")
                self.target = None
            else:
                print(f"{self} Steps={len(route)} {route=}")
                self.move(route[1])
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            pass
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            pass
        elif self.mode == person.CUST_DRINK:
            if not self.satisfaction:
                self.target = Coord(1, 1)
                self.chair.get_up()
                print(f"{self} got up from {self.chair}")
                print(f"{self} had enough")
                self.mode = person.CUST_GO_HOME
        elif self.mode == person.CUST_GO_HOME:
            route = list(self.pub.find_route(self.pos, Coord(1, 1)))
            self.move(route[1])

        # Thirsty
        if not self.demands.get('amount', 0):
            self.generate_demand(tick)
            self.satisfaction -= 1

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
