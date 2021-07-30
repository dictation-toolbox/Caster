from castervoice.lib.ctrl.mgr.grammar_container.basic_grammar_container import BasicGrammarContainer
from castervoice.lib.ctrl.mgr.ccr_toggle import CCRToggle
from castervoice.lib.ctrl.mgr.companion.companion_config import CompanionConfig
from castervoice.lib.ctrl.mgr.grammar_activator import GrammarActivator
from castervoice.lib.ctrl.mgr.loading.reload.manual_reload_observable import ManualReloadObservable
from castervoice.lib.ctrl.mgr.loading.reload.timer_reload_observable import TimerReloadObservable
from castervoice.lib.ctrl.mgr.rule_maker.mapping_rule_maker import MappingRuleMaker
from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
from castervoice.lib.ctrl.mgr.validation.combo.combo_validation_delegator import ComboValidationDelegator
from castervoice.lib.ctrl.mgr.validation.combo.non_empty_validator import RuleNonEmptyValidator
from castervoice.lib.ctrl.mgr.validation.combo.rule_family_validator import RuleFamilyValidator
from castervoice.lib.ctrl.mgr.validation.combo.treerule_validator import TreeRuleValidator
from castervoice.lib.merge.ccrmerging2.compatibility.simple_compat_checker import SimpleCompatibilityChecker
from castervoice.lib.merge.ccrmerging2.hooks.hooks_config import HooksConfig
from castervoice.lib.merge.ccrmerging2.hooks.hooks_runner import HooksRunner
from castervoice.lib.merge.ccrmerging2.sorting.config_ruleset_sorter import ConfigBasedRuleSetSorter
from castervoice.lib.merge.ccrmerging2.transformers.transformers_config import TransformersConfig
from castervoice.lib.merge.ccrmerging2.transformers.transformers_runner import TransformersRunner
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.validation.details.ccr_app_validator import AppCCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.details.ccr_validator import CCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.details.details_validation_delegator import DetailsValidationDelegator
from castervoice.lib.ctrl.mgr.validation.details.non_ccr_validator import NonCCRDetailsValidator
from castervoice.lib.ctrl.mgr.validation.rules.mergerule_validator import IsMergeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.not_treerule_validator import NotTreeRuleValidator
from castervoice.lib.ctrl.mgr.validation.rules.selfmod_validator import CCRSelfModifyingRuleValidator
from castervoice.lib.merge.communication import Communicator
from castervoice.lib.merge.selfmod.smr_configurer import SelfModRuleConfigurer
from castervoice.lib.merge.state.stack import CasterState
from castervoice.lib.ctrl.mgr.grammar_manager import GrammarManager
from castervoice.lib.ctrl.mgr.validation.rules.rule_validation_delegator import CCRRuleValidationDelegator
from castervoice.lib.merge.ccrmerging2.ccrmerger2 import CCRMerger2
from castervoice.lib.merge.ccrmerging2.merging.classic_merging_strategy import ClassicMergingStrategy

class Nexus:
    def __init__(self, content_loader):
        """
        The Nexus is the 'glue code' of Caster. It is where the things reside which
        manage global state. It is also an access point to those things for other
        things which need them. This access should be limited.
        """

        '''CasterState is used for impl of the asynchronous actions'''

        self.state = CasterState()

        '''rpc class for interacting with Caster UI elements via xmlrpclib'''
        self.comm = Communicator()

        '''tracks both which rules are enabled and the rules' order'''
        rules_config = RulesConfig()

        '''does post-instantiation configuration on selfmodrules'''
        smrc = SelfModRuleConfigurer()

        '''hooks runner: receives and runs events, manages its hooks'''
        hooks_config = HooksConfig()
        hooks_runner = HooksRunner(hooks_config)
        smrc.set_hooks_runner(hooks_runner)

        '''does transformations on rules when rules are activated'''
        transformers_config = TransformersConfig()
        transformers_runner = TransformersRunner(transformers_config)

        '''the ccrmerger -- only merges MergeRules'''
        self._merger = Nexus._create_merger(smrc, transformers_runner)

        '''unified loading mechanism for [rules, transformers, hooks] 
        from [caster starter locations, user dir]'''
        self._content_loader = content_loader

        '''mapping rule maker: like the ccrmerger, but doesn't merge and isn't ccr'''
        mapping_rule_maker = MappingRuleMaker(transformers_runner, smrc)

        '''the grammar manager -- probably needs to get broken apart more'''
        self._grammar_manager = Nexus._create_grammar_manager(self._merger,
            self._content_loader, hooks_runner, rules_config, smrc, mapping_rule_maker,
            transformers_runner)

        '''ACTION TIME:'''
        self._load_and_register_all_content(rules_config, hooks_runner, transformers_runner)
        self._grammar_manager.initialize()

    def _load_and_register_all_content(self, rules_config, hooks_runner, transformers_runner):
        """
        all rules go to grammar_manager
        all transformers go to transformers runner
        all hooks go to hooks runner
        """
        content = self._content_loader.load_everything(rules_config)
        [self._grammar_manager.register_rule(rc, d) for rc, d in content.rules]
        [transformers_runner.add_transformer(t) for t in content.transformers]
        [hooks_runner.add_hook(h) for h in content.hooks]
        self._grammar_manager.load_activation_grammars()

    @staticmethod
    def _create_ccr_rule_validator():
        return CCRRuleValidationDelegator(
            IsMergeRuleValidator(),
            CCRSelfModifyingRuleValidator(),
            NotTreeRuleValidator()
        )

    @staticmethod
    def _create_details_validator():
        return DetailsValidationDelegator(
            CCRDetailsValidator(),
            AppCCRDetailsValidator(),
            NonCCRDetailsValidator(),
        )

    @staticmethod
    def _create_combo_validator():
        return ComboValidationDelegator(
            RuleFamilyValidator(),
            RuleNonEmptyValidator(),
            TreeRuleValidator()
        )

    @staticmethod
    def _create_grammar_manager(merger, content_loader, hooks_runner, rule_config, smrc,
                                mapping_rule_maker, transformers_runner):
        """
        This is where settings should be used to alter the dependency injection being done.
        Setting things to alternate implementations can live here.

        :param merger:
        :param content_loader:
        :param hooks_runner:
        :param rule_config
        :param smrc
        :param mapping_rule_maker
        :param transformers_runner
        :return:
        """

        ccr_toggle = CCRToggle()

        ccr_rule_validator = Nexus._create_ccr_rule_validator()
        details_validator = Nexus._create_details_validator()
        combo_validator = Nexus._create_combo_validator()

        timer = settings.SETTINGS["grammar_reloading"]["reload_timer_seconds"]
        observable = TimerReloadObservable(timer)
        if settings.SETTINGS["grammar_reloading"]["reload_trigger"] == "manual":
            observable = ManualReloadObservable()

        grammars_container = BasicGrammarContainer()

        activator = GrammarActivator(lambda rule: isinstance(rule, MergeRule))

        companion_config = CompanionConfig()

        gm = GrammarManager(rule_config,
                            merger,
                            content_loader,
                            ccr_rule_validator,
                            details_validator,
                            observable,
                            activator,
                            mapping_rule_maker,
                            grammars_container,
                            hooks_runner,
                            ccr_toggle,
                            smrc,
                            transformers_runner,
                            companion_config,
                            combo_validator)
        return gm

    @staticmethod
    def _create_merger(smrc, transformers_runner):
        compat_checker = SimpleCompatibilityChecker()
        merge_strategy = ClassicMergingStrategy()
        max_repetitions = settings.settings(["miscellaneous", "max_ccr_repetitions"])

        return CCRMerger2(transformers_runner, compat_checker, merge_strategy, max_repetitions, smrc)

    def set_ccr_active(self, active):
        self._grammar_manager.set_ccr_active(active)
