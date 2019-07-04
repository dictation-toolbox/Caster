from castervoice.lib import settings
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.user import UserContentManager
from castervoice.lib.ctrl.wsrdf import TimerForWSR, RecognitionHistoryForWSR
from castervoice.lib.dfplus.communication import Communicator
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.stack import CasterState
from dragonfly.grammar.context import AppContext
from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from castervoice.lib.ctrl.mgr.grammar_manager import GrammarManager
from castervoice.lib.ctrl.mgr.validation.rules.composite_validator import CompositeValidator
from castervoice.lib.ctrl.mgr.validation.rules.context_validator import HasContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.mergerule_validator import IsMergeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.no_context_validator import HasNoContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.not_noderule_validator import NotNodeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.pronunciation_validator import PronunciationAvailableValidator
from castervoice.lib.ctrl.mgr.validation.rules.selfmod_validator import SelfModifyingRuleValidator
from castervoice.lib.dfplus.ccrmerging2.ccrmerger2 import CCRMerger2
from castervoice.lib.dfplus.ccrmerging2.config.config_toml import TomlCCRConfig
from castervoice.lib.dfplus.ccrmerging2.sorting.config_ruleset_sorter import ConfigRuleSetSorter
from castervoice.lib.dfplus.ccrmerging2.compatibility.simple_compat_checker import SimpleCompatibilityChecker
from castervoice.lib.dfplus.ccrmerging2.merging.classic_merging_strategy import ClassicMergingStrategy


class Nexus:
    def __init__(self, real_merger_config=True):

        self.state = CasterState()

        self.clip = {}

        self.temp = ""

        if settings.WSR or not real_merger_config:
            self.history = RecognitionHistoryForWSR(20)
            self.timer = TimerForWSR(0.025)
        else:
            from dragonfly.timer import _Timer
            self.timer = _Timer(0.025)
            self.history = RecognitionHistory(20)
            self.history.register()
        self.state.set_stack_history(self.history)
        self.preserved = None

        self.comm = Communicator()

        self.dep = DependencyMan()

        self.macros_grammar = Grammar("recorded_macros")

        self.merger = CCRMerger()

        self.user_content_manager = None
        
    def set_merger(self, merger):
        self.merger = merger

    def process_user_content(self):
        self.user_content_manager = UserContentManager()

        self.merger.add_user_content(self.user_content_manager)
    
    def create_merger(self):
        '''
        def __init__(self, ccr_config, 
                 transformers, rule_sorter, compatibility_checker,
                 merging_strategy, grammar_manager_module):
        
        '''
        config = TomlCCRConfig()
        sorter = ConfigRuleSetSorter()
        compat_checker = SimpleCompatibilityChecker()
        merge_strategy = ClassicMergingStrategy()
        
        merger = CCRMerger2(config, sorter, compat_checker, 
                            merge_strategy, GrammarManager)

    def create_grammar_manager(self, merger, transformers):
        global_validator = CompositeValidator([
                IsMergeRuleValidator(),
                HasNoContextValidator(),
                PronunciationAvailableValidator()
            ])
        app_validator = CompositeValidator([
            HasContextValidator(),
            PronunciationAvailableValidator()
            ])
        sm_validator = CompositeValidator([
            SelfModifyingRuleValidator(),
            NotNodeRuleValidator(),
            PronunciationAvailableValidator()
            ])
        GrammarManager.set_instance(merger, settings, AppContext, Grammar, transformers,
                                    global_validator, app_validator, sm_validator)


_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS
