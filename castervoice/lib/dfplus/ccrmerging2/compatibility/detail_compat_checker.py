from castervoice.lib.dfplus.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult

'''
This compatibility checker reports back both the compatibility
verdict, and the conflicting specs if there is incompatibility.
It is slower than SimpleCompatibilityChecker but can be used to 
enable alternate merge collision strategies. 
'''
class DetailCompatibilityChecker(BaseCompatibilityChecker):
    
    def compatibility_check(self, current_rules, new_rule):
        ''''''
        conflicting_specs = set()
        for current_rule in current_rules:
            conflicting_specs |= self._check_rule_pair(current_rule, new_rule)
        return CompatibilityResult(len(conflicting_specs) > 0, conflicting_specs)
            
    
    def _check_rule_pair(self, mergerule1, mergerule2):
        conflicting_specs = set()
        specs1 = mergerule1.mapping_copy().keys()
        specs2 = mergerule2.mapping_copy().keys() 
        for spec in specs1:
            if spec in specs2:
                conflicting_specs.add(spec)
        return conflicting_specs