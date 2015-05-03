from random import randint

from dragonfly import (ActionBase, Text, Key, Function, Mimic, MappingRule)

from lib import utilities


class CasterState:
    def __init__(self):
        
        ''''''


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
        has = registered_action != None
        self.base = registered_action.base if has else None  # Dragonfly action
        self.rspec = registered_action.rspec if has else "seeker spec"
        self.rdescript = registered_action.rdescript if has else "seeker descript"
        self.breakable = registered_action.rbreakable if has else False
    def execute(self):
        self.complete = True
        self.base._execute()
class DeckItemSeeker(DeckItemRegisteredAction):
    def __init__(self, seeker):
        DeckItemRegisteredAction.__init__(self, None, "seeker")
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
    def execute(self):
        self.complete = True
        c = []
        if self.back != None:c += self.back
        if self.forward != None:c += self.forward
        for cl in c:
            action = cl.result
            if not action in [Text, Key, Mimic]:
                # it's a function object
                if cl.parameters == None:
                    action()
                else:
                    action(cl.parameters)
            else:
                action(cl.parameters)._execute()
    def satisfy_level(self, level_index, is_back, deck_item):
        direction = self.back if is_back else self.forward
        cl = direction[level_index]
        if not cl.satisfied:
            if deck_item != None:
                for cs in cl.sets:
                    # deck_item must have a spec
                    if deck_item.rspec in cs.specTriggers:
                        cl.satisfied = True
                        cl.result = cs.f
                        cl.parameters = cs.parameters
                        break
            if not cl.satisfied and self.type != "continuer":  # if still not satisfied, do default
                cl.satisfied = True
                cl.result = cl.sets[0].f
                cl.parameters = cl.sets[0].parameters
    def get_index_of_next_unsatisfied_level(self):
        for i in range(0, len(self.forward)):
            cl = self.forward[i]
            if not cl.satisfied:
                return i
        return -1


class ContextDeck:
    def __init__(self):
        self.list = []
    
    def add(self, deck_item):  # deck_item is an instance of DeckItem 
        
        
        ''' case: the new item is has backward seeking --
            -- satisfy levels, then move on to other logic'''
        if deck_item.type == "seeker":
            if deck_item.back != None:
                deck_size = len(self.list)
                seekback_size = len(deck_item.back)
                print "deck size: ", deck_size, "seekback_size: ", seekback_size
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
                    seeker.execute()
                # consume deck_item
                if seeker.type != "continuer" and deck_item.type == "raction":  # do not consume seekers, it would disable chaining
                    deck_item.complete = True
                    deck_item.consumed = True
        
        is_forward_seeker = deck_item.type == "seeker" and deck_item.forward != None
        if not deck_item.consumed and not is_forward_seeker:
            deck_item.put_time_action()  # this is where display window information will happen
            deck_item.execute()
                    
        self.list.append(deck_item)
         
        
        # the other cases that need to be handled here:
        # an unsatisfied continuer exists -- satisfy_level will need to be modified
    def generate_registered_action_deck_item(self, raction):
        return DeckItemRegisteredAction(raction)
    def generate_context_seeker_deck_item(self, seeker):
        return DeckItemSeeker(seeker)
    def get_incomplete_seekers(self):
        incomplete = []
        for i in range(0, len(self.list)):
            if not self.list[i].complete:  # no need to check type because only forward seekers will be incomplete
                incomplete.append(self.list[i])
        return incomplete
                



class RegisteredAction(ActionBase):
    def __init__(self, base, rspec="default", rdescript=None, rbreakable=False):
        ActionBase.__init__(self)
        global DECK
        self.deck = DECK
        self.base = base
        self.rspec = rspec
        self.rdescript = rdescript
        self.rbreakable = rbreakable
    
    def _execute(self, data=None):  # copies everything relevant and places it in the deck
        self.deck.add(self.deck.generate_registered_action_deck_item(self))


class CS:  # ContextSet
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

class CL:  # ContextLevel
    '''
    A context level is composed of two or more context sets.
    Once one of the sets is chosen, the level is marked as satisfied
    and the result, either an ActionBase or a function object is
    determined and parameters set.
    '''
    def __init__(self, *args):
        assert len(args) >= 2, "Cannot create ContextLevel with <2 ContextSets"
        self.sets = args
        self.satisfied = False
        self.result = None
        self.parameters = None
    def copy(self):
        return CL(*self.sets)

# ContextSeeker([CL(CS(["ashes"], Text, "ashes to ashes"), CS(["bravery"], Mimic, ["you", "can", "take", "our", "lives"]))], None)

class ContextSeeker(ActionBase):
    def __init__(self, back, forward):
        ActionBase.__init__(self)
        self.back = back
        self.forward = forward
        global DECK
        self.deck = DECK
        assert self.back != None or self.forward != None, "Cannot create ContextSeeker with no levels"
    def _execute(self, data=None):
        self.deck.add(self.deck.generate_context_seeker_deck_item(self))
    
        
        
        

class Continuer(ContextSeeker):
    ''''''
DECK = ContextDeck()
