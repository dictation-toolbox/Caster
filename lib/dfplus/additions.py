'''
Created on Feb 16, 2015

@author: dave


'''
from dragonfly.actions.action_base import ActionBase
from dragonfly.grammar.context import Context

from lib import utilities


class FiletypeContext(Context):
    """
        Context class using foreground application details.

        This class determines whether the foreground window meets
        certain requirements.  Which requirements must be met for this
        context to match are determined by the constructor arguments.

        Constructor arguments:
         - *filetype* (*str*) --
           the extension of the foreground application's
           file's filetype; case insensitive
        
        Very similar to appcontext, but attempts to keep track of changes to file
        in order to periodically rescan file for Element

    """

    #-----------------------------------------------------------------------
    # Initialization methods.

    def __init__(self, filetype=None, exclude=False):
        Context.__init__(self)

        if isinstance(filetype, str):
            self._title = filetype.lower()
        elif filetype is None:
            self._title = None
        else:
            raise TypeError("filetype argument must be a string or None;"
                        " received %r" % filetype)

        self._exclude = bool(exclude)

        self._str = "%s, %s, %s" % (None, self._title,
                                    self._exclude)

    #-----------------------------------------------------------------------
    # Matching methods.

    def matches(self, executable, title, handle):
        title = title.lower()
        
        if self._title:
            found = (title.find(self._title) != -1)
            if self._exclude == found:
                self._log_match.debug("%s:"
                        " No match, filetype doesn't match." % (self))
                return False

        if self._log_match: self._log_match.debug("%s: Match." % (self))
        print " match encountered: " + self._title
        return True
    
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
            self.action._execute()
