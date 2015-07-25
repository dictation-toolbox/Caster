from caster.dev import print_time
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import L, S


class ConfirmAction(AsynchronousAction):
    '''
    
    '''
    def __init__(self, base, rspec="default", rdescript="unnamed command (RA)"):
        forward = [L(S(["cancel"], print_time, None))]
        AsynchronousAction.__init__(self, forward, 1, 60, rdescript, False)
        self.base = base
        self.rspec = rspec
    def _execute(self, data=None):
        self.state.add(self.state.generate_continuer_stack_item(self, data))