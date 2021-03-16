""" Customer """
import random

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
        self.mode = person.CUST_WAIT_FOR_CHAIR

    ##########################################################################
    def order(self):
        """ Deliver order to staff """
        self.mode = person.CUST_WAIT_TO_DRINK
        return self.demands['amount']

    ##########################################################################
    def go_to_chair(self):
        """ Find a chair to sit down at """
        if not self.move():
            self.mode = person.CUST_WAIT_TO_ORDER
            self.chair = self.target_chair
            self.pos = self.target_chair.pos
            self.chair.sit_down(self)
            print(f"{self} sat down in {self.chair}")
            self.target = None

    ##########################################################################
    def wait_for_chair(self):
        """ Move somewhere and wait for a chair to be free """
        self.target_chair = self.pub.find_empty_chair()
        if self.target_chair is None:
            if self.target is None:
                self.target = self.pub.map.free_people_loc()
                print(f"{self} Moving to {self.target} waiting for chair")
            self.move()
        else:
            self.target = self.target_chair.pos
            self.mode = person.CUST_GO_CHAIR

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if self.mode == person.CUST_GO_CHAIR:
            self.go_to_chair()
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            self.generate_demand(tick)
            pass
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            pass
        elif self.mode == person.CUST_DRINK:
            if not self.satisfaction:
                self.target = self.pub.door
                self.chair.get_up()
                print(f"{self} got up from {self.chair}")
                print(f"{self} had enough")
                self.mode = person.CUST_GO_HOME
            else:
                self.mode = person.CUST_WAIT_TO_ORDER
        elif self.mode == person.CUST_GO_HOME:
            if self.pos == self.pub.door.pos:
                return False
            self.move()
        elif self.mode == person.CUST_WAIT_FOR_CHAIR:
            self.wait_for_chair()
        return True

    ##########################################################################
    def generate_demand(self, tick):
        """ So thirsty ... """
        if not self.demands.get('amount', 0) and self.satisfaction:
            self.demands = {'time': tick, 'amount': random.randint(1, 3)}
            self.satisfaction -= 1

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        self.mode = person.CUST_DRINK
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        return grab

# EOF
