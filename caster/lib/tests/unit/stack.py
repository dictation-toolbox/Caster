from dragonfly.actions.action_function import Function
from dragonfly.actions.action_text import Text

from caster.lib import utilities
from caster.lib.dfplus.state.actions import AsynchronousAction, ContextSeeker, \
    RegisteredAction
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.dfplus.state.stackitems import StackItemAsynchronous, \
    StackItemRegisteredAction, StackItemSeeker
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
    
    def test_list_pruning(self):
        '''make fake RegisteredAction'''
        action = R(NullAction(), rspec="test")
        action.set_nexus(self.nexus)
        
        
        for i in range(0, self.nexus.state.stack.max_list_size+5):
            '''make fake StackItemRegisteredAction'''
            alt = MockAlternative(u"my", u"spoken", u"words")
            sira1 = StackItemRegisteredAction(action, {"_node":alt})
            '''add it'''
            self.nexus.state.add(sira1)
        
        self.assertEqual(len(self.nexus.state.stack.list), self.nexus.state.stack.max_list_size)
        
    def test_preserving_spoken_words(self):
        '''make fake RegisteredAction'''
        action = R(NullAction(), rspec="test")
        action.set_nexus(self.nexus)
        '''make fake StackItemRegisteredAction'''
        spoken=[u"my", u"spoken", u"words"]
        alt = MockAlternative(*spoken)
        sira1 = StackItemRegisteredAction(action, {"_node":alt})
        '''add it'''
        self.nexus.state.add(sira1)
        
        last_item = self.nexus.state.stack.list[len(self.nexus.state.stack.list)-1]
        self.assertEqual(spoken, last_item.get_preserved())
    
    def test_seeker_forward(self):
        mutable_string = {"value": ""}
        def append_a():
            mutable_string["value"] += "a"
        def append_b():
            mutable_string["value"] += "b"
        def append_c():
            mutable_string["value"] += "c"
        def append_d():
            mutable_string["value"] += "d"
        
        '''create context levels'''
        set_1_1 = S(["arch"], append_a)
        set_1_2 = S(["bell"], append_b)
        level_1 = L(set_1_1, set_1_2)
        set_2_1 = S(["cellar"], append_c)
        set_2_2 = S(["door"], append_d)
        level_2 = L(set_2_1, set_2_2)
        
        '''create context seeker'''
        levels = [level_1, level_2]
        seeker = ContextSeeker(forward=levels)
        seeker.set_nexus(self.nexus)
        
        '''create context seeker stack item'''
        alt = MockAlternative(u"my", u"spoken", u"words")
        stack_seeker = StackItemSeeker(seeker, {"_node":alt})
        '''add it'''
        self.nexus.state.add(stack_seeker)
        
        '''make 2 fake triggering RegisteredActions'''
        trigger1 = NullAction(rspec="bell")
        trigger2 = NullAction(rspec="cellar")
        trigger1.set_nexus(self.nexus)
        trigger2.set_nexus(self.nexus)
        '''make fake StackItemRegisteredActions'''
        alt2 = MockAlternative(u"my", u"spoken", u"words")
        sira1 = StackItemRegisteredAction(trigger1, {"_node":alt2})
        sira2 = StackItemRegisteredAction(trigger2, {"_node":alt2})
        '''add them'''
        self.nexus.state.add(sira1)
        self.nexus.state.add(sira2)
        
        self.assertEqual(mutable_string["value"], "bc")
#     def test_clean_items(self):
    def test_seeker_consume(self):
        '''seeker actions have the option to not/consume their triggers;
        that is, the trigger actions do not execute and only act as triggers'''
        
        mutable_string = {"value": ""}
        def append_a():
            mutable_string["value"] += "a"
        def append_b():
            mutable_string["value"] += "b"
        def append_c():
            mutable_string["value"] += "c"
        def append_d():
            mutable_string["value"] += "d"
        def append_e():
            mutable_string["value"] += "e"
        def append_f():
            mutable_string["value"] += "f"
        
        '''create context levels'''
        set_1_1 = S(["arch"], append_a)
        set_1_2 = S(["bell"], append_b)
        set_1_2.consume = False
        level_1 = L(set_1_1, set_1_2)
        set_2_1 = S(["cellar"], append_c)
        set_2_2 = S(["door"], append_d)
        level_2 = L(set_2_1, set_2_2)
        set_3_1 = S(["echo"], append_e)
        set_3_2 = S(["frame"], append_f)
        set_3_2.consume = False
        level_3 = L(set_3_1, set_3_2)
        
        '''create context seeker'''
        levels = [level_1, level_2, level_3]
        seeker = ContextSeeker(forward=levels)
        seeker.set_nexus(self.nexus)
        
        '''create context seeker stack item'''
        alt = MockAlternative(u"my", u"spoken", u"words")
        stack_seeker = StackItemSeeker(seeker, {"_node":alt})
        '''add it'''
        self.nexus.state.add(stack_seeker)
        
        '''make 3 fake triggering RegisteredActions;
        the first and third do not consume their triggers'''
        trigger1 = RegisteredAction(Function(append_a), rspec="bell")
        trigger2 = RegisteredAction(Function(append_c), rspec="door")
        trigger3 = RegisteredAction(Function(append_e), rspec="frame")
        trigger1.set_nexus(self.nexus)
        trigger2.set_nexus(self.nexus)
        trigger3.set_nexus(self.nexus)
        '''make fake StackItemRegisteredActions'''
        alt2 = MockAlternative(u"my", u"spoken", u"words")
        sira1 = StackItemRegisteredAction(trigger1, {"_node":alt2})
        sira2 = StackItemRegisteredAction(trigger2, {"_node":alt2})
        sira3 = StackItemRegisteredAction(trigger3, {"_node":alt2})
        '''add them'''
        self.nexus.state.add(sira1)
        self.nexus.state.add(sira2)
        self.nexus.state.add(sira3)
        
        self.assertEqual(mutable_string["value"], "aebdf")
    
    def test_seeker_backward(self):
        for i in range(0, 2):
            '''make 2 fake NullActions'''
            trigger1 = NullAction(rspec="bell")
            trigger2 = NullAction(rspec="door")
            trigger1.set_nexus(self.nexus)
            trigger2.set_nexus(self.nexus)
            '''make fake StackItemRegisteredActions'''
            alt2 = MockAlternative(u"my", u"spoken", u"words")
            sira1 = StackItemRegisteredAction(trigger1, {"_node":alt2})
            sira2 = StackItemRegisteredAction(trigger2, {"_node":alt2})
            '''add them'''
            self.nexus.state.add(sira1)
            self.nexus.state.add(sira2)
            
            '''set up backward looking seeker'''
            mutable_string = {"value": ""}
            def append_a():
                mutable_string["value"] += "a"
            def append_b():
                mutable_string["value"] += "b"
            def append_c():
                mutable_string["value"] += "c"
            def append_d():
                mutable_string["value"] += "d"
            
            '''create context levels'''
            set_1_1 = S(["arch"], append_a)
            set_1_2 = S(["bell"], append_b)
            level_1 = L(set_1_1, set_1_2)
            set_2_1 = S(["cellar"], append_c)
            set_2_2 = S(["door"], append_d)
            level_2 = L(set_2_1, set_2_2)
            
            '''create context seeker'''
            levels = [level_1, level_2]
            seeker = ContextSeeker(back=levels)
            if i==0:
                seeker.reverse = True
            seeker.set_nexus(self.nexus)
            
            '''create context seeker stack item'''
            alt = MockAlternative(u"my", u"spoken", u"words")
            stack_seeker = StackItemSeeker(seeker, {"_node":alt})
            '''add it'''
            self.nexus.state.add(stack_seeker)
            
            if i==0:
                self.assertEqual(mutable_string["value"], "db")
            else:
                self.assertEqual(mutable_string["value"], "bd")
    
    def test_actions_cleaned(self):
        '''these test functions should stay in sync with the clean methods for each stack action'''
        def registered_is_clean(r):
            return r.dragonfly_data is None and r.base is None
        def seeker_is_clean(s):
            result = True
            levels = []
            if s.back is not None: levels += s.back
            if s.forward is not None: levels += s.forward
            for context_level in levels:
                result &= context_level.dragonfly_data is None
            return result
        def asynchronous_is_clean(a):
            return a.closure is None
        
        '''mock words being the same doesn't matter for this test, or most tests'''
        alt = MockAlternative(u"my", u"spoken", u"words")
        
        '''make fake NullActions'''
        action1 = NullAction(rspec="barkley")
        action2 = NullAction(rspec="gaiden")
        action3 = NullAction(rspec="is")
        action4 = NullAction(rspec="awesome")
        action1.set_nexus(self.nexus)
        action2.set_nexus(self.nexus)
        action3.set_nexus(self.nexus)
        action4.set_nexus(self.nexus)
        '''make fake StackItemRegisteredActions'''
        sira1 = StackItemRegisteredAction(action1, {"_node":alt})
        sira2 = StackItemRegisteredAction(action2, {"_node":alt})
        sira3 = StackItemRegisteredAction(action3, {"_node":alt})
        sira4 = StackItemRegisteredAction(action4, {"_node":alt})
        
        '''should not be clean before it's executed'''
        self.assertFalse(registered_is_clean(sira1))
        
        '''add first one for backward seeker'''
        self.nexus.state.add(sira1)
        
        '''should be clean as soon as it's executed'''
        self.assertTrue(registered_is_clean(sira1))
        
        '''make backward seeker'''
        back_seeker = ContextSeeker(back=[L(S(["minecraft"], Function(lambda: None)))])
        back_seeker.set_nexus(self.nexus)
        '''create backward seeker stack item'''
        stack_seeker = StackItemSeeker(back_seeker, {"_node":alt})
        '''add it'''
        self.nexus.state.add(stack_seeker)
        
        '''levels should be clean as soon as it's executed'''
        self.assertTrue(registered_is_clean(stack_seeker) and seeker_is_clean(stack_seeker))
        
        #
        
        '''make forward seeker'''
        forward_seeker = ContextSeeker(forward=[L(S(["cave"], Function(lambda: None))), 
                                                L(S(["story"], Function(lambda: None)))])
        forward_seeker.set_nexus(self.nexus)
        '''create context seeker stack item'''
        stack_seeker2 = StackItemSeeker(forward_seeker, {"_node":alt})
        '''add it'''
        self.nexus.state.add(stack_seeker2)
    
        self.nexus.state.add(sira2)
        '''levels should not be clean before seeker is executed'''
        self.assertFalse(registered_is_clean(stack_seeker2) or seeker_is_clean(stack_seeker2))

        self.nexus.state.add(sira3)
        '''levels should be clean as soon as it's executed'''
        self.assertTrue(registered_is_clean(stack_seeker2) and seeker_is_clean(stack_seeker2))
        
        #
        
        '''make asynchronous action'''
        asynchronous = AsynchronousAction([L(S(["eternal", "daughter", "awesome"], lambda: None))], 
                                          blocking=False)
        asynchronous.set_nexus(self.nexus)
        '''make StackItemAsynchronous'''
        sia1 = StackItemAsynchronous(asynchronous, {"_node":alt})
        '''add it'''
        self.nexus.state.add(sia1)
        
        '''closure should not be clean before asynchronous is executed'''
        self.assertFalse(registered_is_clean(sia1) or seeker_is_clean(sia1) or asynchronous_is_clean(sia1))
        
        self.nexus.state.add(sira4)
        
        '''closure should be clean after asynchronous is executed'''
        self.assertTrue(registered_is_clean(sia1) and seeker_is_clean(sia1) and asynchronous_is_clean(sia1))











        
        
        
        
        
        
        
        
        
        
        
        
