'''
Created on Jun 7, 2015

@author: dave
'''
import Queue

from caster.lib import settings
from caster.lib.dfplus.state.stackitems import StackItemRegisteredAction, \
    StackItemSeeker, StackItemAsynchronous, StackItemConfirm


class CasterState:
    def __init__(self, nexus):
        self.stack = ContextStack(self)
        self.blocker = None
        self.waiting = Queue.Queue()
        self.nexus = nexus
    def add(self, stack_item):
        if self.blocker is None:
            ''' important to block before adding because the add might unblock '''
            if ContextStack.is_asynchronous(stack_item.type) and stack_item.blocking:
                self.blocker = stack_item
            self.stack.add(stack_item)
        else:
            if stack_item.rspec in self.blocker.get_triggers():  # let cancels go through
                self.unblock()
                while not self.waiting.empty():
                    self.waiting.get_nowait() # discard the Queue if cancelled
                self.add(stack_item)
            else:
                self.waiting.put_nowait(stack_item)
    def unblock(self):
        self.blocker = None
    def run_waiting_commands(self):
        self.unblock()
        while not self.waiting.empty():
            task = self.waiting.get(True, 2)
            task.execute()
            if ContextStack.is_asynchronous(task.type):
                self.blocker=task
                break
    def terminate_asynchronous(self, success):
        ''' only for use with Dragonfly Function actions which can't return true or false but need spoken parameters'''
        self.blocker.execute(success)

class ContextStack:
    def __init__(self, state):
        self.list = []
        self.state = state
    
    def add(self, stack_item):  # stack_item is an instance of stackItem 
        stack_item.preserve()
        if settings.WSR:
            self.state.nexus.history.on_recognition(stack_item.get_preserved())            
        
        ''' case: the new item is has backward seeking --
            -- satisfy levels, then move on to other logic'''
        if stack_item.type == StackItemSeeker.TYPE and stack_item.back is not None:
                stack_size = len(self.list)
                seekback_size = len(stack_item.back)
                for i in range(0, seekback_size):
                    index = stack_size - 1 - i
                    # back looking seekers have nothing else to wait for
                    if index >= 0 and self.list[index].base != None:
                        # what's the purpose in blocking seeker chaining?
                        prev = self.list[index]  # if self.list[index].type not in ["seeker", "continuer"] else None
                        stack_item.satisfy_level(i, True, prev)
                        stack_item.eat(i, prev)
                    else:
                        stack_item.satisfy_level(i, True, None)
        
        ''' case: there are forward seekers in the stack --
            -- every incomplete seeker has the reach to 
               get a level from this stack item, so make
               a list of incomplete forward seekers, feed 
               the new stack item to each of them in order, 
               then check them each for completeness in order 
               and if they are complete, execute them in FIFO order'''
        incomplete = self.get_incomplete_seekers()
        number_incomplete = len(incomplete)
        if number_incomplete > 0:
            for i in range(0, number_incomplete):
                seeker = incomplete[i]
                unsatisfied = seeker.get_index_of_next_unsatisfied_level()
                seeker.satisfy_level(unsatisfied, False, stack_item)
                
                # consume stack_item
                seeker_is_continuer = ContextStack.is_asynchronous(seeker.type)
                if ((stack_item.type == StackItemRegisteredAction.TYPE and not seeker_is_continuer)  # do not consume seekers, it would disable chaining
                or (seeker_is_continuer and seeker.get_index_of_next_unsatisfied_level() == -1)):
                    if seeker.forward[unsatisfied].result.consume:
                        stack_item.complete = True
                        stack_item.consumed = True
                        stack_item.clean()
                    seeker.eat(unsatisfied, stack_item)
                
                if seeker.get_index_of_next_unsatisfied_level() == -1:
                    seeker.execute(False)
                
        stack_item_is_forward_seeker = stack_item.type == StackItemSeeker.TYPE and stack_item.forward != None
        stack_item_is_continuer = ContextStack.is_asynchronous(stack_item.type)
        if not stack_item.consumed and not stack_item_is_forward_seeker and not stack_item_is_continuer:
            stack_item.execute()
            stack_item.put_time_action()  # this is where display window information will happen
        elif stack_item_is_continuer:
            stack_item.begin()
            stack_item.put_time_action()
                    
        self.list.append(stack_item)
        if len(self.list)>100:# make this number configurable
            self.list.remove(self.list[0])
    
    def get_incomplete_seekers(self):
        incomplete = []
        for i in range(0, len(self.list)):
            if not self.list[i].complete:  # no need to check type because only forward seekers will be incomplete
                incomplete.append(self.list[i])
        return incomplete
    
    @staticmethod
    def is_asynchronous(action_type):
        return action_type in [StackItemAsynchronous.TYPE, StackItemConfirm.TYPE]

