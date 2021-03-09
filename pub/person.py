""" Definition of Person base class """
from thing import Thing

UNKNOWN = -1
CUST_GO_CHAIR = 0
CUST_WAIT_TO_ORDER = 1
CUST_WAIT_TO_DRINK = 2
CUST_DRINK = 3
CUST_GO_HOME = 4
CUST_WAIT_FOR_CHAIR = 5

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
        self.target = None
        self.mode = UNKNOWN

    def move(self, adjacent=False):
        """ Route to the target
            Return True if still moving, False if arrived
        """
        route = self.pub.find_route(self.pos, self.target, adjacent=adjacent)
        if route is None:
            routelist = []
        else:
            routelist = list(route)
        # print(f"{self} {self.pos=} {self.target=} {len(routelist)=}")      # DBG

        if len(routelist) <= 1:
            return False
        self.pub.move(self, routelist[1])
        self.pos = routelist[1]
        return True

# EOF
