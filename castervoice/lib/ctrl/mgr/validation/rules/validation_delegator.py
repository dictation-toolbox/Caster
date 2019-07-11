from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.rules.composite_validator import CompositeValidator
from castervoice.lib.ctrl.mgr.validation.rules.context_validator import HasContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.mergerule_validator import IsMergeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.no_context_validator import HasNoContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.not_noderule_validator import NotNodeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.selfmod_validator import SelfModifyingRuleValidator


class CCRValidationDelegator(object):
    def __init__(self):
        self._global_validator = CompositeValidator([
            IsMergeRuleValidator(),
            HasNoContextValidator()
        ])
        self._app_validator = HasContextValidator()

        self._selfmod_validator = CompositeValidator([
            SelfModifyingRuleValidator(),
            NotNodeRuleValidator()
        ])

    '''
    if it has a context, it's an app rule
    else if its a selfmod, then selfmod
    else global
    '''

    def validate(self, rule, declared_ccrtype):
        error_message = None
        if declared_ccrtype == CCRType.GLOBAL:
            error_message = self._global_validator.validate(rule)
        elif declared_ccrtype == CCRType.APP:
            error_message = self._app_validator.validate(rule)
        elif declared_ccrtype == CCRType.SELFMOD:
            error_message = self._selfmod_validator.validate(rule)
        return error_message
