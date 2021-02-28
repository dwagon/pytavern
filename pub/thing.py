""" Generic Base Class for something that exists in space and time """


##############################################################################
class Thing:
    """ Define a thing """
    def __init__(self, pub, name, pos):
        self.pub = pub
        self.name = name
        self.pos = pos
        self.permeable = False

    ##########################################################################
    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} @ {self.pos}"

# EOF
