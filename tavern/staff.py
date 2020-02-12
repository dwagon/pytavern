""" Staff member definition """
from .person import Person


##############################################################################
class Staff(Person):
    """ Staff member - satisfies customer requirements """
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.supplies = 0
        self.repr = 'B'

    ##########################################################################
    def turn(self):
        """ Time passing """
        return self.move(self.pick_target, self.serve)

    ##########################################################################
    def serve(self):
        """ Transact with suppliers / consumers """
        if hasattr(self.target, 'take'):
            take = self.target.take(5)
            self.supplies += take
            if take == 0:
                return False
            print(f"{self.name} took {take} supplies from {self.target.name}")
        if hasattr(self.target, 'receive'):
            receive = self.target.receive(self.supplies)
            self.supplies -= receive
            print(f"{self.name} gave {receive} supplies to {self.target.name}")
        self.target = None
        return True

    ##########################################################################
    def pick_target(self):
        """ Pick where to go next """
        if not self.supplies:
            min_dist = 99999
            target = None
            for i in self.tavern.supplies:
                if not i.amount:
                    continue
                path = self.tavern.find_route(self, i)
                distance = len(list(path))
                if min_dist > distance:
                    min_dist = distance
                    target = i
        else:
            target = None
            max_demand = 0
            max_cust = None
            for cust in self.tavern.customers:
                dem = (self.tavern.time - cust.demands['time']) * cust.demands['amount']
                if dem > max_demand:
                    max_demand = dem
                    max_cust = cust
            if max_demand:
                target = max_cust
        return target


# EOF
