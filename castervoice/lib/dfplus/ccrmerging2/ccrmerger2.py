class CCRMerger2(object):

    def __init__(self, transformers, rule_sorter, compatibility_checker, merging_strategy):
        """
        4-Step Merge Process
        ====================
        1. Run all transformers over all rules.
        2. Use a rule set sorter to sort rules.
        3. Use a compatibility checker to calculate incompatibility.
        4. Pass the transformed/sorted/checked rules to the merging strategy.
        ====================
        :param transformers: collection of Transformers
        :param rule_sorter: BaseRuleSetSorter impl
        :param compatibility_checker: BaseCompatibilityChecker impl
        :param merging_strategy: BaseMergingStrategy impl
        """
        self._transformers = transformers
        self._rule_sorter = rule_sorter
        self._compatibility_checker = compatibility_checker
        self._merging_strategy = merging_strategy
        self._hooks = []

    def add_transformer(self, transformer):
        self._transformers.append(transformer)

    def add_hook(self, hook):
        self._hooks.append(hook)

    def merge(self, rule_classes):
        """
        does 4-step merging, runs hooks, returns a merged rule
        :param rule_classes: collection of MergeRule
        :return: MergeRule
        """



        pass

