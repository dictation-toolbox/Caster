class CompatibilityResult(object):
    def __init__(self, mergerule, compatible, incompatible_rules=[]):
        self._mergerule = mergerule
        self._compatible = compatible
        self._incompatible_rules = incompatible_rules

    def rule(self):
        return self._mergerule

    def is_compatible(self):
        return self._compatible

    def incompatible_rules(self):
        return list(self._incompatible_rules)
