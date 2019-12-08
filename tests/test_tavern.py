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


##############################################################################
class Test_Path(unittest.TestCase):
    """ Test path and movement """
    def setUp(self):
        self.tvn = tavern.Tavern(size_x=10, size_y=10, num_stools=1, max_customers=1, num_staff=0)
        self.tvn.populate()

    def test_path(self):
        """ Test that a customer gets to the stool """
        for _ in range(20):
            self.tvn.turn()
        cust = self.tvn.customers[0]
        stool = self.tvn.stools[0]
        self.assertEqual(cust.pos, stool.pos)


# EOF
