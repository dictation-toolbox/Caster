'''
Created on Jun 7, 2015

@author: dave
'''
from dragonfly import Pause, ActionBase, get_current_engine

from castervoice.lib import printer, settings


class StackItem:
    def __init__(self, type):
        assert type in [
            StackItemRegisteredAction.TYPE, StackItemSeeker.TYPE,
            StackItemAsynchronous.TYPE, StackItemConfirm.TYPE
        ]
        self.type = type
        self.complete = False  # indicates whether it has been run already
        self.consumed = False  # indicates that an undo is unnecessary
        self.rspec = "default"

    def put_time_action(self):
        ''' this always happens at the time that the Stack item is placed in the Stack '''


class StackItemRegisteredAction(StackItem):
    TYPE = "raction"

    def __init__(self, registered_action, data, type=TYPE):
        StackItem.__init__(self, type)
        self.dragonfly_data = data
        self.base = registered_action.base
        self.rspec = registered_action.rspec
        self.rdescript = registered_action.rdescript
        self.rundo = registered_action.rundo
        self.show = registered_action.show
        self.preserved = []
        self.nexus = registered_action.nexus()

    def execute(self):
        self.complete = True
        self.base.execute(self.dragonfly_data)
        # do presentation here
        self.clean()

    def clean(self):
        self.dragonfly_data = None
        self.base = None

    def preserve(self):
        '''save the useful parts of the incoming dragonfly data
        (in this case, spoken words)'''
        if self.dragonfly_data is not None:
            self.preserved = [x[0] for x in self.dragonfly_data["_node"].results]
            return True
        return False

    def get_preserved(self):
        return self.preserved

    def put_time_action(self):
        self.preserve()
        if settings.SETTINGS["miscellaneous"]["print_rdescripts"] and self.show:
            # formats rdescript with the given data
            try:
                rd = self.rdescript % self.dragonfly_data if self.dragonfly_data else self.rdescript
            except KeyError:
                rd = self.rdescript
            except TypeError:
                print("TypeError: dragonfly_data <{}>".format(self.dragonfly_data))
                rd = self.rdescript
            printer.out(rd)


class StackItemSeeker(StackItemRegisteredAction):
    TYPE = "seeker"

    def __init__(self, seeker, data, type=TYPE):
        StackItemRegisteredAction.__init__(self, seeker, data, type)
        if self.type == StackItemSeeker.TYPE: self.back = self.copy_direction(seeker.back)
        self.forward = self.copy_direction(seeker.forward)
        self.reverse = seeker.reverse
        self.param_spoken = {}
        self.param_rspec = {}

    @staticmethod
    def copy_direction(context_levels):
        result = None
        if context_levels is not None:
            result = []
            for i in range(0, len(context_levels)):
                context_level = context_levels[i].copy()
                context_level.number(i)
                result.append(context_level)
        return result

    def executeCL(self, context_level
                  ):  # the return value is whether to terminate an AsynchronousAction
        action = context_level.result.f
        if action is None:
            return False
        elif isinstance(action, ActionBase):
            action.execute(context_level.dragonfly_data)
            return False
        else:
            # it's a function object, so get the parameters, if any
            level = context_level.index
            fnparams = context_level.result.parameters
            if context_level.result.use_spoken:
                fnparams = self.param_spoken[level]
            if context_level.result.use_rspec:
                fnparams = self.param_rspec[level]
            if fnparams is None:
                return action()
            else:
                return action(fnparams)

    def get_parameters(self, level, stack_item):
        '''gets information from another stack item
        for use as parameters in a ContextSet's
        function object in executeCL()'''
        self.param_spoken[level] = stack_item.preserved  # array of strings
        self.param_rspec[level] = stack_item.rspec  # single string

    def clean(self):
        '''clean up now-unnecessary references'''
        StackItemRegisteredAction.clean(self)
        if self.back is not None:
            for context_level in self.back:
                context_level.dragonfly_data = None
        if self.forward is not None:
            for context_level in self.forward:
                context_level.dragonfly_data = None

    def fillCL(self, context_level, context_set):
        context_level.result = context_set
        context_level.dragonfly_data = self.dragonfly_data

    def execute(self, unused=None):  # "unused" is only for Async, but must also be here
        self.complete = True
        c = []
        if self.reverse: self.back.reverse()
        if self.back is not None: c += self.back
        if self.forward is not None: c += self.forward
        for context_level in c:
            self.executeCL(context_level)
        self.clean()

    def satisfy_level(self, level_index, is_back, stack_item):
        direction = self.back if is_back else self.forward
        reverse = -1 if self.reverse else 1
        context_level = direction[level_index*reverse]
        if not context_level.satisfied:
            if stack_item is not None:
                for context_set in context_level.sets:
                    # stack_item must have a spec
                    if stack_item.rspec in context_set.specTriggers or "*" in context_set.specTriggers:
                        context_level.satisfied = True
                        self.fillCL(context_level, context_set)
                        break
            if not context_level.satisfied:  # if still not satisfied, do default
                context_level.satisfied = True
                self.fillCL(context_level, context_level.sets[0])

    def get_index_of_next_unsatisfied_level(self):
        for i in range(0, len(self.forward)):
            context_level = self.forward[i]
            if not context_level.satisfied:
                return i
        return -1


class StackItemAsynchronous(StackItemSeeker):
    TYPE = "continuer"

    def __init__(self, continuer, data, type=TYPE):
        StackItemSeeker.__init__(self, continuer, data, type)
        self.back = None
        self.closure = None
        self.fillCL(self.forward[0],
                    self.forward[0].sets[0])  # set context set and dragonfly data
        self.repetitions = continuer.repetitions

        self.time_in_seconds = continuer.time_in_seconds
        self.blocking = continuer.blocking
        self.timer = None

    def satisfy_level(
            self, level_index, is_back, stack_item
    ):  # level_index and is_back are unused here, but left in for compatibility
        context_level = self.forward[0]
        if not context_level.satisfied:
            if stack_item is not None:
                context_set = context_level.sets[0]
                if stack_item.rspec in context_set.specTriggers:  # stack_item must have a spec
                    context_level.satisfied = True

    def get_triggers(self):
        return self.forward[0].sets[0].specTriggers

    def execute(self, success):  # this method should be what deactivates the continuer
        '''
        There are three ways this can be triggered: success, timeout, and cancel.
        Success and timeout are in the closure. Cancels are handled in the Stack.
        Waiting commands should only be run on success.
        '''
        self.complete = True

        if self.base is not None:  # finisher
            self.base.execute()

        self.clean()

        if success:
            self.nexus.state.run_waiting_commands()
        else:
            self.nexus.state.unblock()

    def clean(self):
        StackItemSeeker.clean(self)
        self.timer.stop()
        self.timer = None
        self.closure = None

    def begin(self):
        '''here pass along a closure to the timer multiplexer'''
        execute_context_levels = self.executeCL
        context_level = self.forward[0]
        repetitions = self.repetitions
        count = {"value": 0}
        execute = self.execute

        def closure():
            do_terminate = execute_context_levels(context_level)
            if do_terminate:
                execute(do_terminate)

            elif repetitions != 0:  # if not run forever
                count["value"] += 1
                if count["value"] == repetitions:
                    execute(False)

        self.closure = closure
        self.timer = get_current_engine().create_timer(self.closure, self.time_in_seconds)
        self.closure()


class StackItemConfirm(StackItemAsynchronous):
    TYPE = "confirm"

    def __init__(self, confirm, data, type=TYPE):
        StackItemAsynchronous.__init__(self, confirm, data, type)
        self.base = Pause("50") + confirm.base  # TODO: fix this race condition
        self.rspec = confirm.rspec
        self.hmc_response = 0

    def execute(self, success):
        if self.mutable_integer["value"] == 1:
            self.base.execute(self.dragonfly_data)
        self.base = None
        StackItemAsynchronous.execute(self, success)

    def shared_state(self, mutable_integer):
        self.mutable_integer = mutable_integer
