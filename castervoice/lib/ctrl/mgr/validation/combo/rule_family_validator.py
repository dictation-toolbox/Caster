from dragonfly import MappingRule

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.combo.base_combo_validator import BaseComboValidator
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class RuleFamilyValidator(BaseComboValidator):
    """
    Non-MappingRules are not handled by Caster.
    MappingRules must not have ccrtypes.
    MergeRules must have ccrtypes.
    SelfModifyingRules can have ccrtypes.
    CCR SelfModifyingRules must use correct type.
    Nothing else is allowed to use SelfModifyingRules CCR type.
    Function Context must not have CCRType `GLOBAL` or `SELFMOD`
    """

    def validate(self, rule, details):
        mapping = isinstance(rule, MappingRule)
        merge = isinstance(rule, MergeRule)
        selfmod = isinstance(rule, BaseSelfModifyingRule)
        has_ccrtype = details.declared_ccrtype is not None
        has_function_context = details.function_context is not None

        invalidations = []

        if not mapping:
            invalidations.append("non-MappingRule rules are not handled")
        elif mapping and not merge and has_ccrtype:
            invalidations.append("MappingRules must not have a ccrtype")
        elif merge and not selfmod:
            if not has_ccrtype:
                invalidations.append("MergeRules must have a ccrtype")
            elif details.declared_ccrtype == CCRType.SELFMOD:
                invalidations.append("non-SelfModifyingRules must not use CCRType.SELFMOD")
        elif selfmod and has_ccrtype and details.declared_ccrtype != CCRType.SELFMOD:
            invalidations.append("CCR SelfModifyingRules must use CCRType.SELFMOD")
        if has_function_context and has_ccrtype:
            if details.declared_ccrtype == CCRType.GLOBAL or details.declared_ccrtype == CCRType.SELFMOD:
                invalidations.append("Function Context cannot be used with `CCRType.GLOBAL` or `CCRType.SELFMOD`")


        return None if len(invalidations) == 0 else ", ".join(invalidations)
