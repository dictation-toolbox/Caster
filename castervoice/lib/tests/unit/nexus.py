import unittest

from castervoice.lib.ctrl.nexus import Nexus


class TestNexus(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.nexus = Nexus(False)
