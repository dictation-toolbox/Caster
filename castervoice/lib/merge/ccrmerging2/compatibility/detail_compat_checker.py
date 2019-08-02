from castervoice.lib.merge.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.merge.ccrmerging2.compatibility.compat_result import CompatibilityResult


class DetailCompatibilityChecker(BaseCompatibilityChecker):
    """
    This compatibility checker reports back both the compatibility
    verdict, and the conflicting specs if there is incompatibility.
    It is slower than SimpleCompatibilityChecker but can be used to
    enable alternate merge collision strategies.
    """

    def __init__(self, count_against_all=False):
        """
        If 'count_against_all' is true, incompatibility for a given
        rule will be calculated against all prior rules, whether or not
        they were compatible. You want this False in case you have a
        scenario like:
        [A, B, C]
        A -> B = False
        B -> C = False
        C -> A = True
        If B's specs get dumped into the "pool" despite the fact that B
        will be KO'd by A, C will get KO'd by the "ghost" of B, even though
        it could have coexisted with A.

        :param count_against_all: boolean
        """
        self._count_against_all = count_against_all

    def compatibility_check(self, mergerules):
        results = []
        specs_to_rules = {}
        for rule in mergerules:
            rule_specs = rule.mapping_copy().keys()
            incompatible_rules = self._find_all_incompatible_rules(specs_to_rules, rule_specs)

            is_compatible = len(incompatible_rules) == 0

            result = CompatibilityResult(rule, is_compatible, incompatible_rules)

            results.append(result)

            if is_compatible or self._count_against_all:
                self._invert_mapping(rule, rule_specs, specs_to_rules)
        return results

    def _invert_mapping(self, rule, rule_specs, specs_to_rules):
        """
        Given a rule and its specs, associates each spec with its rule in
        'specs_to_rules'. This is so that later on, if there is a spec conflict,
        it's easy to pinpoint the rules it came from.
        """

        for spec in rule_specs:
            if spec not in specs_to_rules:
                specs_to_rules[spec] = []
            specs_to_rules[spec].append(rule)

    def _find_all_incompatible_rules(self, specs_to_rules, rule_specs):
        results = []
        for rule_spec in rule_specs:
            if rule_spec in specs_to_rules:
                results.extend(specs_to_rules[rule_spec])
        return results
