'''
Merging strategies define what happens when two compatibility-checked
rules are merged. The "merge" method should return the resulting
MergeRule.
'''


class BaseMergingStrategy(object):

    def merge(self, sorted_checked_rules):
        return None
