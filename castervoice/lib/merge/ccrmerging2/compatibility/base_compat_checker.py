from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class BaseCompatibilityChecker(object):
    """
    Implementors of new compat checkers should override the "compatibility_check" method.
    """

    def compatibility_check(self, mergerules):
        raise DontUseBaseClassError(self)
