from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.validation.details.base_validator import BaseDetailsValidator


class AppCCRDetailsValidator(BaseDetailsValidator):

    '''
    Validates any CCR (APP-type) Details
    '''
    def validate(self, details):
        invalidations = []
        if details.declared_ccrtype == CCRType.APP:
            if details.executable is None:
                invalidations.append("ccr app types must have 'executable'")

        return None if len(invalidations) == 0 else ", ".join(invalidations)
