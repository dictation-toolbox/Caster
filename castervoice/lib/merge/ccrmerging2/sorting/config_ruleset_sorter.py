from castervoice.lib.merge.ccrmerging2.sorting.base_ruleset_sorter import BaseRuleSetSorter


class _IndexedRule(object):
    def __init__(self, rule, index):
        self.rule = rule
        self.index = index


class ConfigBasedRuleSetSorter(BaseRuleSetSorter):
    """
    Uses a function borrowed from somewhere else to
    determine rule merging order.
    """

    def __init__(self, ordered_rcns):
        self._ordered_rcns = list(ordered_rcns)

    def sort_rules(self, rules):
        indexed_rules = [_IndexedRule(r, self._ordered_rcns.index(ConfigBasedRuleSetSorter._get_class_name(r)))
                         for r in rules]
        sorted_indexed_rules = sorted(indexed_rules, key=lambda ir: ir.index)
        return [i.rule for i in sorted_indexed_rules]

    @staticmethod
    def _get_class_name(rule):
        return rule.__class__.__name__
