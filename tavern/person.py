""" Definition of Person base class """
from .thing import Thing


##############################################################################
class Person(Thing):
    """ Definition of a Person - mobile Thing """
    def __init__(self, tavern, name, pos):
        super().__init__(tavern, name, pos)
        self.target = None
        self.category = 'person'

    ##########################################################################
    def move(self, pick_target=None, got_there=None):
        """ Move Person """
        # Decide where to go
        if self.target is None and pick_target:
            self.target = pick_target()
            if self.target is None:
                return False
        # Go there
        route = list(self.tavern.find_route(self.pos, self.target))
        if len(route) <= 1:
            ans = got_there()
        else:
            self.tavern.move(self, route[1])
            self.pos = route[1]
            ans = True
        return ans

# EOF
