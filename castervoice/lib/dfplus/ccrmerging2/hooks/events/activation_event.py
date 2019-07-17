from castervoice.lib.dfplus.ccrmerging2.hooks.events.base_event import BaseHookEvent


class RuleActivationEvent(BaseHookEvent):
    def __init__(self, rule_class_name, active):
        super("activation")
        self.rule_class_name = rule_class_name
        self.active = active
