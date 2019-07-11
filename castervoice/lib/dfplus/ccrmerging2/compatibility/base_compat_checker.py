from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult

'''
Need to abandon the MergeRule ID system and caching
results if the same rule can be reloaded repeatedly.
Instead, this stateless checker will do comparisons
on the fly. Also, there is no such thing as "merge
time" anymore. It's always what legacy Caster called
"boot time" now.
'''


class BaseCompatibilityChecker(object):
    '''
    Do not override this. 
    The parameter 'mergerules' should be a sorted iterable of MergeRules. 
    '''

    def compatibility_check(self, mergerules):
        return self._check(mergerules)

    '''
    Override this.
    This method should always return a CompatibilityResult array.
    '''

    def _check(self, mergerules):
        [CompatibilityResult(None, False, [])]
