""" Staff member definition """
import random
import person


##############################################################################
class Staff(person.Person):
    """ Staff member - satisfies customer requirements """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.supplies = 0
        self.repr = 'B'
        self.target = None
        self.cust_serving = None
        self.cust_request = None
        self.mode = person.SERV_WAIT

    ##########################################################################
    def pick_waiting_customer(self):
        """ Pick a customer that is waiting to order """
        for cust in self.pub.customers:
            if cust.mode == person.CUST_WAIT_TO_ORDER:
                return cust
        return None

    ##########################################################################
    def pick_supplies(self):
        """ Pick which supplies to go to """
        return random.choice(self.pub.supplies)

    ##########################################################################
    def route(self, newmode):
        """ Route to the target - take on newmode if we reach
            Return True if moving, False if arrived
        """
        route = self.pub.find_route(self.pos, self.target, adjacent=True)
        if route is None:
            routelist = []
        else:
            routelist = list(route)
        if len(routelist) <= 1:
            self.mode = newmode
            return False
        self.move(routelist[1])
        return True

    ##########################################################################
    def turn(self, tick):   # pylint: disable=unused-argument
        """ Time passing """
        if self.mode == person.SERV_WAIT:
            cust = self.pick_waiting_customer()
            if cust:
                self.target = cust
                self.cust_serving = cust
                self.mode = person.SERV_GET_ORDER
            else:
                if self.target is None:
                    self.target = self.pub.free_location()
                self.route(person.SERV_WAIT)
            return True
        elif self.mode == person.SERV_GET_ORDER:
            if not self.route(person.SERV_GET_SUPPLIES):
                self.get_request(self.cust_serving)
                self.target = None
        elif self.mode == person.SERV_GET_SUPPLIES:
            if self.target is None:
                self.target = self.pick_supplies()
            if not self.route(person.SERV_SERVE_SUPPLIES):
                self.get_supplies()
        elif self.mode == person.SERV_SERVE_SUPPLIES:
            self.target = self.cust_serving
            if not self.route(person.SERV_WAIT):
                self.deliver_order()
        return True

    ##########################################################################
    def get_request(self, cust):
        """ Get the request from the customer """
        self.cust_request = cust.order()

    ##########################################################################
    def get_supplies(self):
        """ Get supplies """
        take = self.target.take(min(5, self.cust_request))
        self.supplies += take
        print(f"Took {take} supplies from {self.target.name}")

    ##########################################################################
    def deliver_order(self):
        """ Deliver order to customer """
        receive = self.target.receive(self.supplies)
        self.supplies -= receive
        print(f"Gave {receive} supplies to {self.target.name}")

# EOF
