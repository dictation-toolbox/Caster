'''
Initial content, loaded once when Caster starts.
'''
class FullContentSet(object):
    def __init__(self, rules, transformers, hooks):
        self.rules = rules
        self.transformers = transformers
        self.hooks = hooks