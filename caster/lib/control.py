from dragonfly import RecognitionHistory, Grammar
from dragonfly.timer import _Timer

from caster.lib import settings
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

        

class Nexus:
    def __init__(self):
        
        self.state = None
        self.clip = {}
        self.sticky = []
        self.history = RecognitionHistory(20)
        self.history.register()
        self.preserved = None
        
        self.comm = Communicator()
        self.intermediary = StatusIntermediary(self.comm)
        self.timer = _Timer(0.025)
        
        self.dep = DependencyMan()
        self.intermediary = None
        
        self.macros_grammar = Grammar("recorded_macros")
        self.noderules = []
    
    def inform_state(self, state):# resolves circular import 
        self.state = state
        
    def add_node_rule(self, n):
        self.noderules.append(n)
    
    def get_node_rule(self, name):
        for n in self.noderules:
            if n.node.text == name:
                return n
    
    def node_rule_active(self, name, value):
        print self.get_node_rule(name).node, value
        
        self.get_node_rule(name).node.active = value
        
        print 5
        settings.SETTINGS["nodes"][name] = value
        settings.save_config()
        

def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS



print "*- Starting " + settings.SOFTWARE_NAME + " -*"









