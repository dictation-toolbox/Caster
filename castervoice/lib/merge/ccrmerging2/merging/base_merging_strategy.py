from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError


class BaseMergingStrategy(object):
    """
    Merging strategies define how the transformed, sorter, compat-checked
    rules become one or more merged CCR rules.
    """

    def merge_into_single(self, sorted_checked_rules):
        raise DontUseBaseClassError() # pylint: disable=no-value-for-parameter
