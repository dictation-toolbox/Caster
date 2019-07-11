from castervoice.lib.dfplus.ccrmerging2.merging.base_merging_strategy import BaseMergingStrategy

'''
This strategy KOs any incompatible rules.
'''


class ClassicMergingStrategy(BaseMergingStrategy):

    def merge(self, sorted_checked_rules):
        merged_rule = None
        for compat_result in sorted_checked_rules:
            if merged_rule is None:
                merged_rule = compat_result.rule()
            elif compat_result.is_compatible():
                merged_rule = merged_rule.merge(compat_result.rule())
        return merged_rule
