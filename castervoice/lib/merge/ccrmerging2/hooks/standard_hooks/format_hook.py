from castervoice.lib import settings, textformat
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType


def _apply_format(rule_pronunciation):
    if rule_pronunciation in settings.SETTINGS["formats"]:
        if 'text_format' in settings.SETTINGS["formats"][rule_pronunciation]:
            cap, spacing = settings.SETTINGS["formats"][rule_pronunciation]['text_format']
            textformat.format.set_text_format(cap, spacing)
        else:
            textformat.format.clear_text_format()
        if 'secondary_format' in settings.SETTINGS["formats"][rule_pronunciation]:
            cap, spacing = settings.SETTINGS["formats"][rule_pronunciation]['secondary_format']
            textformat.secondary_format.set_text_format(cap, spacing)
        else:
            textformat.secondary_format.clear_text_format()
    else:
        textformat.format.clear_text_format()
        textformat.secondary_format.clear_text_format()


class FormattingHook(BaseHook):

    def __init__(self):
        super(FormattingHook, self).__init__(EventType.ACTIVATION)

    def get_pronunciation(self):
        return "formatting"

    def run(self, event_content):
        pronunciation = event_content["pronunciation"]
        _apply_format(pronunciation)


def get_hook():
    return FormattingHook
