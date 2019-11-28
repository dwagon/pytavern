""" Generic Base Class for something that exists in space and time """


##############################################################################
class Thing:
    """ Define a thing """
    def __init__(self, tavern, name, pos):
        self.tavern = tavern
        self.name = name
        self.pos = pos
        self.category = 'undef'

    ##########################################################################
    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} @ {self.pos}"

    ##########################################################################
    def turn(self):
        """ Time passing """
        pass

# EOF
