'''
Created on Jun 23, 2019

@author: synkarius
'''


class RuleDetails(object):
    def __init__(self, rule_path=None, name=None, executable=None, grammar_name=None,
                 enabled=True, ccrtype=None, context=None):
        # TODO: some validations of rule_path/name/executable/grammar_name/crr configurations, think this through

        self.rule_path = rule_path
        self.name = name
        self.executable = executable
        self.grammar_name = grammar_name
        self.enabled = enabled
        self.declared_ccrtype = ccrtype
        self.context = context
