from dragonfly.grammar.elements import RuleRef, Alternative, Repetition
from dragonfly.grammar.rule_compound import CompoundRule
from dragonfly import FuncContext
from castervoice.lib.const import CCRType
from castervoice.lib.context import AppContext
from castervoice.lib.ctrl.mgr.rules_enabled_diff import RulesEnabledDiff
from castervoice.lib.merge.ccrmerging2.merge_result import MergeResult


class CCRMerger2(object):
    _ORIGINAL = "original"
    _SEQ = "caster_base_sequence"
    _TERMINAL = "terminal"

    def __init__(self, transformers_runner, compatibility_checker, merging_strategy, max_repetitions, smr_configurer):
        """
        5-Step Merge Process
        ====================
        1. Run all transformers over all rules.
        2. Use a rule set sorter to sort rules.
        3. Use a compatibility checker to calculate incompatibility.
        4. Pass the transformed/sorted/checked rules to the merging strategy.
        5. Use the old trick from _multiedit.py to turn a MappingRule into a CCR rule.
        ====================
        :param transformers_runner: runs Transformers on generated rules
        :param compatibility_checker: BaseCompatibilityChecker impl
        :param merging_strategy: BaseMergingStrategy impl
        :param max_repetitions
        :param smr_configurer
        """
        self._transformers_runner = transformers_runner
        self._compatibility_checker = compatibility_checker
        self._merging_strategy = merging_strategy
        #
        self._sequence = 0
        self._max_repetitions = int(max_repetitions)
        self._smr_configurer = smr_configurer

    def merge_rules(self, managed_rules, rule_sorter):
        """
        :param managed_rules: list of ManagedRules
        :param rule_sorter: BaseRuleSetSorter impl
        :return: MergeResult
        """
        pre_merge_rcns = [mr.get_rule_class_name() for mr in managed_rules]
        rcns_to_details = CCRMerger2._rule_details_dict(managed_rules)
        instantiated_rules = self._instantiate_and_configure_rules(managed_rules)

        # 1: run transformers over rules
        transformed_rules = self._run_transformers(instantiated_rules, rcns_to_details)
        # 2: sort rules into the order they'll be merged in
        sorted_rules = rule_sorter.sort_rules(transformed_rules)
        # 3: compute compatibility results for all rules vs all rules in O(n) for total specs
        compat_results = self._compatibility_checker.compatibility_check(sorted_rules)
        # 4: create one merged rule for each context, plus the no-contexts merged rule
        app_crs, non_app_crs = self._separate_app_rules(compat_results, rcns_to_details)
        merged_rules = self._create_merged_rules(app_crs, non_app_crs)
        # 5: turn the merged rules into repeat rules
        repeat_rules = [self._create_repeat_rule(merged_rule) for merged_rule in merged_rules]
        contexts = CCRMerger2._create_contexts(app_crs, rcns_to_details)

        rules_and_contexts = list(zip(repeat_rules, contexts))
        enabled_ordered_rcns = [cr.rule_class_name() for cr in compat_results]
        diff = CCRMerger2._calculate_post_merge_diff(pre_merge_rcns, enabled_ordered_rcns)
        return MergeResult(rules_and_contexts, enabled_ordered_rcns, diff)

    @staticmethod
    def _calculate_post_merge_diff(pre_merge_rcns, post_merge_rcns):
        """
        Given list of pre-merge rcns and post-merge rcns, calculates which rules
        were enabled and which were disabled by the merge.

        :param pre_merge_rcns: iterable
        :param post_merge_rcns: iterable
        :return: RulesEnabledDiff
        """
        set_pre = frozenset(pre_merge_rcns)
        set_post = frozenset(post_merge_rcns)
        newly_enabled = list()  # must remain ordered
        newly_disabled = set()  # order doesn't matter

        for rcn in pre_merge_rcns:
            if rcn not in set_post:
                newly_disabled.add(rcn)
        for rcn in post_merge_rcns:
            if rcn not in set_pre:
                newly_enabled.append(rcn)

        return RulesEnabledDiff(newly_enabled, newly_disabled)

    def _instantiate_and_configure_rules(self, managed_rules):
        instantiated_rules = []
        for mr in managed_rules:
            mergerule = mr.get_rule_instance()
            # smr configurer only configures selfmodrules, but checks all
            self._smr_configurer.configure(mergerule)
            instantiated_rules.append(mergerule)
        return instantiated_rules

    def _run_transformers(self, instantiated_rules, rcns_to_details):
        transformed_rules = []
        for rule in instantiated_rules:
            has_exclusion = rcns_to_details[rule.get_rule_class_name()].transformer_exclusion
            if not has_exclusion:
                rule = self._transformers_runner.transform_rule(rule)
            transformed_rules.append(rule)
        return transformed_rules

    def _separate_app_rules(self, compat_results, rcns_to_details):
        """
        Given M non-app rules and N app rules, we want to produce
        N+1 merged rules, where one of them has no app rules and the rest
        each have one app rule.
        """
        app_crs = []
        non_app_crs = []
        for cr in compat_results:
            details = rcns_to_details[cr.rule_class_name()]
            if details.declared_ccrtype == CCRType.APP:
                app_crs.append(cr)
            else:
                non_app_crs.append(cr)
        return app_crs, non_app_crs

    def _create_merged_rules(self, app_crs, non_app_crs):
        merged_rules = []
        merged_non_app_crs_rule = self._merging_strategy.merge_into_single(non_app_crs)
        if merged_non_app_crs_rule is not None:
            merged_rules.append(merged_non_app_crs_rule)
        for app_cr in app_crs:
            with_one_app = list(non_app_crs)
            with_one_app.append(app_cr)
            merged_rules.append(self._merging_strategy.merge_into_single(with_one_app))
        return merged_rules

    @staticmethod
    def _create_contexts(app_crs, rcns_to_details):
        """
        Returns a list of contexts, AppContexts based on 'executable', FuncContext, one for each
        app rule, and if more than zero app rules, the negation context for the
        global ccr rule. (Global rule should be active when none of the other
        contexts are.) If there are zero app rules, [None] will be returned
        so the result can be zipped.

        :param app_crs: list of CompatibilityResult for app rules
        :param rcns_to_details: map of {rule class name: rule details}
        :return:
        """
        contexts = []
        negation_context = None
        for cr in app_crs:
            details = rcns_to_details[cr.rule_class_name()]
            context = AppContext(executable=details.executable, title=details.title)
            if details.function_context is not None:
                funkcontext = context
                funkcontext &= FuncContext(function=details.function_context)
                contexts.append(funkcontext)
            else:
                contexts.append(context)
            if details.function_context is None:
                if negation_context is None:
                    negation_context = ~context
                else:
                    negation_context &= ~context
        contexts.insert(0, negation_context)
        return contexts

    @staticmethod
    def _rule_details_dict(managed_rules):
        """
        :param managed_rules: list of ManagedRule
        :return: dict of {class name (str): RuleDetails}
        """
        result = {}
        for managed_rule in managed_rules:
            result[managed_rule.get_rule_class_name()] = managed_rule.get_details()
        return result

    def _create_repeat_rule(self, merge_rule):
        merge_rule = merge_rule.prepare_for_merger()
        alts = [RuleRef(rule=merge_rule)]  # +[RuleRef(rule=sm) for sm in selfmod]
        single_action = Alternative(alts)
        sequence = Repetition(single_action, min=1, max=self._max_repetitions, name=CCRMerger2._SEQ)
        original = Alternative(alts, name=CCRMerger2._ORIGINAL)
        terminal = Alternative(alts, name=CCRMerger2._TERMINAL)

        class RepeatRule(CompoundRule):
            spec = "[<" + CCRMerger2._ORIGINAL + "> original] " + \
                   "[<" + CCRMerger2._SEQ + ">] " + \
                   "[terminal <" + CCRMerger2._TERMINAL + ">]"
            extras = [sequence, original, terminal]

            def _process_recognition(self, node, extras):
                _original = extras[CCRMerger2._ORIGINAL] if CCRMerger2._ORIGINAL in extras else None
                _sequence = extras[CCRMerger2._SEQ] if CCRMerger2._SEQ in extras else None
                _terminal = extras[CCRMerger2._TERMINAL] if CCRMerger2._TERMINAL in extras else None
                if _original is not None: _original.execute()
                if _sequence is not None:
                    for action in _sequence:
                        action.execute()
                if _terminal is not None: _terminal.execute()

        return RepeatRule(name=self._get_new_rule_name())

    def _get_new_rule_name(self):
        self._sequence += 1
        return "Repeater{}".format(str(self._sequence))
