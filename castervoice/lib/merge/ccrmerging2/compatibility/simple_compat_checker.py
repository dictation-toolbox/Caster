from castervoice.lib.merge.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.merge.ccrmerging2.compatibility.compat_result import CompatibilityResult


class SimpleCompatibilityChecker(BaseCompatibilityChecker):
    """
    Does a simple compatibility computation,
    eliminates incompatible rules using the
    provided order.
    """

    def compatibility_check(self, mergerules):
        all_specs = set()
        results = []

        for rule in reversed(list(mergerules)):
            rule_specs = frozenset(rule.get_mapping().keys())
            if SimpleCompatibilityChecker._intersection_exists(rule_specs, all_specs):
                continue
            all_specs.update(rule_specs)
            results.append(CompatibilityResult(rule, frozenset()))

        return list(reversed(results))

    @staticmethod
    def _intersection_exists(set_a, set_b):
        """
        Lazy/fast intersection.
        """
        for a in set_a:
            if a in set_b:
                return True
        return False
