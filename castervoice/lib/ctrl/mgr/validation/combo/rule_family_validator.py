from dragonfly import MappingRule

from castervoice.lib.ctrl.mgr.validation.combo.base_combo_validator import BaseComboValidator
from castervoice.lib.merge.mergerule import MergeRule


class RuleFamilyValidator(BaseComboValidator):

    def validate(self, rule, details):
        invalidations = []
        if isinstance(rule, MappingRule) and details.declared_ccrtype is not None:
            invalidations.append("MappingRules must not have a ccrtype")
        if isinstance(rule, MergeRule) and details.declared_ccrtype is None:
            invalidations.append("MergeRules must have a ccrtype")
        return None if len(invalidations) == 0 else ", ".join(invalidations)
