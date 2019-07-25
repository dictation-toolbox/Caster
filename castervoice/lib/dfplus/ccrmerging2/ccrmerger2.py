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
        TODO: it is in fact NOT rule classes being passed in, but ManagedRules
        ... this is good. This method needs to
        A) for each contexted rule in the sorted list, make a copy of the list with no other contexted rules in it
            (also need a no-contexts copy)
        B) compat-check each of these lists
        c) merge each of these lists and then
            c-1) add a "not-any" context to the main merged rule
            c-2) add an "only" (normal) context to each of the contexted merged rules

        does 4-step merging, runs examples, returns a merged rule
        :param rule_classes: collection of MergeRule
        :return: MergeRule
        """

        # TODO: make sure that test instantiations are done even on selfmod rules before this
        instantiated_rules = [r() for r in rule_classes]

        transformed_rules = []
        for rule in instantiated_rules:
            for transformer in self._transformers:
                rule = transformer.get_transformed_rule(rule)
            transformed_rules.append(rule)

        sorted_rules = self._rule_sorter.sort_rules(transformed_rules)

        compat_results = [self._compatibility_checker.compatibility_check(r) for r in sorted_rules]



