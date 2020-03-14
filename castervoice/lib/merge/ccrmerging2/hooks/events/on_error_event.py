from castervoice.lib.merge.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class OnErrorEvent(BaseHookEvent):
    def __init__(self):
        super(OnErrorEvent, self).__init__(EventType.ON_ERROR)
        