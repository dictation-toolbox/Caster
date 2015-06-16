'''
Created on Jun 7, 2015

@author: dave
'''
from dragonfly import ActionBase

from caster.lib import control

class RegisteredAction(ActionBase):
    def __init__(self, base, rspec="default", rdescript=None, rundo=None):
        ActionBase.__init__(self)
        self.state = control.nexus().state
        self.base = base
        self.rspec = rspec
        self.rdescript = rdescript
        self.rundo = rundo
    
    def _execute(self, data=None):  # copies everything relevant and places it in the deck
        self.dragonfly_data = data
        self.state.add(self.state.generate_registered_action_deck_item(self))




class ContextSeeker(RegisteredAction):
    def __init__(self, back, forward, rspec="default", rdescript="unnamed command (CS)", consume=True):
        RegisteredAction.__init__(self, None)
        self.back = back
        self.forward = forward
        self.rspec = rspec
        self.rdescript = rdescript
        self.consume = consume
        self.state = control.nexus().state
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
    def __init__(self, forward, time_in_seconds=1, repetitions=0, rdescript="unnamed command (A)"):
        ContextSeeker.__init__(self, None, forward)
#         self.forward = forward
        self.repetitions = repetitions
        self.time_in_seconds = time_in_seconds
        self.rdescript = rdescript
        self.state = control.nexus().state
        assert self.forward != None, "Cannot create Continuer with no termination commands"
        assert len(self.forward) == 1, "Cannot create Continuer with > or < one purpose"
    def _execute(self, data=None):
        if "time_in_seconds" in data: self.time_in_seconds=float(data["time_in_seconds"])
        if "repetitions" in data: self.time_in_seconds=int(data["repetitions"])
          
        self.dragonfly_data = data
        self.state.add(self.state.generate_continuer_deck_item(self))