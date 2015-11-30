from dragonfly.actions.action_function import Function

from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import S, L, R
from caster.lib.dfplus.state.stackitems import StackItemAsynchronous, \
    StackItemRegisteredAction
from caster.lib.tests.testutils import MockAlternative
from caster.lib.tests.unit.nexus import TestNexus


class TestState(TestNexus):
    
    def setUp(self):
        TestNexus.setUp(self)
    
    def test_blocking(self):
        '''make fake AsynchronousAction'''
        context_set = S(["cancel", "words"], NullAction())
        context_level = L(context_set)
        aa1 = AsynchronousAction([context_level], 
                                time_in_seconds=0.2, 
                                repetitions=20,
                                blocking=True) # turn blocking on
        aa1.set_nexus(self.nexus)
        '''make fake StackItemAsynchronous'''
        alt = MockAlternative(u"run", u"blocker")
        sia1 = StackItemAsynchronous(aa1, {"_node":alt})# the dictionary is fake Dragonfly data
        '''add it'''
        self.nexus.state.add(sia1)
        
        '''blocked function'''
        mutable_integer = {"value": 0}
        def increment():
            mutable_integer["value"]+=1
        for i in range(0, 3):
            '''make fake incrementing RegisteredAction'''
            inc = R(Function(increment), rspec="inc")
            inc.set_nexus(self.nexus)
            '''make fake StackItemRegisteredAction'''
            alt2 = MockAlternative(u"my", u"spoken", u"words")
            sira1 = StackItemRegisteredAction(inc, {"_node":alt2})
            '''add it'''
            self.nexus.state.add(sira1)
        '''incrementing should be blocked at this point'''
        self.assertEqual(mutable_integer["value"], 0)
        
        '''incrementing should happen that moment of unblocking'''
        self.nexus.state.terminate_asynchronous(True)
        self.assertEqual(mutable_integer["value"], 3)
