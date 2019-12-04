class FullContentSet(object):
    """
    Initial content, loaded once when Caster starts.
    """
    def __init__(self, rules, transformers, hooks):
        self.rules = rules
        self.transformers = transformers
        self.hooks = hooks
