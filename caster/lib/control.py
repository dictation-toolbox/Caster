from dragonfly import RecognitionHistory, Grammar
from dragonfly.timer import _Timer

from caster.lib import settings
from caster.lib.dfplus.communication import Communicator

NEXUS = None


class Nexus:
    def __init__(self):
        self._map = {}
        self._nodes_map = {"CSS": False}
        
        self.state = None
        self.clip = {}
        self.sticky = []
        self.history = RecognitionHistory(20)
        self.history.register()
        self.preserved = None
        
        self._comm = Communicator()
        self.timer = _Timer(0.025)
        
        self.dep = None
        self.intermediary = None
        
        self.macros_grammar = Grammar("recorded_macros")
        self.aliases_grammar = Grammar("aliases")
    
    def inform_state(self, state):
        self.state = state
    def inform_dep(self, dep):
        self.dep = dep
    def inform_intermediary(self, intermediary):
        self.intermediary = intermediary


def nexus():
    global NEXUS
    if NEXUS==None:
        NEXUS = Nexus()
    return NEXUS






MULTI_CLIPBOARD = {}
STICKY_LIST = []

DICTATION_CACHE = RecognitionHistory(20)
DICTATION_CACHE.register()
PRESERVED_CACHE = None

COMM = Communicator()
TIMER_MANAGER = _Timer(0.025)

RECORDED_MACROS_GRAMMAR = Grammar("recorded_macros")
ALIASES_GRAMMAR = Grammar("aliases")



def print_startup_message():
    print "*- Starting " + settings.SOFTWARE_NAME + " -*"

class DependencyMan:
    def __init__(self):
        self.list = [("natlink", None, ["Auto-Command", "SelectiveAction"], "http://sourceforge.net/projects/natlink"),
                   ("PIL", None, ["Legion"], "https://pypi.python.org/pypi/Pillow"),
                   ("win32ui", "pywin32", ["very many essential"], "http://sourceforge.net/projects/pywin32")]
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
    
print_startup_message()
DEP = DependencyMan()

class StatusIntermediary:
    def __init__(self):
        global COMM
        self.communicator = COMM
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").hint(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").text(message)

nexus().inform_dep(DependencyMan())
nexus().inform_intermediary(StatusIntermediary())
STAT = StatusIntermediary()
