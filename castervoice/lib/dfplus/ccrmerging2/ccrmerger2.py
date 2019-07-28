from dragonfly.grammar.elements import RuleRef, Alternative, Repetition
from dragonfly.grammar.rule_compound import CompoundRule

from castervoice.lib.const import CCRType


class CCRMerger2(object):

    def __init__(self, transformers, rule_sorter, compatibility_checker, merging_strategy, max_repetitions,
                 smr_configurer):
        """
        5-Step Merge Process
        ====================
        1. Run all transformers over all rules.
        2. Use a rule set sorter to sort rules.
        3. Use a compatibility checker to calculate incompatibility.
        4. Pass the transformed/sorted/checked rules to the merging strategy.
        5. Use the old trick from _multiedit.py to turn a MappingRule into a CCR rule.
        ====================
        :param transformers: collection of Transformers
        :param rule_sorter: BaseRuleSetSorter impl
        :param compatibility_checker: BaseCompatibilityChecker impl
        :param merging_strategy: BaseMergingStrategy impl
        :param max_repetitions
        :param smr_configurer
        """
        self._transformers = transformers
        self._rule_sorter = rule_sorter
        self._compatibility_checker = compatibility_checker
        self._merging_strategy = merging_strategy
        #
        self._sequence = 0
        self._max_repetitions = max_repetitions
        self._smr_configurer = smr_configurer

    def add_transformer(self, transformer):
        self._transformers.append(transformer)

    def merge(self, managed_rules):
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
        :param managed_rules: ManagedRules
        :return: MergeRule
        """
        result = []

        # TODO: something needs to happen here in the recursive version of the call
        non_app_managed_rules, app_managed_rules = self._separate_app_rules(managed_rules)
        if len(app_managed_rules) > 0:
            app_ccr_rules = self._get_app_rule_clones(non_app_managed_rules, app_managed_rules)
            result.extend(app_ccr_rules)

        instantiated_rules = [mr.get_rule_instance() for mr in non_app_managed_rules]

        # selfmodrule configuration
        for rule in instantiated_rules:
            self._smr_configurer.configure(rule)

        # 1
        transformed_rules = []
        for rule in instantiated_rules:
            for transformer in self._transformers:
                rule = transformer.get_transformed_rule(rule)
            transformed_rules.append(rule)
        # 2
        sorted_rules = self._rule_sorter.sort_rules(transformed_rules)
        # 3
        compat_results = [self._compatibility_checker.compatibility_check(r) for r in sorted_rules]
        # 4
        merged_rule = self._merging_strategy.merge(compat_results)
        # 5
        ccr_rule = self._create_repeat_rule(merged_rule)

        result.append(ccr_rule)
        '''TODO: This current setup assumes no app rules -- have to correct that, see above notes.'''
        return result

    def _separate_app_rules(self, managed_rules):
        non_app_managed_rules = []
        app_managed_rules = []
        for managed_rule in managed_rules:
            if managed_rule.details.declared_ccrtype == CCRType.APP:
                app_managed_rules.append(managed_rule)
            else:
                non_app_managed_rules.append(managed_rule)
        return non_app_managed_rules, app_managed_rules

    def _get_app_rule_clones(self, non_app_managed_rules, app_managed_rules):
        """
        TODO: for each app managed rule,
        1. add it in to a clone of the non-app list
        2. call merge() on that list
        3. hmmm.... how to return a context with each clone?

        TODO:
        HERE'S ANOTHER COMPLICATION: if you're calling merge() on each group, you'll
        also need some signal to skip checking for contexts -- a new merge() parameter which is only true from
        inside the merger

        :param non_app_managed_rules:
        :param app_managed_rules:
        :return:
        """

        return []

    def _create_repeat_rule(self, rule):
        ORIGINAL, SEQ, TERMINAL = "original", "caster_base_sequence", "terminal"
        alts = [RuleRef(rule=rule)]  # +[RuleRef(rule=sm) for sm in selfmod]
        single_action = Alternative(alts)
        sequence = Repetition(single_action, min=1, max=self._max_repetitions, name=SEQ)
        original = Alternative(alts, name=ORIGINAL)
        terminal = Alternative(alts, name=TERMINAL)

        class RepeatRule(CompoundRule):
            spec = "[<" + ORIGINAL + "> original] [<" + SEQ + ">] [terminal <" + TERMINAL + ">]"
            extras = [sequence, original, terminal]

            def _process_recognition(self, node, extras):
                original = extras[ORIGINAL] if ORIGINAL in extras else None
                sequence = extras[SEQ] if SEQ in extras else None
                terminal = extras[TERMINAL] if TERMINAL in extras else None
                if original is not None: original.execute()
                if sequence is not None:
                    for action in sequence:
                        action.execute()
                if terminal is not None: terminal.execute()

        return RepeatRule(name=self._get_new_rule_name())

    def _get_new_rule_name(self):
        self._sequence += 1
        return "Repeater{}".format(str(self._sequence))
