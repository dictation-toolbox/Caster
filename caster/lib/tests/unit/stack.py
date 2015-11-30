from dragonfly.actions.action_text import Text

from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.dfplus.state.stackitems import StackItemAsynchronous, \
    StackItemRegisteredAction
from caster.lib.tests.testutils import MockAlternative
from caster.lib.tests.unit.nexus import TestNexus


class TestStack(TestNexus):
    
    def setUp(self):
        TestNexus.setUp(self)
    
    def test_cancel(self):
        mutable_integer = {"value": 0}
        def increment():
            mutable_integer["value"]+=1
        
        '''make fake AsynchronousAction'''
        context_set = S(["test", "words"], increment)
        unused_context_set = S(["other"], Text, "words")
        context_level = L(context_set, unused_context_set)
        aa1 = AsynchronousAction([context_level], 
                                time_in_seconds=0.2, 
                                repetitions=20,
                                blocking=False)
        aa1.set_nexus(self.nexus)
        
        '''make fake StackItemAsynchronous'''
        alt = MockAlternative(u"gray", u"fox")
        sia1 = StackItemAsynchronous(aa1, {"_node":alt})# the dictionary is fake Dragonfly data
        '''add it'''
        self.nexus.state.add(sia1)
        
        '''make fake canceling RegisteredAction'''
        cancel = R(NullAction(), rspec="test")
        cancel.set_nexus(self.nexus)
        '''make fake StackItemRegisteredAction'''
        alt2 = MockAlternative(u"my", u"spoken", u"words")
        sira1 = StackItemRegisteredAction(cancel, {"_node":alt2})
        '''add it'''
        self.nexus.state.add(sira1)
        
        '''AsynchronousAction should have executed exactly once, 
        when it was added, then immediately gotten canceled'''
        self.assertEqual(mutable_integer["value"], 1)