class BaseMergingStrategy(object):
    """
    Merging strategies define how the transformed, sorter, compat-checked
    rules become one or more merged CCR rules.
    """

    def merge(self, sorted_checked_rules):
        return []
