class RulesEnabledDiff(object):
    def __init__(self, newly_enabled, newly_disabled):
        self.newly_enabled = list(newly_enabled)
        self.newly_disabled = set(newly_disabled)
