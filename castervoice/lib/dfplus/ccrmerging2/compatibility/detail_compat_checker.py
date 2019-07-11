from castervoice.lib.dfplus.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult

'''
This compatibility checker reports back both the compatibility
verdict, and the conflicting specs if there is incompatibility.
It is slower than SimpleCompatibilityChecker but can be used to 
enable alternate merge collision strategies. 
'''


class DetailCompatibilityChecker(BaseCompatibilityChecker):
    '''
    If 'count_against_all' is true, incompatibility for a given
    rule will be calculated against all prior rules, whether or not
    they were compatible. This may make sense for some compatibility
    scenarios, but the default behavior will be to only check
    compatibility against prior non-conflicting rules.
    '''

    def __init__(self, count_against_all=False):
        self._count_against_all = count_against_all

    def _check(self, mergerules):
        results = []
        specs_set = set()
        for new_rule in mergerules:
            new_specs = new_rule.mapping_copy().keys()
            incompatible_specs = self._find_all_incompatible_specs(specs_set, new_specs)
            is_compatible = len(incompatible_specs) == 0
            result = CompatibilityResult(new_rule, is_compatible, incompatible_specs)
            results.append(result)
            if is_compatible or self._count_against_all:
                specs_set.update(new_specs)
        return results

    def _find_all_incompatible_specs(self, specs_set, new_specs):
        results = []
        for new_spec in new_specs:
            if new_spec in specs_set:
                results.append(new_spec)
        return results
