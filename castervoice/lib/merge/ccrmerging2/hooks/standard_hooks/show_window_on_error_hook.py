from castervoice.lib import settings, textformat
from castervoice.lib.merge.ccrmerging2.hooks.base_hook import BaseHook
from castervoice.lib.merge.ccrmerging2.hooks.events.event_types import EventType
from castervoice.lib import printer

import six
from dragonfly import get_current_engine
from dragonfly.windows.window import Window

def show_window():
    title = None
    engine = get_current_engine().name
    if engine == 'natlink':
        import natlinkstatus  # pylint: disable=import-error
        status = natlinkstatus.NatlinkStatus()
        if status.NatlinkIsEnabled() == 1:
            if six.PY2:
               title = "Messages from Python Macros"
            else: 
                title= "Messages from Natlink"
        else:
            title = "Caster: Status Window"
    if engine != 'natlink':
        title = "Caster: Status Window"
    windows = Window.get_matching_windows(title=title)
    if windows:
        windows[0].set_foreground()


class ShowStatusWindowOnErrorHook(BaseHook):
    def __init__(self):
        super(ShowStatusWindowOnErrorHook, self).__init__(EventType.ON_ERROR)

    def get_pronunciation(self):
        return "show status error"

    def run(self, event_data):
        show_window()

def get_hook():
    return ShowStatusWindowOnErrorHook
