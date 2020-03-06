from castervoice.lib.ctrl.mgr.validation.details.base_validator import BaseDetailsValidator


class FunctionContextDetailsValidator(BaseDetailsValidator):

    '''
    Validates any Function Context Details
    '''
    def validate(self, details):
        invalidations = []
        if details.function_context is not bool:
                invalidations.append("Function Context must return a bool value")

        return None if len(invalidations) == 0 else ", ".join(invalidations)