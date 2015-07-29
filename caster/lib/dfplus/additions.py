from dragonfly import (ActionBase)

from caster.lib import utilities

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
        executable = utilities.get_active_window_path().split("\\")[-1]
        is_executable = executable in self.executables
        if (is_executable and not self.negate) or (self.negate and not is_executable):
            self.action.execute()

class FuzzyMatch(ActionBase):
    '''
    list_function: provides a list of strings to filter
    filter_function: reduces the size of the list from list_function
    selection_function: what to do with the result that the user chooses
    '''
    def __init__(self, list_function, filter_function, selection_function):
        ''''''
        
        
        
        
        
        
        
        
        
    