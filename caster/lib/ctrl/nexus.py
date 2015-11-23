from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from caster.lib import settings
from caster.lib.ctrl.dependencies import DependencyMan
from caster.lib.ctrl.intermediary import StatusIntermediary
from caster.lib.ctrl.switcher import AutoSwitcher
from caster.lib.ctrl.wsrdf import TimerForWSR, RecognitionHistoryForWSR
from caster.lib.dfplus.communication import Communicator
from caster.lib.dfplus.merge.ccrmerger import CCRMerger


class Nexus:
    def __init__(self, real_merger_config=True):
        
        self.state = None
        
        self.clip = {}
        self.sticky = []
        
        self.history = RecognitionHistoryForWSR(20)
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
        
        self.merger = CCRMerger(real_merger_config)
        self.auto = AutoSwitcher(self)
    
    def inform_state(self, state):# resolves circular import 
        self.state = state

_NEXUS = None
def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS
