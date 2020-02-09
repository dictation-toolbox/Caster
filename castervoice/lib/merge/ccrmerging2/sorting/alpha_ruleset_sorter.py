from castervoice.lib.merge.ccrmerging2.sorting.base_ruleset_sorter import BaseRuleSetSorter


class AlphaRuleSetSorter(BaseRuleSetSorter):
    def sort_rules(self, rules):
        return sorted(rules, key=AlphaRuleSetSorter._pronunciation_or_name)

    @staticmethod
    def _pronunciation_or_name(rule):
        if hasattr(rule, "get_pronunciation"):
            return rule.get_pronunciation().lower()
        return rule.name.lower()
