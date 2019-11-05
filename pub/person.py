""" Definition of Person base class """
from thing import Thing


##############################################################################
class Person(Thing):
    """ Definition of a Person - mobile Thing """
    def __init__(self, pub, name, x, y):
        super().__init__(pub, name, x, y)

# EOF
