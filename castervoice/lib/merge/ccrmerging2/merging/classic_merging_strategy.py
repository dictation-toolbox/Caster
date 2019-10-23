from castervoice.lib.merge.ccrmerging2.merging.base_merging_strategy import BaseMergingStrategy


class ClassicMergingStrategy(BaseMergingStrategy):
    """
    This strategy KOs any incompatible rules.
    """

    def merge_into_single(self, sorted_checked_rules):
        """
        Merge any rules which aren't KO'd by their peers.
        Done in O(n) for the total number of specs.

        :param sorted_checked_rules: list of CompatibilityResult
        :return: MergeRule
        """

        length = len(sorted_checked_rules)
        rule_range = range(0, length)

        # set up O(1) access to indices for the second loop in O(n) for # of rules
        indices_map = {}
        for index in rule_range:
            compat_result = sorted_checked_rules[index]
            indices_map[compat_result.rule_class_name()] = index

        # rules with higher indices (activated "later") get priority
        merged_rule = None
        for index in rule_range:
            compat_result = sorted_checked_rules[index]
            ko = False
            rule_index = indices_map[compat_result.rule_class_name()]
            # this looks like O(n^2), and it is for the rule graph, but it's O(n) for specs:
            for incompat_rcn in compat_result.incompatible_rule_class_names():
                incompat_index = indices_map[incompat_rcn]
                if incompat_index > rule_index:
                    ko = True
                    break
            if not ko:
                if merged_rule is None:
                    merged_rule = compat_result.rule()
                else:
                    merged_rule = merged_rule.merge(compat_result.rule())
        return merged_rule
