import Queue
import xmlrpclib

from dragonfly import (ActionBase, Text, Key, Function, Mimic, Paste)

from caster.asynch import statuswindow
from caster.lib import control, utilities, settings


class CasterState:
    def __init__(self):
        self.deck = ContextDeck(self)
        self.blocker = None
        self.waiting = Queue.Queue()
    def add(self, deck_item):
        if self.blocker == None:
            ''' important to block before adding because the add might unblock '''
            if deck_item.type == "continuer":
                self.blocker = deck_item
            self.deck.add(deck_item)
        else:
            if deck_item.rspec in self.blocker.get_triggers():  # let cancels go through
                self.unblock()
                while not self.waiting.empty():
                    self.waiting.get_nowait() # discard the Queue if cancelled
                self.add(deck_item)
            else:
                self.waiting.put_nowait(deck_item)
    def unblock(self):
        self.blocker = None
    def run_waiting_commands(self):
        self.unblock()
        while not self.waiting.empty():
            task = self.waiting.get(True, 2)
            task.execute()
            if task.type == "continuer":
                self.blocker=task
                break
    def halt_asynchronous(self, success):
        ''' only for use with Dragonfly Function actions which can't return true or false but need spoken parameters'''
        self.blocker.execute(success)
#         if success:
#             self.run_waiting_commands()
#         else:
#             self.unblock()
    def generate_registered_action_deck_item(self, raction):
        return DeckItemRegisteredAction(raction)
    def generate_context_seeker_deck_item(self, seeker):
        return DeckItemSeeker(seeker)
    def generate_continuer_deck_item(self, continuer):
        return DeckItemContinuer(continuer)

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
            control.COMM.get_com("status").text(self.rdescript)
class DeckItemSeeker(DeckItemRegisteredAction):
    def __init__(self, seeker):
        DeckItemRegisteredAction.__init__(self, seeker, "seeker")
        self.back = self.copy_direction(seeker.back)
        self.forward = self.copy_direction(seeker.forward)
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
        if not action in [Text, Key, Mimic, Function, Paste]:
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
class DeckItemContinuer(DeckItemSeeker):
    def __init__(self, continuer):
        DeckItemRegisteredAction.__init__(self, continuer, "continuer")
        self.back = None
        self.forward = self.copy_direction(continuer.forward)
        self.repetitions = continuer.repetitions
        self.fillCL(self.forward[0], self.forward[0].sets[0])
        self.closure = None
        self.time_in_seconds = continuer.time_in_seconds
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
        control.TIMER_MANAGER.remove_callback(self.closure)
        DeckItemSeeker.clean(self)
        self.closure = None
        global STATE
        if success:
            STATE.run_waiting_commands()
        else:
            STATE.unblock()
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
                try:
                    e(terminate)
                except Exception:
                    utilities.simple_log(False) 
                
            elif r != 0:  # if not run forever
                c["value"] += 1
                if c["value"] == r:
                    e(False)
        self.closure = closure
        control.TIMER_MANAGER.add_callback(self.closure, self.time_in_seconds)
        self.closure()
 
        

class ContextDeck:
    def __init__(self, state):
        self.list = []
        self.state = state
    
    def add(self, deck_item):  # deck_item is an instance of DeckItem 
        
        
        ''' case: the new item is has backward seeking --
            -- satisfy levels, then move on to other logic'''
        if deck_item.type == "seeker":
            if deck_item.back != None:
                deck_size = len(self.list)
                seekback_size = len(deck_item.back)
                # print "deck size: ", deck_size, "seekback_size: ", seekback_size
                for i in range(0, seekback_size):
                    index = deck_size - 1 - i
                    # back looking seekers have nothing else to wait for
                    if index >= 0 and self.list[index].base != None:
                        # what's the purpose in blocking seeker chaining?
                        prev = self.list[index]  # if self.list[index].type not in ["seeker", "continuer"] else None
                        deck_item.satisfy_level(i, True, prev)
                    else:
                        deck_item.satisfy_level(i, True, None)
        
        ''' case: there are forward seekers in the deck --
            -- every incomplete seeker has the reach to 
               get a level from this deck item, so make
               a list of incomplete forward seekers, feed 
               the new deck item to each of them in order, 
               then check them each for completeness in order 
               and if they are complete, execute them in FIFO order'''
        incomplete = self.get_incomplete_seekers()
        number_incomplete = len(incomplete)
        if number_incomplete > 0:
            for i in range(0, number_incomplete):
                seeker = incomplete[i]
                seeker.satisfy_level(seeker.get_index_of_next_unsatisfied_level(), False, deck_item)
                if seeker.get_index_of_next_unsatisfied_level() == -1:
                    seeker.execute(False)
                # consume deck_item
                if ((seeker.type != "continuer" and deck_item.type == "raction")  # do not consume seekers, it would disable chaining
                or (seeker.type == "continuer" and seeker.get_index_of_next_unsatisfied_level() == -1)):
                    deck_item.complete = True
                    deck_item.consumed = True
                    deck_item.clean()
        
        is_forward_seeker = deck_item.type == "seeker" and deck_item.forward != None
        is_continuer = deck_item.type == "continuer"
        if not deck_item.consumed and not is_forward_seeker and not is_continuer:
            deck_item.execute()
            deck_item.put_time_action()  # this is where display window information will happen
        elif is_continuer:
            deck_item.begin()
            deck_item.put_time_action()
                    
        self.list.append(deck_item)
    
    def get_incomplete_seekers(self):
        incomplete = []
        for i in range(0, len(self.list)):
            if not self.list[i].complete:  # no need to check type because only forward seekers will be incomplete
                incomplete.append(self.list[i])
        return incomplete
                

class RegisteredAction(ActionBase):
    def __init__(self, base, rspec="default", rdescript=None, rundo=None):
        ActionBase.__init__(self)
        global STATE
        self.state = STATE
        self.base = base
        self.rspec = rspec
        self.rdescript = rdescript
        self.rundo = rundo
    
    def _execute(self, data=None):  # copies everything relevant and places it in the deck
        self.dragonfly_data = data
        self.state.add(self.state.generate_registered_action_deck_item(self))


class ContextSet:  # ContextSet
    '''
    The context has composed one or more trigger words. These trigger words
    will be the spec of another command. That other command will be consumed
    by the ContextSeeker and will not be executed.
    '''
    def __init__(self, specTriggers, f, parameters=None):
        assert len(specTriggers) > 0, "ContextSet must have at least one spec trigger"
        assert f != None, "Function parameter can't be null"
        self.specTriggers = specTriggers
        self.f = f
        self.parameters = parameters

class ContextLevel:  # ContextLevel
    '''
    A ContextLevel is composed of one or more ContextSets.
    Once one of the ContextSets is chosen, the ContextLevel is marked as satisfied
    and the result, either an ActionBase or a function object is
    determined and parameters set.
    '''
    def __init__(self, *args):
        self.sets = args
        self.satisfied = False
        self.result = None
        self.parameters = None
        self.dragonfly_data = None
    def copy(self):
        return ContextLevel(*self.sets)

class ContextSeeker(RegisteredAction):
    def __init__(self, back, forward):
        RegisteredAction.__init__(self, None)
        self.back = back
        self.forward = forward
        global STATE
        self.state = STATE
        assert self.back != None or self.forward != None, "Cannot create ContextSeeker with no levels"
    def _execute(self, data=None):
        self.dragonfly_data = data
        self.state.add(self.state.generate_context_seeker_deck_item(self))
        
        
        
        

class Continuer(ContextSeeker):
    '''
    A Continuer should have exactly one ContextLevel with one ContextSet.
    Any triggers in the 0th ContextSet will terminate the Continuer.
    The repetitions parameter indicates the maximum times the function provided
    in the 0th ContextSet should run. 0 indicates forever (or until the 
    termination word is spoken). The time_in_seconds parameter indicates
    how often the associated function should run.
    '''
    def __init__(self, forward, time_in_seconds=1, repetitions=0):
        ContextSeeker.__init__(self, None, forward)
#         self.forward = forward
        self.repetitions = repetitions
        self.time_in_seconds = time_in_seconds
        global STATE
        self.state = STATE
        assert self.forward != None, "Cannot create Continuer with no termination commands"
        assert len(self.forward) == 1, "Cannot create Continuer with > or < one purpose"
    def _execute(self, data=None):
        if "time_in_seconds" in data: self.time_in_seconds=float(data["time_in_seconds"])
        if "repetitions" in data: self.time_in_seconds=int(data["repetitions"])
          
        self.dragonfly_data = data
        self.state.add(self.state.generate_continuer_deck_item(self))

# shorter names for classes
R = RegisteredAction
L = ContextLevel
S = ContextSet
STATE = CasterState()
