class CompatibilityResult(object):
    def __init__(self, mergerule, incompatible_rule_class_names=[]):
        """
        :param mergerule: MergeRule
        :param incompatible_rule_class_names: list of strings
        """
        self._mergerule = mergerule
        self._incompatible_rule_class_names = incompatible_rule_class_names

    def rule(self):
        return self._mergerule

    def rule_class_name(self):
        return self._mergerule.get_rule_class_name()

    def is_compatible(self):
        return len(self._incompatible_rule_class_names) > 0

    def incompatible_rule_class_names(self):
        return set(self._incompatible_rule_class_names)
