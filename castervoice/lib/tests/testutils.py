from dragonfly.actions.action_pause import Pause
from dragonfly.actions.action_playback import Playback
from dragonfly.actions.action_startapp import BringApp
from dragonfly.actions.action_waitwindow import WaitWindow

from castervoice.lib import context
from castervoice.lib.actions import Key, Text

#     get_notepad()
#     notepad_message("\nStarting Tests")
#     notepad_message("\nPlease Do Not Close Notepad")
#     for i in range(0, 3): notepad_message("\n.", 25)
#     get_output()


class MockAlternative(object):
    '''mocks dragonfly data'''

    def __init__(self, *words):
        self.results = tuple([(word, 0) for word in words])


def get_notepad():
    action = BringApp("notepad.exe") + WaitWindow(executable="notepad.exe", timeout=15)
    action.execute()


def notepad_message(message, sec100=100):
    action = Text(message) + Pause(str(sec100))
    action.execute()


def get_output():
    get_notepad()
    Key("c-a").execute()
    output = context.read_selected_without_altering_clipboard(True)[1]
    Key("backspace").execute()
    return output


def get_playback(commands):
    '''commands is an array of strings'''
    playback_tuples = [(utterance.split(" "), 1.0) for utterance in commands]
    return Playback(playback_tuples)
