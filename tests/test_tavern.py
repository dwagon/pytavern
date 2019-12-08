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
class Test_Populate(unittest.TestCase):
    """ Test populate """
    def test_stools(self):
        """ test stools creation """
        tvn = tavern.Tavern(size_x=11, size_y=12, num_stools=1)
        tvn.populate()
        self.assertEqual(tvn.size_x, 11)
        self.assertEqual(tvn.size_y, 12)
        self.assertEqual(len(tvn.stools), 1)

# EOF
