from dragonfly import (ActionBase)

from caster.lib import utilities, control


if control.nexus().dep.NATLINK:
    import natlink
    
class SelectiveAction(ActionBase):
    def __init__(self, action, executables, negate=True):
        '''
        action: another Dragonfly action
        executables: an array of strings, each of which is the name of an executable
        negate: if True, the action should not occur during any of the listed executables, if false the opposite
        '''
        ActionBase.__init__(self)
        self.action = action
        self.executables = executables
        self.negate = negate
        
    def _execute(self, data=None):
        if control.nexus().dep.NATLINK:
            executable = utilities.get_active_window_path(natlink).split("\\")[-1]
            is_executable = executable in self.executables
            if (is_executable and not self.negate) or (self.negate and not is_executable):
                self.action._execute()
        else:
            utilities.availability_message("SelectiveAction", "natlink")
            self.action._execute()

