from castervoice.lib.merge.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class RulesLoadedEvent(BaseHookEvent):
    def __init__(self, rules=None):
        super(RulesLoadedEvent, self).__init__(EventType.RULES_LOADED)
        self.rules = rules
