import castervoice.lib.rules_collection
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class RulesLoadedHook(BaseHook):
    def __init__(self):
        super(RulesLoadedHook, self).__init__(EventType.RULES_LOADED)

    def get_pronunciation(self):
        return "rules loaded"

    def run(self, event_data):
        castervoice.lib.rules_collection.get_instance().update(event_data.rules)


def get_hook():
    return RulesLoadedHook
