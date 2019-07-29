from castervoice.lib.merge.ccrmerging2.sorting.base_ruleset_sorter import BaseRuleSetSorter


class ConfigBasedRuleSetSorter(BaseRuleSetSorter):
    """
    Uses a function borrowed from somewhere else to
    determine rule merging order.
    """

    def __init__(self, rules_order_fn):
        self._rules_order_fn = rules_order_fn

    def sort_rules(self, rules):
        ordered_rule_class_names = self._rules_order_fn()
        return sorted(rules, lambda r: ordered_rule_class_names.index(ConfigBasedRuleSetSorter._get_class_name(r)))

    @staticmethod
    def _get_class_name(rule):
        return rule.__class__.__name__
