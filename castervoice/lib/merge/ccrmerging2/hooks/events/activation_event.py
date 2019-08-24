from castervoice.lib.merge.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class RuleActivationEvent(BaseHookEvent):
    def __init__(self, rule_class_name, active):
        super(RuleActivationEvent, self).__init__(EventType.ACTIVATION)
        self.rule_class_name = rule_class_name
        self.active = active
