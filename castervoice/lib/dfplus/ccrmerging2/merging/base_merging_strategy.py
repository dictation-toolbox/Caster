'''
0. Run all transformers over all rules.
1. Use a rule set sorter to sort rules.
2. Use a compatibility checker to calculate incompatibility.
3. Pass the transformed/sorted/checked rules to the merging strategy.

Merging strategies define what happens when two compatibility-checked
rules are merged. The "merge" method should return the resulting
MergeRule.
'''
class BaseMergingStrategy(object):
    
    def merge(self, sorted_checked_rules):
        return None