from castervoice.lib import printer
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


class PrinterHook(BaseHook):

    def __init__(self):
        super(PrinterHook, self).__init__(EventType.ACTIVATION)

    def get_pronunciation(self):
        return "printer"

    def run(self, event):
        state = "active" if event.active else "inactive"
        printer.out("The rule {} was set to {}.".format(event.rule_class_name, state))


def get_hook():
    return PrinterHook
