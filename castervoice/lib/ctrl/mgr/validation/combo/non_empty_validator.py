from castervoice.lib.ctrl.mgr.validation.combo.base_combo_validator import BaseComboValidator
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule


class RuleNonEmptyValidator(BaseComboValidator):
    """
    Any static rule should have at least one command to start.

    Some selfmod rules don't have any rules the first time they
    are instantiated, but then immediately fill in and "reboot"
    themselves.

    SikuliRule is not a selfmod rule, but it kind of works like
    one, so it is also exempted.
    """

    def validate(self, rule, details):
        invalidations = []
        if len(rule.mapping) == 0 and not self._rule_is_exempt(rule):
            invalidations.append("rules must have at least one command")
        return None if len(invalidations) == 0 else ", ".join(invalidations)

    def _rule_is_exempt(self, rule):
        selfmod = isinstance(rule, BaseSelfModifyingRule)
        sikuli = rule.__class__.__name__ == "SikuliRule"
        return selfmod or sikuli
