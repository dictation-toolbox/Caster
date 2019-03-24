from dragonfly import Function, Pause
from castervoice.lib import context, control
from castervoice.lib.actions import Text, Key

_NEXUS = control.nexus()


def Store():
    def temp_store():
        _, text = context.read_selected_without_altering_clipboard(False)
        _NEXUS.temp = text if text else ""
    return Function(temp_store)

def Retrieve(action_if_no_text="", action_if_text=""):
    def temp_retrieve(action_if_no_text, action_if_text):
        Text(_NEXUS.temp).execute()
        if _NEXUS.temp:
            Key(action_if_text).execute()
        else:
            Key(action_if_no_text).execute()
    return Function(temp_retrieve, action_if_no_text=action_if_no_text, action_if_text=action_if_text)

