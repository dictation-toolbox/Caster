import unittest

from caster.lib.ctrl.nexus import Nexus


class TestNexus(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.nexus = Nexus()
        self.nexus.merger.use_real_config = False