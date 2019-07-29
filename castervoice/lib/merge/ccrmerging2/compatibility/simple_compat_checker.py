from castervoice.lib.merge.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.merge.ccrmerging2.compatibility.compat_result import CompatibilityResult

'''
This compatibility checker mostly works the way Caster's legacy checker did:
it looks for a single incompatibility and then returns early. This has
the benefit of being faster than DetailCompatibilityChecker.
'''


class SimpleCompatibilityChecker(BaseCompatibilityChecker):

    def _check(self, mergerules):
        results = []
        specs_set = set()
        for new_rule in mergerules:
            new_specs = new_rule.mapping_copy().keys()
            incompatible_spec = self._find_first_incompatible_spec(specs_set, new_specs)
            if incompatible_spec is not None:
                results.append(CompatibilityResult(new_rule, False, [incompatible_spec]))
            else:
                results.append(CompatibilityResult(new_rule, True))
                specs_set.update(new_specs)
        return results

    def _find_first_incompatible_spec(self, specs_set, new_specs):
        for new_spec in new_specs:
            if new_spec in specs_set:
                return new_spec
        return None
