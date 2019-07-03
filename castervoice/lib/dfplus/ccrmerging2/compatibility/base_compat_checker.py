'''
Need to abandon the MergeRule ID system and caching
results if the same rule can be reloaded repeatedly.
Instead, this stateless checker will do comparisons
on the fly. Also, there is no such thing as "merge
time" anymore. It's always what legacy Caster called
"boot time" now.
'''
from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult
class BaseCompatibilityChecker(object):
    
    '''
    current_rules: an iterable of currently "active" rules
    new_rule: the newcomer, needs to be checked against the others
    
    This method should always return a CompatibilityResult
    '''
    def compatibility_check(self, current_rules, new_rule):
        return CompatibilityResult(False, ["use impl, not base checker"])