class BaseDetailsValidator(object):

    '''
    Details validation, vs rules validation, is about detecting invalid configurations.
    There is no need to check anything here about how the rule matches the configuration.
    Details validators are only about the details objects not themselves being valid.
    
    Takes a Details, returns error messages if certain kind of invalid configuration
    is contained within it.
    '''
    def validate(self, details):
        return None

'''
class RuleDetails(object):
    def __init__(self, rule_path=None, name=None, executable=None, grammar_name=None,
                 enabled=True, ccrtype=None):
        # TODO: some validations of rule_path/name/executable/grammar_name/crr configurations, think this through

        self.rule_path = rule_path
        self.name = name
        self.executable = executable
        self.grammar_name = grammar_name
        self.enabled = enabled
        self.declared_ccrtype = ccrtype

(IS A CCR APP GRAMMAR)
if declared_ccrtype is app then
    must have executable (=> turns into context)
    


"RDP mode" (not recommended):
if settings.SETTINGS["miscellaneous"]["rdp_mode"] and rdp:
    then add it as a ccr global rule, fuck all about what kind of rule it actually is

'''