class BaseRuleSetSorter(object):
    """
    When multiple active rules get edited at the same time and
    reloaded, there is no such thing anymore as the
    "currently active rules" and the "new rule". It's a set of
    active rules which need to be merged together in some kind
    of deterministic order. This behavior should be customizable.
    Hence ruleset sorters.
    """

    def sort_rules(self, rules):
        return list(rules)
