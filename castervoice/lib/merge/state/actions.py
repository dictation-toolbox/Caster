from dragonfly import ActionBase

from castervoice.lib import control
from castervoice.lib.merge.state.stackitems import StackItemRegisteredAction, \
    StackItemSeeker, StackItemAsynchronous


class RegisteredAction(ActionBase):
    def __init__(self,
                 base,
                 rspec="default",
                 rdescript=None,
                 rundo=None,
                 show=True):
        ActionBase.__init__(self)
        self._nexus = None
        self.base = base
        self.rspec = rspec
        self.rdescript = rdescript
        self.rundo = rundo
        self.show = show

    def __mul__(self, factor):
        self.base = self.base * factor
        return self

    def _execute(self, data=None):
        # copies everything relevant and places it in the stack
        self.nexus().state.add(StackItemRegisteredAction(self, data))

    def set_nexus(self, nexus):
        self._nexus = nexus

    def nexus(self):
        return self._nexus or control.nexus()


class ContextSeeker(RegisteredAction):
    def __init__(self,
                 back=None,
                 forward=None,
                 rspec="default",
                 rdescript="unnamed command (CS)",
                 reverse=False):
        RegisteredAction.__init__(self, None)
        self.back = back
        self.forward = forward
        self.rspec = rspec
        self.rdescript = rdescript
        self.reverse = reverse  # indicates that context levels on backward seekers should be satisfied in reverse order
        assert self.back is not None or self.forward is not None, "Cannot create ContextSeeker with no levels"

    def _execute(self, data=None):
        self.nexus().state.add(StackItemSeeker(self, data))


class AsynchronousAction(ContextSeeker):
    '''
    AsynchronousAction should have exactly one ContextLevel with one ContextSet.
    Any triggers in the 0th ContextSet will terminate the AsynchronousAction.
    The repetitions parameter indicates the maximum times the function provided
    in the 0th ContextSet should run. 0 indicates forever (or until the
    termination word is spoken). The time_in_seconds parameter indicates
    how often the associated function should run.
    '''

    def __init__(self,
                 forward,
                 time_in_seconds=1,
                 repetitions=0,
                 rdescript="unnamed command (A)",
                 blocking=True,
                 finisher=None):
        forward[0].sets[
            0].consume = False  # consume is for ContextSeekers, not AsynchronousActions
        ContextSeeker.__init__(self, None, forward)
        self.repetitions = repetitions
        self.time_in_seconds = time_in_seconds
        self.rdescript = rdescript
        self.blocking = blocking
        self.base = finisher
        assert self.forward is not None, "Cannot create AsynchronousAction with no termination commands"
        assert len(
            self.forward) == 1, "Cannot create AsynchronousAction with > or < one purpose"

    def _execute(self, data=None):
        if data is not None:
            if "time_in_seconds" in data:
                self.time_in_seconds = float(data["time_in_seconds"])
            if "repetitions" in data: self.time_in_seconds = int(data["repetitions"])

        self.nexus().state.add(StackItemAsynchronous(self, data))

    @staticmethod
    def hmc_complete(data_function):
        ''' returns a function which applies the passed in function to
        the data returned by the pop-up window - the returned function
        will be called by AsynchronousAction's timer repeatedly,
        to see if the data is available yet'''

        def check_complete():
            data = None
            try:
                data = control.nexus().comm.get_com("hmc").get_message()
                if data is None:
                    return False
            except Exception:
                return False
            data_function(data)
            return True

        return check_complete
