""" Staff member definition """
import random
import person

# Random
# Min: 3
# Avg: 85.41666666666667
# Max: 407


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
    def random_pick_waiting_customer(self):
        """ Pick a customer at random that is waiting to order """
        custs = self.pub.customers[:]
        random.shuffle(custs)
        for cust in custs:
            if cust.mode == person.CUST_WAIT_TO_ORDER:
                return cust
        return None

    ##########################################################################
    def pick_waiting_customer(self):
        """ Pick the customer that had been waiting the longest """
        max_demand = 9999999
        neediest_customer = None
        for cust in self.pub.customers:
            if cust.mode != person.CUST_WAIT_TO_ORDER:
                continue
            if cust.demands['amount'] and cust.demands['time'] < max_demand:
                max_demand = cust.demands['time']
                neediest_customer = cust
        return neediest_customer

    ##########################################################################
    def pick_supplies(self):
        """ Pick which supplies to go to """
        return random.choice(self.pub.supplies)

    ##########################################################################
    def get_order(self):
        """ Get the order from the customer """
        try:
            if not self.move(adjacent=True):
                self.mode = person.SERV_GET_SUPPLIES
                self.get_request(self.cust_serving)
                self.target = None
        except AttributeError:
            print("f{self=} {self.target=}")
            raise

    ##########################################################################
    def wait_for_customer(self):
        """ Wait for a customer to serve """
        cust = self.pick_waiting_customer()
        if cust:
            self.target = cust
            self.cust_serving = cust
            self.mode = person.SERV_GET_ORDER
        else:
            if self.target is None:
                self.target = self.pub.map.free_people_loc()
            if not self.move(adjacent=True):
                self.mode = person.SERV_WAIT

    ##########################################################################
    def turn(self, tick):   # pylint: disable=unused-argument
        """ Time passing """
        if self.mode == person.SERV_WAIT:
            self.wait_for_customer()
        elif self.mode == person.SERV_GET_ORDER:
            self.get_order()
        elif self.mode == person.SERV_GET_SUPPLIES:
            if self.target is None:
                self.target = self.pick_supplies()
            if not self.move():
                self.mode = person.SERV_SERVE_SUPPLIES
                self.get_supplies()
        elif self.mode == person.SERV_SERVE_SUPPLIES:
            self.target = self.cust_serving
            if not self.move(adjacent=True):
                self.mode = person.SERV_WAIT
                self.deliver_order()

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
