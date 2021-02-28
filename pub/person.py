""" Definition of Person base class """
from thing import Thing

UNKNOWN = -1
CUST_GO_CHAIR = 0
CUST_WAIT_TO_ORDER = 1
CUST_WAIT_TO_DRINK = 2
CUST_DRINK = 3
CUST_GO_HOME = 4

SERV_WAIT = 10
SERV_GET_ORDER = 11
SERV_GET_SUPPLIES = 12
SERV_SERVE_SUPPLIES = 13


##############################################################################
class Person(Thing):
    """ Definition of a Person - mobile Thing """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.repr = '?'
        self.mode = UNKNOWN

    def move(self, newloc):
        """ Move to newloc """
        self.pub.move(self, newloc)
        self.pos = newloc

# EOF
