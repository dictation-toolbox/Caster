class CompatibilityResult(object):
    def __init__(self, mergerule, incompatible_rule_class_names=[]):
        self._mergerule = mergerule
        self._incompatible_rule_class_names = incompatible_rule_class_names

    def rule(self):
        return self._mergerule

    def is_compatible(self):
        return len(self._incompatible_rule_class_names) > 0

    def incompatible_rule_class_names(self):
        return list(self._incompatible_rule_class_names)
