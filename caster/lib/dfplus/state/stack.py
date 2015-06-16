'''
Created on Jun 7, 2015

@author: dave
'''
import Queue

from caster.lib import control
from caster.lib.dfplus.state.stackitems import DeckItemRegisteredAction, \
    DeckItemSeeker, DeckItemContinuer




class CasterState:
    def __init__(self):
        self.deck = ContextStack(self)
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
    def generate_registered_action_deck_item(self, raction):
        return DeckItemRegisteredAction(raction)
    def generate_context_seeker_deck_item(self, seeker):
        return DeckItemSeeker(seeker)
    def generate_continuer_deck_item(self, continuer):
        return DeckItemContinuer(continuer)

class ContextStack:
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
                    if seeker.consume:
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


control.nexus().inform_state(CasterState())