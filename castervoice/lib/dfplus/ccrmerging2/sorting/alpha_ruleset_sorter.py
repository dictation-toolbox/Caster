from castervoice.lib.dfplus.ccrmerging2.sorting.base_ruleset_sorter import BaseRuleSetSorter


class AlphaRuleSetSorter(BaseRuleSetSorter):
    def sort_ruleset(self, ruleset):
        return sorted(ruleset, key=lambda mergerule: mergerule.get_pronunciation())
