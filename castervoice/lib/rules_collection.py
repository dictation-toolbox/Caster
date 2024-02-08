'''
Collection of rules that are merged into a CCR grammar.
'''
_RULES = None


class RulesCollection:

    def __init__(self):
        self._rules = []

    def update(self, rules=None):
        self._rules = rules

    def serialize(self):
        rules = []
        for rule in self._rules:
            klass = rule.get_rule_class()
            instance = rule.get_rule_instance()
            mapping = instance._smr_mapping if '_smr_mapping' in instance.__dict__ else klass.mapping
            specs = sorted(["{}::{}".format(x, mapping[x]) for x in mapping])
            rules.append({
                'name': rule.get_rule_class_name(),
                'specs': specs
            })
        return [{'name': 'ccr', 'rules': rules}]


def get_instance():
    global _RULES
    if _RULES is None:
        _RULES = RulesCollection()
    return _RULES
