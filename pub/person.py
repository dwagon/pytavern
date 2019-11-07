""" Definition of Person base class """
from thing import Thing


##############################################################################
class Person(Thing):
    """ Definition of a Person - mobile Thing """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)

# EOF
