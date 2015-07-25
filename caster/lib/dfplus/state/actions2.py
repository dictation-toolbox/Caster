from caster.asynch.hmc import h_launch
from caster.lib import settings
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import L, S




class ConfirmAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    -
    Homunculus response guide:
    0: no response yet
    1: True
    2: False
    '''
    def __init__(self, base, rspec="default", rdescript="unnamed command (RA)"):
        mutable_integer = {"value": 0}
        def check_response(): # signals to the stack to cease waiting, return True terminates
            return mutable_integer["value"]!=0
        self.mutable_integer = mutable_integer
        AsynchronousAction.__init__(self, 
                                    [L(S(["cancel"], check_response, None))], 
                                    1, 60, rdescript, False)# cannot block, if it does, it'll block its own confirm command
        self.base = base
        self.rspec = rspec
    def _execute(self, data=None):
        confirm_stack_item = self.state.generate_confirm_stack_item(self, data)
        self.mutable_integer["value"] = 0
        mutable_integer = self.mutable_integer
        def hmc_closure(data):
            '''
            receives response from homunculus, uses it to
            stop the stack and tell the ConfirmAction how
            to execute
            '''
            mutable_integer["value"] = data["confirm"]
            confirm_stack_item.receive_hmc_response(data["confirm"])
                    
        h_launch.launch(settings.QTYPE_CONFIRM, hmc_closure, "_".join(self.rdescript.split(" ")))
        self.state.add(confirm_stack_item)
