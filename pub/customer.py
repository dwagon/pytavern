""" Customer """
from person import Person


##############################################################################
class Customer(Person):
    """ Customer - resource consumer """
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.demands = []
        self.repr = 'C'

# EOF
