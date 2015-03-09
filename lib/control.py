from dragonfly import RecognitionHistory, Grammar
from dragonfly.timer import _Timer

from lib import settings


MULTI_CLIPBOARD = {}
STICKY_LIST = []

DICTATION_CACHE = RecognitionHistory(10)
DICTATION_CACHE.register()
PRESERVED_CACHE = None

TIMER_MANAGER = _Timer(1)

RECORDED_MACROS_GRAMMAR = Grammar("recorded_macros")
HOOK_MANAGER = None

def print_startup_message():
    print "*- Starting " + settings.SOFTWARE_NAME + " -*"

class DependencyMan():
    def __init__(self):
        self.list = [("pyHook", None, ["Auto-Command (external mode)"], "http://sourceforge.net/projects/pyhook"),
                   ("natlink", None, ["Auto-Command", "SelectiveAction"], "http://sourceforge.net/projects/natlink"),
                   ("PIL", None, ["Legion"], "https://pypi.python.org/pypi/Pillow"),
                   ("win32ui", "pywin32", ["very many essential"], "http://sourceforge.net/projects/pywin32"),
                   ("psutil", None, ["Reboot", "HMC Cleanup"], "http://pythonhosted.org/psutil")]
        for dep in self.list:
            is_win32ui = dep[0] == "win32ui"
            try:
                exec("import " + dep[0])
            except Exception:
                urgency = "You can get it at " if is_win32ui else "If you wish to use those features, you can get it at "
                print "\n" + dep[0] + " is required for ", dep[2], " features. " + urgency + dep[3] + "\n"
            else:
                name = dep[0] if not is_win32ui else dep[1]
                exec("self." + name.upper() + "=True")
    
    PYHOOK = False
    NATLINK = False
    PIL = False
    PYWIN32 = False
    PSUTIL = False
    
print_startup_message()
DEP = DependencyMan()



