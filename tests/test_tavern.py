""" Test Tavern """

import unittest
import tavern.tavern as tavern


##############################################################################
class Test_Tavern(unittest.TestCase):
    """ Tavern """
    def setUp(self):
        self.tavern = tavern.Tavern()
        self.tavern.populate()

    def test_staff(self):
        """ Test staff provisioning """
        self.assertEqual(len(self.tavern.staff), self.tavern.num_staff)


##############################################################################
class Test_Stool(unittest.TestCase):
    """ Test populate """
    def setUp(self):
        self.tvn = tavern.Tavern(size_x=11, size_y=12, num_stools=1)
        self.tvn.populate()

    def test_populate(self):
        """ test stools creation """
        self.assertEqual(self.tvn.size_x, 11)
        self.assertEqual(self.tvn.size_y, 12)
        self.assertEqual(len(self.tvn.stools), 1)

    def test_locations(self):
        """ Test stool locations """
        stool = self.tvn.stools[0]
        loc = self.tvn.locations[stool.pos]
        self.assertEqual(loc.data['furniture'], stool)

# EOF
