from castervoice.lib import printer
from castervoice.lib.dfplus.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.dfplus.ccrmerging2.hooks.events.event_types import EventType


class PrinterHook(BaseHook):
    """
    Copying this into the .caster dir enables printing of rule de/activation.
    """

    def __init__(self):
        super(EventType.ACTIVATION)

    def run(self, event):
        state = "active" if event.active else "inactive"
        printer.out("The rule {} was set to {}.".format(event.rule_class_name, state))


def get_hook():
    return PrinterHook()
