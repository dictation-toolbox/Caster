import unittest

from dragonfly.actions.action_function import Function
from castervoice.lib.dfplus.state.actions import AsynchronousAction
from castervoice.lib.dfplus.state.actions2 import NullAction
from castervoice.lib.dfplus.state.short import S, L, R
from castervoice.lib.dfplus.state.stackitems import StackItemAsynchronous, \
    StackItemRegisteredAction
from castervoice.lib.tests.testutils import MockAlternative
from castervoice.lib.tests.unit.nexus import TestNexus


class TestState(TestNexus):

    def setUp(self):
        TestNexus.setUp(self)

    def test_blocking(self):
        '''
        Tests:
        1 - successful termination (queued actions execute immediately)
        2 - unsuccessful termination (queued actions are dropped)
        3 - cancellation (queued actions are dropped)
        '''

        for i in range(0, 3):
            '''make fake AsynchronousAction'''
            context_set = S(["cancel", "words"], NullAction())
            context_level = L(context_set)
            aa1 = AsynchronousAction([context_level], blocking=True)  # turn blocking on
            aa1.set_nexus(self.nexus)
            '''make fake StackItemAsynchronous'''
            alt = MockAlternative(u"run", u"blocker")
            sia1 = StackItemAsynchronous(
                aa1, {"_node": alt})  # the dictionary is fake Dragonfly data
            '''add it'''
            self.nexus.state.add(sia1)
            '''blocked function'''
            mutable_integer = {"value": 0}

            def increment():
                mutable_integer["value"] += 1

            '''make fake incrementing RegisteredAction'''
            inc = R(Function(increment), rspec="inc")
            inc.set_nexus(self.nexus)
            '''make fake StackItemRegisteredAction'''
            alt2 = MockAlternative(u"my", u"spoken", u"words")
            sira1 = StackItemRegisteredAction(inc, {"_node": alt2})
            '''add it'''
            self.nexus.state.add(sira1)
            '''incrementing should be blocked at this point'''
            self.assertEqual(mutable_integer["value"], 0)

            if i == 0:
                '''incrementing should happen that moment of unblocking'''
                self.nexus.state.terminate_asynchronous(True)
                self.assertEqual(mutable_integer["value"], 1)
            elif i == 1:
                '''incrementing gets dropped'''
                self.nexus.state.terminate_asynchronous(False)
                self.assertEqual(mutable_integer["value"], 0)
            elif i == 2:
                '''make fake canceling RegisteredAction'''
                cancel = NullAction(rspec="cancel")
                cancel.set_nexus(self.nexus)
                '''make fake StackItemRegisteredAction'''
                alt3 = MockAlternative(u"my", u"cancel", u"words")
                sira2 = StackItemRegisteredAction(cancel, {"_node": alt3})
                '''add it'''
                self.nexus.state.add(sira2)
                '''incrementing gets dropped'''
                self.assertEqual(mutable_integer["value"], 0)

if __name__ == '__main__':
    unittest.main()
