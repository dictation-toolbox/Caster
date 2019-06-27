from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from castervoice.lib import settings
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.wsrdf import RecognitionHistoryForWSR
from castervoice.lib.dfplus.communication import Communicator
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.stack import CasterState
from castervoice.lib.ctrl.user import UserContentManager


class Nexus:
    def __init__(self, real_merger_config=True):

        self.state = CasterState()

        self.clip = {}

        self.temp = ""

        if settings.WSR or not real_merger_config:
            self.history = RecognitionHistoryForWSR(20)
        else:
            self.history = RecognitionHistory(20)
            self.history.register()
        self.state.set_stack_history(self.history)
        self.preserved = None

        self.comm = Communicator()

        self.dep = DependencyMan()

        self.macros_grammar = Grammar("recorded_macros")

        self.merger = CCRMerger(real_merger_config)

        self.content_manager = UserContentManager()

