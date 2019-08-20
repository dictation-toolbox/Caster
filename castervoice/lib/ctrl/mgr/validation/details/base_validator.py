from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class BaseDetailsValidator(object):

    def validate(self, details):
        """
        Details validation, vs rules validation, is about detecting invalid configurations.
        There is no need to check anything here about how the rule matches the configuration.
        Details validators are only about the details objects not themselves being valid.

        Takes a Details, returns error messages if certain kind of invalid configuration
        is contained within it.

        :param details: RuleDetails
        :return: str
        """
        raise DontUseBaseClassError(self)
