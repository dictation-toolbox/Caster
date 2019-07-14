class ManagedRule(object):

    def __init__(self, rule_class, details, grammar=None):
        self.rule_class = rule_class
        self.details = details
        self.grammar = grammar