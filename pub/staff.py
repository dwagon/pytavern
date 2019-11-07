""" Staff member definition """
from person import Person


##############################################################################
class Staff(Person):
    """ Staff member - satisfies customer requirements """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.supplies = 0
        self.repr = 'B'
        self.target = None

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if self.target is None:
            self.target = self.pick_target(tick)
            if self.target is None:
                return False
            print(f"Going to {self.target.name}")
        route = list(self.pub.find_route(self, self.target))
        if len(route) <= 1:
            return self.serve()
        else:
            self.pub.move(self, route[1])
            self.pos = route[1]
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

    ##########################################################################
    def pick_target(self, tick):
        """ Pick where to go next """
        if not self.supplies:
            min_dist = 99999
            target = None
            for i in self.pub.supplies:
                if not i.amount:
                    continue
                path = self.pub.find_route(self, i)
                distance = len(list(path))
                if min_dist > distance:
                    min_dist = distance
                    target = i
        else:
            max_demand = 0
            max_cust = None
            for cust in self.pub.customers:
                dem = (tick - cust.demands['time']) * cust.demands['amount']
                print(f"{cust.name} has demand {dem}")
                if dem > max_demand:
                    max_demand = dem
                    max_cust = cust
            target = max_cust
        return target


# EOF
