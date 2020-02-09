from dragonfly.actions.action_function import Function

from castervoice.asynch.hmc import h_launch
from castervoice.lib import settings, utilities
from castervoice.lib.merge.state.actions import AsynchronousAction, \
    RegisteredAction
from castervoice.lib.merge.state.short import L, S
from castervoice.lib.merge.state.stackitems import StackItemConfirm, \
    StackItemAsynchronous


#win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 1)
class BoxAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    '''

    def __init__(self,
                 receiver,
                 rspec="default",
                 rdescript="unnamed command (BA)",
                 repetitions=60,
                 box_type=settings.QTYPE_DEFAULT,
                 box_settings={},
                 log_failure=False):
        _ = {"tries": 0}
        self._ = _  # signals to the stack to cease waiting, return True terminates

        def check_for_response():
            try:
                _data = self.nexus().comm.get_com("hmc").get_message()
            except Exception:
                if log_failure: utilities.simple_log()
                _["tries"] += 1
                if _["tries"] > 9:
                    return True  # try 10 times max if there's no Homonculus response
                else:
                    return False
            if _data is None: return False
            try:
                _data.append(
                    _["dragonfly_data"])  # pass dragonfly data into receiver function
                _["dragonfly_data"] = None
                receiver(_data)
            except Exception:
                if log_failure: utilities.simple_log()
            return True

        AsynchronousAction.__init__(
            self,  # cannot block, if it does, it'll block its own confirm command
            [L(S(["cancel"], check_for_response))],
            1,
            repetitions,
            rdescript,
            blocking=False)
        self.rspec = rspec
        self.box_type = box_type
        self.box_settings = box_settings  # custom instructions for setting up the tk window ("Homunculus")
        self.log_failure = log_failure

    def _execute(self, data=None):
        self._["tries"] = 0  # reset
        self._["dragonfly_data"] = data
        h_launch.launch(self.box_type, data=self.encode_box_settings())
        self.nexus().state.add(StackItemAsynchronous(self, data))

    def encode_box_settings(self):
        result = ""
        instructions_first = False
        if self.box_type == settings.QTYPE_INSTRUCTIONS and "instructions" in self.box_settings:
            result += settings.HMC_SEPARATOR.join(
                self.box_settings["instructions"].split(" ")) + "|"
            instructions_first = True
        for key in self.box_settings.keys():
            if instructions_first and key == "instructions":
                continue
            result += settings.HMC_SEPARATOR.join(self.box_settings[key].split(" ")) + "|"
        return result


class ConfirmAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    -
    Homunculus response guide:
    0: no response yet
    1: True
    2: False
    -
    This is the only action which requires the nexus in the constructor;
    the rest of them can use the setter. This is because on_complete
    needs a nexus immediately.
    '''

    def __init__(self,
                 base,
                 rspec="default",
                 rdescript="unnamed command (CA)",
                 instructions="instructions missing",
                 nexus=None):
        self.set_nexus(nexus)
        on_complete = AsynchronousAction.hmc_complete(lambda data: receive_response(data))
        AsynchronousAction.__init__(
            self, [L(S(["cancel"], on_complete))], 1, 60, rdescript,
            False)  # cannot block, if it does, it'll block its own confirm command

        self.base = base
        self.rspec = rspec
        self.instructions = instructions

        mutable_integer = {"value": 0}

        def receive_response(
                data):  # signals to the stack to cease waiting, return True terminates
            '''
            receives response from homunculus, uses it to
            stop the stack and tell the ConfirmAction how
            to execute
            '''
            mutable_integer["value"] = data["confirm"]

        self.mutable_integer = mutable_integer

    def _execute(self, data=None):
        '''the factory (ConfirmAction) sharing data with the objects 
        it generates (StackItemConfirm) would be a problem if there 
        could ever be more than one of these at a time, but there can't'''
        self.mutable_integer["value"] = 0

        confirm_stack_item = StackItemConfirm(self, data)
        confirm_stack_item.shared_state(self.mutable_integer)

        h_launch.launch(
            settings.QTYPE_CONFIRM,
            data=settings.HMC_SEPARATOR.join(self.instructions.split(" ")))
        self.nexus().state.add(confirm_stack_item)


class NullAction(RegisteredAction):
    def __init__(self, rspec="default", rdescript="unnamed command (RA)", show=False):
        RegisteredAction.__init__(
            self,
            Function(lambda: None),
            rspec=rspec,
            rdescript=rdescript,
            rundo=None,
            show=show)


class UntilCancelled(AsynchronousAction):
    def __init__(self, action, t=3):
        AsynchronousAction.__init__(self, [L(S(["cancel"], action))], t, 100, "UC", False,
                                    None)
        self.show = True
