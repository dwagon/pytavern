""" Staff member definition """
import person


##############################################################################
class Staff(person.Person):
    """ Staff member - satisfies customer requirements """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.supplies = 0
        self.repr = 'B'
        self.target = None
        self.mode = person.SERV_WAIT

    ##########################################################################
    def pick_waiting_customer(self):
        """ Pick a customer that is waiting to order """
        for cust in self.pub.customers:
            if cust.mode == person.CUST_WAIT_TO_ORDER:
                return cust
        return None

    ##########################################################################
    def turn(self, tick):   # pylint: disable=unused-argument
        """ Time passing """
        if self.mode == person.SERV_WAIT:
            cust = self.pick_waiting_customer()
            if cust:
                self.target = cust
                self.mode = person.SERV_GET_ORDER
            else:
                print(f"{self} waiting to do something")
            return True
        elif self.mode == person.SERV_GET_ORDER:
            route = list(self.pub.find_route(self.pos, self.target, adjacent=True))
            assert route, f"{self} No route to {self.target}"
            if len(route) > 1:
                self.move(route[1])
            else:
                # TODO: get order from customer
                self.mode = person.SERV_GET_SUPPLIES
        elif self.mode == person.SERV_GET_SUPPLIES:
            pass
        elif self.mode == person.SERV_SERVE_SUPPLIES:
            pass
        return True

    ##########################################################################
    def serve(self):
        """ Transact with suppliers / consumers """
        if hasattr(self.target, 'take'):
            take = self.target.take(5)
            self.supplies += take
            if take == 0:
                return False
            print(f"Took {take} supplies from {self.target.name}")
        if hasattr(self.target, 'receive'):
            receive = self.target.receive(self.supplies)
            self.supplies -= receive
            print(f"Gave {receive} supplies to {self.target.name}")
        self.target = None
        return True

# EOF
