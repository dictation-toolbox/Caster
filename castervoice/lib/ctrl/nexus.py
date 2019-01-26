from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from castervoice.lib import settings
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.wsrdf import TimerForWSR, RecognitionHistoryForWSR
from castervoice.lib.dfplus.communication import Communicator
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.stack import CasterState


class Nexus:
    def __init__(self, real_merger_config=True):

        self.state = CasterState()

        self.clip = {}

        self.history = RecognitionHistoryForWSR(20)
        if not settings.WSR:
            self.history = RecognitionHistory(20)
            self.history.register()
        self.state.set_stack_history(self.history)
        self.preserved = None

        self.timer = TimerForWSR(0.025)
        if not settings.WSR:
            from dragonfly.timer import _Timer
            self.timer = _Timer(0.025)

        self.comm = Communicator()

        self.dep = DependencyMan()

        self.macros_grammar = Grammar("recorded_macros")

        self.merger = CCRMerger(real_merger_config)


_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS
