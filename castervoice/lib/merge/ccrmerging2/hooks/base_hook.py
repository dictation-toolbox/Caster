from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class BaseHook(object):
    """
    Authors of new hooks should override the "run" method.
    """

    def __init__(self, event_type):
        self._type = event_type

    def run(self):
        raise DontUseBaseClassError(self)

    def match(self, event_type):
        return self._type == event_type
