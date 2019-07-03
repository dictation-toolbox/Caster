from castervoice.lib.dfplus.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult

'''
This compatibility checker mostly works the way Caster's legacy checker did:
it looks for a single incompatibility and then returns early. This has
the benefit of being faster than DetailCompatibilityChecker.
'''
class SimpleCompatibilityChecker(BaseCompatibilityChecker):
    
    def compatibility_check(self, current_rules, new_rule):
        new_specs = new_rule.mapping_copy().keys()
        for current_rule in current_rules:
            current_rule_specs = current_rule.mapping_copy().keys()
            for new_spec in new_specs:
                if new_spec in current_rule_specs:
                    return CompatibilityResult(False)
        return CompatibilityResult(True)