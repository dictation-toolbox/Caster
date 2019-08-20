from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from castervoice.lib import settings
from castervoice.lib.dfplus.communication import Communicator
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.stack import CasterState
from castervoice.lib.ctrl.user import UserContentManager


class Nexus:
    def __init__(self, real_merger_config=True):

        self.state = CasterState()

        self.clip = {}

        self.temp = ""

        self.history = RecognitionHistory(20)
        if real_merger_config:
            self.history.register()
        self.state.set_stack_history(self.history)
        self.preserved = None

        self.comm = Communicator()

        self.macros_grammar = Grammar("recorded_macros")

        self.merger = CCRMerger(real_merger_config)

        self.user_content_manager = None

    def process_user_content(self):
        self.user_content_manager = UserContentManager()

        self.merger.add_user_content(self.user_content_manager)


_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS
