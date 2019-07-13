from castervoice.lib import settings
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.mgr.validation.details.ccr_app_validator import AppCCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.details.ccr_validator import CCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.details.details_validation_delegator import DetailsValidationDelegator
from castervoice.lib.ctrl.mgr.validation.details.non_ccr_validator import NonCCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.rules.context_validator import HasContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.mergerule_validator import IsMergeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.no_context_validator import HasNoContextValidator
from castervoice.lib.ctrl.mgr.validation.rules.not_noderule_validator import NotNodeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.pronunciation_validator import PronunciationAvailableValidator
from castervoice.lib.ctrl.mgr.validation.rules.selfmod_validator import SelfModifyingRuleValidator
from castervoice.lib.ctrl.wsrdf import RecognitionHistoryForWSR
from castervoice.lib.dfplus.communication import Communicator
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.stack import CasterState
from dragonfly.grammar.context import AppContext
from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from castervoice.lib.ctrl.mgr.grammar_manager import GrammarManager
from castervoice.lib.ctrl.mgr.loading.content_loader import ContentLoader
from castervoice.lib.ctrl.mgr.validation.rules.rule_validation_delegator import CCRRuleValidationDelegator
from castervoice.lib.dfplus.ccrmerging2.ccrmerger2 import CCRMerger2
from castervoice.lib.dfplus.ccrmerging2.compatibility.simple_compat_checker import SimpleCompatibilityChecker
from castervoice.lib.dfplus.ccrmerging2.config.config_toml import TomlCCRConfig
from castervoice.lib.dfplus.ccrmerging2.merging.classic_merging_strategy import ClassicMergingStrategy
from castervoice.lib.dfplus.ccrmerging2.sorting.config_ruleset_sorter import ConfigRuleSetSorter
from __builtin__ import True
from castervoice.lib.ctrl.mgr.loading.file_watcher_observable import FileWatcherObservable
from castervoice.lib.ctrl.mgr.loading.manual_reload_observable import ManualReloadObservable


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

        self.merger = CCRMerger()

        self.content_loader = None
        
    def set_merger(self, merger):
        self.merger = merger
        
    def load_and_register_all_content(self):
        self.content_loader = ContentLoader()
        content = self.content_loader.load_everything()
        
        '''
        all rules go to grammar_manager
        all transformers go to merger
        TODO: hooks go to both? depends on where we want hook events, eh?
        '''
        ccr_rule_validator = CCRRuleValidationDelegator(
            IsMergeRuleValidator(),
            HasNoContextValidator(),
            HasContextValidator(),
            SelfModifyingRuleValidator(),
            NotNodeRuleValidator(),
            PronunciationAvailableValidator()
        )
        details_validator = DetailsValidationDelegator(
            CCRDetailsValidator(),
            AppCCRDetailsValidator(),
            NonCCRDetailsValidator()
        )
        some_setting = True
        observable = FileWatcherObservable()
        if some_setting:
            observable = ManualReloadObservable()
        
        GrammarManager.set_instance(self.merger, settings, AppContext, Grammar, [],
                                    ccr_rule_validator, details_validator,
                                    content.rules, observable)
        

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
        pass
#         global_validator = CompositeValidator([
#                 IsMergeRuleValidator(),
#                 HasNoContextValidator(),
#                 PronunciationAvailableValidator()
#             ])
#         app_validator = CompositeValidator([
#             HasContextValidator(),
#             PronunciationAvailableValidator()
#             ])
#         sm_validator = CompositeValidator([
#             SelfModifyingRuleValidator(),
#             NotNodeRuleValidator(),
#             PronunciationAvailableValidator()
#             ])
        


_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS
