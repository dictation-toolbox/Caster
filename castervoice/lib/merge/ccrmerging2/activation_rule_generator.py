from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class ActivationRuleGenerator(object):
    def construct_activation_rule(self):
        """
        Returns a rule which has activation commands.
        """
        raise DontUseBaseClassError(self)