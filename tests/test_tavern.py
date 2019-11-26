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

# EOF
