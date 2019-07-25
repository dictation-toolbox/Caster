from castervoice.lib.dfplus.ccrmerging2.sorting.base_ruleset_sorter import BaseRuleSetSorter


class AlphaPronunciationRuleSetSorter(BaseRuleSetSorter):
    def sort_rules(self, rules):
        return sorted(rules, key=lambda mergerule: mergerule.get_pronunciation())
