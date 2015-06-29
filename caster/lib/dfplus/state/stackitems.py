'''
Created on Jun 7, 2015

@author: dave
'''
from dragonfly import Function, Key, Mimic, Paste, Text

from caster.lib import control, settings
from caster.lib.dfplus.hint.hintnode import NodeAction

class StackItem:
    def __init__(self, type):
        assert type in ["raction", "seeker", "continuer"]
        self.type = type
        self.complete = False  # indicates whether it has been run already
        self.consumed = False  # indicates that an undo is unnecessary
        self.rspec = "default"
    def put_time_action(self):
        ''' this always happens at the time that the Stack item is placed in the Stack '''
class StackItemRegisteredAction(StackItem):
    def __init__(self, registered_action, type="raction"):
        StackItem.__init__(self, type)
        self.dragonfly_data = registered_action.dragonfly_data
        self.base = registered_action.base
        self.rspec = registered_action.rspec
        self.rdescript = registered_action.rdescript
        self.rundo = registered_action.rundo
        self.show = registered_action.show
        self.preserved = []
    def execute(self):
        self.complete = True
        self.base._execute(self.dragonfly_data)
        # do presentation here
        self.clean()
    def clean(self):
        self.dragonfly_data = None
    def preserve(self):# save spoken words
        if self.dragonfly_data!=None:
            self.preserved = [x[0] for x  in self.dragonfly_data["_node"].results]
    def put_time_action(self):
        self.preserve()
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"] and self.show:
            control.nexus().intermediary.text(self.rdescript)
class StackItemSeeker(StackItemRegisteredAction):
    def __init__(self, seeker):
        StackItemRegisteredAction.__init__(self, seeker, "seeker")
        self.back = self.copy_direction(seeker.back)
        self.forward = self.copy_direction(seeker.forward)
        self.rspec = seeker.rspec
        self.use_spoken = seeker.use_spoken
        self.spoken = {}
    
    @staticmethod
    def copy_direction(cls):
        result = None
        if cls != None:
            result = []
            for i in range(0, len(cls)):
                cl = cls[i].copy()
                cl.number(i)
                result.append(cl)
        return result
    def executeCL(self, cl):# the return value is whether to terminate a continuer
        action = cl.result
        level = cl.index
        fnparams = cl.parameters
        if self.use_spoken:
            fnparams = self.spoken[level]
        if not action in [Text, Key, Mimic, Function, Paste, NodeAction]:
            # it's a function object
            if fnparams == None:
                return action()
            else:
                return action(fnparams)
        else:
            # it's a dragonfly action, and the parameters are the spec
            action(cl.parameters)._execute(cl.dragonfly_data)
            return False
    def eat(self, level, stack_item):
        self.spoken[level] = stack_item.preserved
    def clean(self):
        # save whatever data you need here
        StackItemRegisteredAction.clean(self)
        if self.back != None: 
            for cl in self.back:
                cl.dragonfly_data = None
        if self.forward != None: 
            for cl in self.forward:
                cl.dragonfly_data = None
    def fillCL(self, cl, cs):
        cl.result = cs.f
        cl.parameters = cs.parameters
        cl.dragonfly_data = self.dragonfly_data
        cl.consume = cs.consume
#         self.dragonfly_data = None # no need to be hanging onto this in more places than one
    def execute(self, unused=None):
        self.complete = True
        c = []
        if self.back != None:c += self.back
        if self.forward != None:c += self.forward
        for cl in c:
            self.executeCL(cl)
        self.clean()
    def satisfy_level(self, level_index, is_back, stack_item):
        direction = self.back if is_back else self.forward
        cl = direction[level_index]
        if not cl.satisfied:
            if stack_item != None:
                for cs in cl.sets:
                    # stack_item must have a spec
                    if stack_item.rspec in cs.specTriggers:
                        cl.satisfied = True
                        self.fillCL(cl, cs)
                        break
            if not cl.satisfied:  # if still not satisfied, do default
                cl.satisfied = True
                self.fillCL(cl, cl.sets[0])
    def get_index_of_next_unsatisfied_level(self):
        for i in range(0, len(self.forward)):
            cl = self.forward[i]
            if not cl.satisfied:
                return i
        return -1
class StackItemAsynchronous(StackItemSeeker):
    def __init__(self, continuer):
        StackItemRegisteredAction.__init__(self, continuer, "continuer")
        self.back = None
        self.forward = self.copy_direction(continuer.forward)
        self.repetitions = continuer.repetitions
        self.fillCL(self.forward[0], self.forward[0].sets[0])
        self.closure = None
        self.time_in_seconds = continuer.time_in_seconds
        self.blocking = continuer.blocking
        self.use_spoken = False
        self.spoken = {}
    def satisfy_level(self, level_index, is_back, Stack_item):  # level_index and is_back are unused here, but left in for compatibility
        cl = self.forward[0]
        if not cl.satisfied:
            if Stack_item != None:
                cs = cl.sets[0]
                if Stack_item.rspec in cs.specTriggers:  # Stack_item must have a spec
                    cl.satisfied = True
    def get_triggers(self):
        return self.forward[0].sets[0].specTriggers
    def execute(self, success):  # this method should be what deactivates the continuer
        '''
        There are three ways this can be triggered: success, timeout, and cancel.
        Success and timeout are in the closure. Cancels are handled in the Stack.
        Waiting commands should only be run on success.
        '''
        self.complete = True
        control.nexus().timer.remove_callback(self.closure)
        StackItemSeeker.clean(self)
        self.closure = None
        if success:
            control.nexus().state.run_waiting_commands()  # @UndefinedVariable
        else:
            control.nexus().state.unblock()  # @UndefinedVariable
    def begin(self):
        '''here pass along a closure to the timer multiplexer'''
        eCL = self.executeCL
        cl = self.forward[0]
        r = self.repetitions
        c = {"value":0}  # count
        e = self.execute
        def closure():
            terminate = eCL(cl)
            if terminate:
                e(terminate)
                
            elif r != 0:  # if not run forever
                c["value"] += 1
                if c["value"] == r:
                    e(False)
        self.closure = closure
        control.nexus().timer.add_callback(self.closure, self.time_in_seconds)
        self.closure()