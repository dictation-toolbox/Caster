from castervoice.lib.dfplus.ccrmerging2.compatibility.compat_result import CompatibilityResult


class BaseCompatibilityChecker(object):

    def compatibility_check(self, mergerules):
        """
        Do not override this.

        :param mergerules: a sorted iterable of MergeRules
        :return:
        """
        return self._check(mergerules)

    def _check(self, mergerules):
        """
        Override this.
        This method should always return a CompatibilityResult array.

        :param mergerules:
        :return:
        """
        [CompatibilityResult(None, False, [])]
