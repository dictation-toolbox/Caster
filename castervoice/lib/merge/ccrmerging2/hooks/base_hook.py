from castervoice.lib import printer
from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class BaseHook(Pronounceable):
    """
    Authors of new hooks should override the "run_on_event" and "get_pronunciation" methods.
    Optional override "run_on_enable", "run_on_disable" methods
    """

    hook_state = True

    def __init__(self, event_type):
        self._type = event_type

    def run(self):
        raise DontUseBaseClassError(self)

    def run_on_enable(self):
        # Method to override.
        pass

    def _run_on_enable(self):
        # Manages run_on_enable hook state
        try:
            if not self.hook_state:
                self.hook_state = True
                self.run_on_enable()
            else:
                printer.out("{} is already enabled.".format(self.get_class_name()))
        except Exception as err:
            message = "{}: Error with `enable` hook function.\n {}"
            printer.out(message.format(self.get_class_name(), err))

    def run_on_disable(self):
        # Method to override.
        pass

    def _run_on_disable(self):
        # Manages run_on_disable hook state
        try:
            if self.hook_state:
                self.hook_state = False
                self.run_on_disable()
            else:
                printer.out("{} is already disabled.".format(self.get_class_name()))
        except Exception as err:
            message = "{}: Error with `disable` hook function.\n {}"
            printer.out(message.format(self.get_class_name(), err))

    def match(self, event_type):
        return self._type == event_type

    def get_class_name(self):
        return self.__class__.__name__
