'''
Created on Jun 7, 2015

@author: dave
'''
import six
if six.PY2:
    import Queue # pylint: disable=import-error
else:
    import queue as Queue

from dragonfly import RecognitionHistory

from castervoice.lib import settings, utilities
from castervoice.lib.merge.state.stackitems import StackItemSeeker, \
    StackItemRegisteredAction, StackItemAsynchronous, StackItemConfirm


class CasterState:
    def __init__(self):
        self.stack = ContextStack(self)
        self.blocker = None
        self.waiting = Queue.Queue()

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
                    self.waiting.get_nowait()  # discard the Queue if cancelled
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
                self.blocker = task
                break

    def terminate_asynchronous(self, success):
        ''' only for use with Dragonfly Function actions which can't return true or false but need spoken parameters'''
        self.blocker.execute(success)


class ContextStack:
    def __init__(self, state):
        self.list = []
        self.max_list_size = 30
        self.state = state

    def add(self, stack_item):
        stack_item.preserve()
        ''' case: the new item is has backward seeking --
            -- satisfy levels, then move on to other logic'''
        if stack_item.type == StackItemSeeker.TYPE and stack_item.back is not None:
            seeker = stack_item
            stack_size = len(self.list)
            seekback_size = len(seeker.back)

            for i in range(0, seekback_size):
                '''determine whether the seeker should default'''
                no_default = True
                if not seeker.reverse:
                    index = i
                    no_default = index <= stack_size - 1
                else:
                    index = stack_size - 1 - i
                    no_default = index >= 0
                '''satisfy the current level'''
                prior_stack_item = None
                if no_default:
                    prior_stack_item = self.list[-seekback_size:][index]
                seeker.satisfy_level(index, True, prior_stack_item)
                seeker.get_parameters(index, prior_stack_item)
        ''' case: there are forward seekers in the stack --
            -- every incomplete seeker has the reach to
               get a level from this stack item, so make
               a list of incomplete forward seekers, feed
               the new stack item to each of them in order,
               then check them each for completeness in order
               and if they are complete, execute them in FIFO order'''
        incomplete = self.get_incomplete_seekers()
        number_incomplete = len(incomplete)
        seeker_executions = []
        if number_incomplete > 0:
            for i in range(0, number_incomplete):
                seeker = incomplete[i]
                unsatisfied = seeker.get_index_of_next_unsatisfied_level()
                seeker.satisfy_level(unsatisfied, False, stack_item)
                seeker_is_satisfied = seeker.get_index_of_next_unsatisfied_level() == -1
                ''' consume stack_item, but do not consume seekers; it would disable chaining'''
                if (stack_item.type == StackItemRegisteredAction.TYPE or
                    (ContextStack.is_asynchronous(seeker.type) and seeker_is_satisfied)):
                    if seeker.forward[unsatisfied].result.consume:
                        stack_item.complete = True
                        stack_item.consumed = True

                    seeker.get_parameters(unsatisfied, stack_item)

                if seeker_is_satisfied:
                    seeker_executions.append(lambda: seeker.execute(False))

        stack_item_is_forward_seeker = stack_item.type == StackItemSeeker.TYPE and stack_item.forward is not None
        stack_item_is_continuer = ContextStack.is_asynchronous(stack_item.type)
        if not stack_item.consumed and not stack_item_is_forward_seeker and not stack_item_is_continuer:
            stack_item.put_time_action(
            )  # this is where display window information will happen
            stack_item.execute()
        elif stack_item_is_continuer:
            stack_item.begin()
            stack_item.put_time_action()
        ''' forward seeker executions occur after unconsumed triggers -- moved here for more consistent behavior '''
        for seeker_execution in seeker_executions:
            seeker_execution()

        self.list.append(stack_item)
        if len(self.list) > self.max_list_size:  # make this number configurable
            self.list.remove(self.list[0])

    def get_incomplete_seekers(self):
        incomplete = []
        for i in range(0, len(self.list)):
            if not self.list[
                    i].complete:  # no need to check type because only forward seekers will be incomplete
                incomplete.append(self.list[i])
        return incomplete

    @staticmethod
    def is_asynchronous(action_type):
        return action_type in [StackItemAsynchronous.TYPE, StackItemConfirm.TYPE]
