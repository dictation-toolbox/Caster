from caster.lib.tests.unit.nexus import TestNexus
from caster.lib.dfplus.state.stack import CasterState


class TestState(TestNexus):
    
    def setUp(self):
        TestNexus.setUp(self)
        self.nexus.inform_state(CasterState(self.nexus))