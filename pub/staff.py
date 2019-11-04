""" Staff member definition """
from person import Person


##############################################################################
class Staff(Person):
    """ Staff member - satisfies customer requirements """
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.supplies = []
        self.repr = 'B'

# EOF
