""" Customer """
import random

from .person import Person

GO_STOOL = 1
GO_HOME = 2
DRINK = 3


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.demands = {'amount': 0, 'time': 0}
        self.satisfaction = random.randint(1, 9)
        self.target = None
        self.repr = 'C'
        self.mode = GO_STOOL
        self.target_stool = None
        self.terminate = False

    ##########################################################################
    def turn(self):
        """ Time passing """
        return self.move(self.pick_target, self.got_there)

    ##########################################################################
    def description(self):
        """ Return a descripton of what the customer is doing """
        d = f" {self.name}@{self.pos}"
        if self.mode == DRINK:
            d += " sitting"
        else:
            d += f" -> {self.target}"
        if self.demands['amount']:
            d += f" Demands: {self.demands['amount']}"
        if self.satisfaction:
            d += f" Drink to go: {self.satisfaction}"
        d += f" {self.mode}"
        return d

    ##########################################################################
    def got_there(self):
        """ Got to where we want to go """
        if self.mode == GO_STOOL:
            if not self.target_stool.occupied:
                self.mode = DRINK
                self.tavern.move(self, self.target_stool.pos)
                self.target_stool.occupied = True
                self.generate_demand()
                print(f"{self} sat on {self.target_stool}")
            else:
                target = self.pick_stool()
                self.target_stool = target
        elif self.mode == GO_HOME:
            self.terminate = True
        return True

    ##########################################################################
    def pick_stool(self):
        """ Pick a stool to aim for """
        random.shuffle(self.tavern.stools)
        target = None
        for stl in self.tavern.stools:
            if not stl.occupied:
                target = stl
                break
        return target

    ##########################################################################
    def pick_target(self):
        """ Pick where to go based on mode """
        target = None
        # Still Thirsty
        if self.mode == DRINK:
            return None
        # Satisfied
        elif self.mode == GO_HOME:
            target = self.tavern.door
        # Just arrived
        elif self.mode == GO_STOOL:
            if self.target_stool is None:
                target = self.pick_stool()
                self.target_stool = target
                if target is None:
                    print("All stools are occupied")
                    self.target = self.tavern.free_location('person')
            else:
                target = self.target_stool
        else:
            print(f"Unknown mode {self.mode}")
        return target

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        if self.demands['amount'] <= 0:
            self.demands['amount'] = 0
            self.satisfaction -= 1
            if self.satisfaction <= 0:
                print(f"{self} had enough")
                for stl in self.tavern.stools:
                    if stl.pos == self.pos:
                        stl.occupied = False
                self.mode = GO_HOME
            else:
                self.generate_demand()
        return grab

    ##########################################################################
    def generate_demand(self):
        """ Generate new demand for something """
        self.demands = {'time': self.tavern.time, 'amount': random.randint(1, 3)}

# EOF
