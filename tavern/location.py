""" Locations in a tavern """


##############################################################################
class Location:
    """ Class definition of a location """
    categories = ['undef', 'structure', 'installation', 'furniture', 'person']

    def __init__(self):
        self.data = {}

    def add(self, obj):
        """ Add an item to a location """
        self.data[obj.category] = obj

    def isempty(self, category='undef'):
        """ Return True if the location is empty """
        for cat in self.categories:
            if self.data.get(cat):
                if not self.data[cat].permeable:
                    return False
        return self.data.get(category) is None

    def delete(self, category='undef'):
        """ Remove the object from the location """
        self.data[category] = None

    def repr(self):
        """ Return the repr of the location """
        ch = '.'
        for cat in self.categories:
            if self.data.get(cat):
                ch = self.data[cat].repr
        return ch

    def __repr__(self):
        return f"Location {self.data}"

# EOF
