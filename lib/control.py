from dragonfly import RecognitionHistory, Grammar
from dragonfly.timer import _Timer

from lib import settings


MULTI_CLIPBOARD = {}
STICKY_LIST = []

DICTATION_CACHE = RecognitionHistory(20)
DICTATION_CACHE.register()
PRESERVED_CACHE = None

TIMER_MANAGER = _Timer(1)

RECORDED_MACROS_GRAMMAR = Grammar("recorded_macros")
ALIASES_GRAMMAR = Grammar("aliases")

def print_startup_message():
    print "*- Starting " + settings.SOFTWARE_NAME + " -*"

class DependencyMan():
    def __init__(self):
        self.list = [("natlink", None, ["Auto-Command", "SelectiveAction"], "http://sourceforge.net/projects/natlink"),
                   ("PIL", None, ["Legion"], "https://pypi.python.org/pypi/Pillow"),
                   ("win32ui", "pywin32", ["very many essential"], "http://sourceforge.net/projects/pywin32"),
                   ("psutil", None, ["Reboot", "HMC Cleanup"], "http://pythonhosted.org/psutil")]
        warnings = 0
        for dep in self.list:
            is_win32ui = dep[0] == "win32ui"
            try:
                exec("import " + dep[0])
            except Exception:
                if not dep[0] in settings.SETTINGS["one time warnings"]:
                    warnings += 1
                    settings.SETTINGS["one time warnings"][dep[0]] = True
                    urgency = "You can get it at " if is_win32ui else "If you wish to use those features, you can get it at "
                    print "\n" + dep[0] + " is required for ", dep[2], " features. " + urgency + dep[3] + "\n"
            else:
                name = dep[0] if not is_win32ui else dep[1]
                exec("self." + name.upper() + "=True")
        if warnings > 0:
            settings.save_config()

    NATLINK = False
    PIL = False
    PYWIN32 = False
    PSUTIL = False
    
print_startup_message()
DEP = DependencyMan()



