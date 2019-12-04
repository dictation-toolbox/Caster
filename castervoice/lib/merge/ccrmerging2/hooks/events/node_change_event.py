from castervoice.lib.merge.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class NodeChangeEvent(BaseHookEvent):
    def __init__(self, tree_name, active_path, new_specs):
        super(NodeChangeEvent, self).__init__(EventType.NODE_CHANGE)
        self.tree_name = tree_name
        self.active_path = active_path
        self.new_specs = new_specs
