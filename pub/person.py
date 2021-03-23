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
        self.target = None
        self.mode = UNKNOWN
        self.blocked = 0

    ##########################################################################
    def repr(self):
        """ Repr """
        return '?'

    ##########################################################################
    def desc_line(self):
        """ Return a line describing the person, activities and status """
        raise NotImplementedError

    ##########################################################################
    def move(self, adjacent=False):
        """ Route to the target
            Return True if still moving, False if arrived
        """
        assert self.target is not None
        route = self.pub.find_route(self.pos, self.target, adjacent=adjacent)
        if route is None:
            routelist = []
        else:
            routelist = list(route)
        # print(f"{self} {self.pos=} {self.target=} {len(routelist)=}")      # DBG

        if hasattr(self.target, 'pos'):
            if self.pos == self.target.pos:
                return False
        else:
            if self.pos == self.target:
                return False
        if len(routelist) == 1 and adjacent:
            return False

        if not routelist:
            # print(f"{self} Failed to route {self.pos=} {self.target=} {adjacent=}")    # DBG
            self.blocked += 1
            return True
        self.blocked = 0
        self.pub.move(self, routelist[1])
        self.pos = routelist[1]
        return True

# EOF
