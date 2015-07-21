from dragonfly import RecognitionHistory, Grammar

from caster.lib import settings, utilities
from caster.lib.dfplus.communication import Communicator


_NEXUS = None

class StatusIntermediary:
    def __init__(self, c):
        self.communicator = c
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").hint(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").text(message)
    def kill(self):
        if utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
            self.communicator.get_com("status").kill()

class DependencyMan:
    def __init__(self):
        if not settings.WSR:
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

class TimerForWSR:
    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []
    def add_callback(self, function, interval):
        ''''''
    def remove_callback(self, function):
        ''''''
    def callback(self):
        ''''''

class Nexus:
    def __init__(self):
        
        self.state = None
        self.clip = {}
        self.sticky = []
        self.history = []
        if not settings.WSR:
            self.history = RecognitionHistory(20)
            self.history.register()
        self.preserved = None
        
        self.comm = Communicator()
        self.intermediary = StatusIntermediary(self.comm)
        self.timer = TimerForWSR(0.025)
        if not settings.WSR:
            from dragonfly.timer import _Timer
            self.timer = _Timer(0.025)
        self.dep = DependencyMan()
        
        self.macros_grammar = Grammar("recorded_macros")
        self.noderules = []
    
    def inform_state(self, state):# resolves circular import 
        self.state = state
        
    def add_node_rule(self, n):
        self.noderules.append(n)
    
    def get_node_rule(self, name):
        for n in self.noderules:
            if n.master_node.text == name:
                return n
    
    def node_rule_active(self, name, value):        
        self.get_node_rule(name).master_node.active = value
        
        settings.SETTINGS["nodes"][name] = value
        settings.save_config()
        

def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS













