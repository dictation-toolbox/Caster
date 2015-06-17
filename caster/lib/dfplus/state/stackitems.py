'''
Created on Jun 7, 2015

@author: dave
'''
from dragonfly import Function, Key, Mimic, Paste, Text

from caster.lib import settings
from caster.lib.dfplus.hint.hintnode import NodeAction
from caster.lib import control

class DeckItem:
    def __init__(self, type):
        assert type in ["raction", "seeker", "continuer"]
        self.type = type
        self.complete = False  # indicates whether it has been run already
        self.consumed = False  # indicates that an undo is unnecessary
        self.rspec = "default"
    def put_time_action(self):
        ''' this always happens at the time that the deck item is placed in the deck '''
class DeckItemRegisteredAction(DeckItem):
    def __init__(self, registered_action, type="raction"):
        DeckItem.__init__(self, type)
        self.dragonfly_data = registered_action.dragonfly_data
        self.base = registered_action.base
        self.rspec = registered_action.rspec
        self.rdescript = registered_action.rdescript
        self.rundo = registered_action.rundo
    def execute(self):
        self.complete = True
        self.base._execute(self.dragonfly_data)
        self.clean()
    def clean(self):
        self.dragonfly_data = None
    def put_time_action(self):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            control.nexus().comm.get_com("status").text(self.rdescript)
class DeckItemSeeker(DeckItemRegisteredAction):
    def __init__(self, seeker):
        DeckItemRegisteredAction.__init__(self, seeker, "seeker")
        self.back = self.copy_direction(seeker.back)
        self.forward = self.copy_direction(seeker.forward)
        self.consume = seeker.consume
        self.rspec = seeker.rspec
        
    @staticmethod
    def copy_direction(cls):
        result = None
        if cls != None:
            result = []
            for cl in cls:
                result.append(cl.copy())
        return result
    def executeCL(self, cl):
        action = cl.result
        if not action in [Text, Key, Mimic, Function, Paste, NodeAction]:
            # it's a function object
            if cl.parameters == None:
                return action()
            else:
                return action(cl.parameters)
        else:
            # it's a dragonfly action, and the parameters are the spec
            action(cl.parameters)._execute(cl.dragonfly_data)
            return False
    def clean(self):
        # save whatever data you need here
        DeckItemRegisteredAction.clean(self)
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
#         self.dragonfly_data = None # no need to be hanging onto this in more places than one
    def execute(self, unused):
        self.complete = True
        c = []
        if self.back != None:c += self.back
        if self.forward != None:c += self.forward
        for cl in c:
            self.executeCL(cl)
        self.clean()
    def satisfy_level(self, level_index, is_back, deck_item):
        direction = self.back if is_back else self.forward
        cl = direction[level_index]
        if not cl.satisfied:
            if deck_item != None:
                for cs in cl.sets:
                    # deck_item must have a spec
                    if deck_item.rspec in cs.specTriggers:
                        cl.satisfied = True
#                         print deck_item.rspec
                        self.fillCL(cl, cs)
                        break
            if not cl.satisfied:  # if still not satisfied, do default
                cl.satisfied = True
                self.fillCL(cl, cl.sets[0])
#                 print "defaulted", deck_item.rspec
    def get_index_of_next_unsatisfied_level(self):
        for i in range(0, len(self.forward)):
            cl = self.forward[i]
            if not cl.satisfied:
                return i
        return -1
class DeckItemContinuer(DeckItemSeeker):
    def __init__(self, continuer):
        DeckItemRegisteredAction.__init__(self, continuer, "continuer")
        self.back = None
        self.forward = self.copy_direction(continuer.forward)
        self.repetitions = continuer.repetitions
        self.fillCL(self.forward[0], self.forward[0].sets[0])
        self.closure = None
        self.time_in_seconds = continuer.time_in_seconds
        self.consume = continuer.consume
    def satisfy_level(self, level_index, is_back, deck_item):  # level_index and is_back are unused here, but left in for compatibility
        cl = self.forward[0]
        if not cl.satisfied:
            if deck_item != None:
                cs = cl.sets[0]
                if deck_item.rspec in cs.specTriggers:  # deck_item must have a spec
                    cl.satisfied = True
    def get_triggers(self):
        return self.forward[0].sets[0].specTriggers
    def execute(self, success):  # this method should be what deactivates the continuer
        '''
        There are three ways this can be triggered: success, timeout, and cancel.
        Success and timeout are in the closure. Cancels are handled in the deck.
        Waiting commands should only be run on success.
        '''
        self.complete = True
        control.nexus().timer.remove_callback(self.closure)
        DeckItemSeeker.clean(self)
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