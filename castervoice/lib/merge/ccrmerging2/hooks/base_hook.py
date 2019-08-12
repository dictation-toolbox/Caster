from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError
from castervoice.lib.merge.ccrmerging2.pronounceable import Pronounceable


class BaseHook(Pronounceable):
    """
    Authors of new hooks should override the "run" and "get_pronunciation" methods.
    """

    def __init__(self, event_type):
        self._type = event_type

    def run(self):
        raise DontUseBaseClassError(self)

    def match(self, event_type):
        return self._type == event_type

    def get_class_name(self):
        return self.__class__.__name__
