class MergeResult(object):

    def __init__(self, ccr_rules_and_contexts, all_rule_class_names, rules_enabled_diff):
        """
        :param ccr_rules_and_contexts: 1-n RepeatRules and 0-n AppContexts
        :param all_rule_class_names: list of str
        :param rules_enabled_diff: RulesEnabledDiff
        """
        self.ccr_rules_and_contexts = ccr_rules_and_contexts
        self.all_rule_class_names = all_rule_class_names
        self.rules_enabled_diff = rules_enabled_diff
