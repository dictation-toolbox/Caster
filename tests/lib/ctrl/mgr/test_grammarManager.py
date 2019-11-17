from mock import Mock

from castervoice.lib.ctrl.mgr.loading.load.initial_content import FullContentSet
from tests.test_util import settings_mocking
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class TestGrammarManager(SettingsEnabledTestCase):
    """
    A full integration test for the GrammarManager.

    Do not allow any exports to happen at the top of the file which themselves
    import the settings module.
    """

    _MOCK_PATH_RULES_CONFIG = "/mock/rules.file"
    _MOCK_PATH_TRANSFORMERS_CONFIG = "/mock/transformers.file"
    _MOCK_PATH_HOOKS_CONFIG = "/mock/transformers.file"
    _MOCK_PATH_COMPANION_CONFIG = "/mock/companions.file"

    def _setup_config_file(self, utils_module, settings_path, file_path, data):
        self._set_setting(settings_path, file_path)
        utils_module.save_toml_file(data, file_path)

    def _initialize(self, content):
        # self._content_loader.load_everything.side_effect = [content]
        [self._gm.register_rule(rc, d) for rc, d in content.rules]
        [self._transformers_runner.add_transformer(t) for t in content.transformers]
        [self._hooks_runner.add_hook(h) for h in content.hooks]
        self._gm.load_activation_grammars()
        self._gm.initialize()

    def setUp(self):
        settings_mocking.prevent_initialize()
        settings_mocking.prevent_save()
        from tests.test_util import utilities_mocking
        utilities_mocking.mock_toml_files()
        from castervoice.lib import utilities

        # do most imports here so that nothing imports and initializes settings
        from castervoice.lib.ctrl.mgr.ccr_toggle import CCRToggle
        from castervoice.lib.ctrl.mgr.companion.companion_config import CompanionConfig
        from castervoice.lib.ctrl.mgr.grammar_activator import GrammarActivator
        from castervoice.lib.ctrl.mgr.grammar_manager import GrammarManager
        from castervoice.lib.ctrl.mgr.loading.reload.manual_reload_observable import ManualReloadObservable
        from castervoice.lib.ctrl.mgr.rule_maker.mapping_rule_maker import MappingRuleMaker
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.lib.ctrl.nexus import Nexus
        from castervoice.lib.merge.ccrmerging2.hooks.hooks_config import HooksConfig
        from castervoice.lib.merge.ccrmerging2.hooks.hooks_runner import HooksRunner
        from castervoice.lib.merge.ccrmerging2.transformers.transformers_config import TransformersConfig
        from castervoice.lib.merge.ccrmerging2.transformers.transformers_runner import TransformersRunner
        from castervoice.lib.merge.mergerule import MergeRule
        from castervoice.lib.merge.selfmod.smr_configurer import SelfModRuleConfigurer
        from tests.lib.ctrl.mgr.grammar_container.fake_grammar_container import FakeGrammarContainer

        self._setup_config_file(utilities,
                                ["paths", "RULES_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_RULES_CONFIG,
                                {
                                    RulesConfig._ENABLED_ORDERED: [],
                                    RulesConfig._INTERNAL: [],
                                    RulesConfig._WHITELISTED: {}
                                })
        self._setup_config_file(utilities,
                                ["paths", "TRANSFORMERS_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_TRANSFORMERS_CONFIG,
                                {
                                    "TextReplacerTransformer": False
                                })
        self._setup_config_file(utilities,
                                ["paths", "HOOKS_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_HOOKS_CONFIG,
                                {})
        self._setup_config_file(utilities,
                                ["paths", "COMPANION_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_COMPANION_CONFIG,
                                {})
        self._set_setting(["miscellaneous", "max_ccr_repetitions"], 2)
        self._set_setting(["miscellaneous", "ccr_on"], True)

        self._rule_config = RulesConfig()
        smrc = SelfModRuleConfigurer()
        hooks_config = HooksConfig()
        self._hooks_runner = HooksRunner(hooks_config)
        smrc.set_hooks_runner(self._hooks_runner)
        transformers_config = TransformersConfig()
        self._transformers_runner = TransformersRunner(transformers_config)
        merger = Nexus._create_merger(smrc, self._transformers_runner)
        self._content_loader = Mock()
        mapping_rule_maker = MappingRuleMaker(self._transformers_runner, smrc)
        ccr_toggle = CCRToggle()
        ccr_rule_validator = Nexus._create_ccr_rule_validator()
        details_validator = Nexus._create_details_validator()
        combo_validator = Nexus._create_combo_validator()
        observable = ManualReloadObservable()
        grammars_container = FakeGrammarContainer()
        activator = GrammarActivator(lambda rule: isinstance(rule, MergeRule))
        companion_config = CompanionConfig()

        self._gm = GrammarManager(self._rule_config,
                                  merger,
                                  self._content_loader,
                                  ccr_rule_validator,
                                  details_validator,
                                  observable,
                                  activator,
                                  mapping_rule_maker,
                                  grammars_container,
                                  self._hooks_runner,
                                  ccr_toggle,
                                  smrc,
                                  self._transformers_runner,
                                  companion_config,
                                  combo_validator)

    def test_empty_initialize(self):
        """
        Should throw no errors.
        Should have nothing in the grammar container except the ManualGrammarReloadRule.
        """
        self._initialize(FullContentSet([], [], []))
        self.assertEqual(1, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(0, len(self._gm._grammars_container.ccr))

    def test_initialize_one_mergerule(self):
        from castervoice.lib.ccr.core import alphabet
        one_rule = alphabet.get_rule()
        self._initialize(FullContentSet([one_rule], [], []))
        self.assertEqual(2, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(1, len(self._gm._grammars_container.ccr))

    def test_initialize_two_compatible_global_mergerules(self):
        from castervoice.lib.ccr.core import alphabet
        from castervoice.lib.ccr.core import punctuation
        a = alphabet.get_rule()
        b = punctuation.get_rule()
        self._initialize(FullContentSet([a, b], [], []))
        self.assertEqual(2, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(1, len(self._gm._grammars_container.ccr))

    def test_enable_rule_causes_a_save(self):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.lib.ccr.core import alphabet
        from castervoice.lib.ccr.core import punctuation

        # "write" the rules.toml file:
        self._setup_config_file(utilities,
                                ["paths", "RULES_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_RULES_CONFIG,
                                {
                                    RulesConfig._ENABLED_ORDERED: ["Alphabet"],
                                    RulesConfig._INTERNAL: [],
                                    RulesConfig._WHITELISTED: {
                                        "Alphabet": True,
                                        "Punctuation": True
                                    }
                                })
        self._rule_config.load()

        # check that the mock file changes were written
        self.assertEqual(1, len(self._rule_config._config[RulesConfig._ENABLED_ORDERED]))

        # initialize the gm
        a, b = alphabet.get_rule(), punctuation.get_rule()
        self._initialize(FullContentSet([a, b], [], []))

        # simulate a spoken "enable" command from the GrammarActivator:
        self._gm._change_rule_enabled("Punctuation", True)
        # afterwards, the config should have both Alphabet and Punctuation enabled
        config = utilities.load_toml_file(TestGrammarManager._MOCK_PATH_RULES_CONFIG)
        self.assertIn("Alphabet", config[RulesConfig._ENABLED_ORDERED])
        self.assertIn("Punctuation", config[RulesConfig._ENABLED_ORDERED])

    def test_enable_incompatible_rule_knockout_is_saved(self):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.lib.ccr.java import java
        from castervoice.lib.ccr.python import python

        # "write" the rules.toml file:
        self._setup_config_file(utilities,
                                ["paths", "RULES_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_RULES_CONFIG,
                                {
                                    RulesConfig._ENABLED_ORDERED: ["Java"],
                                    RulesConfig._INTERNAL: [],
                                    RulesConfig._WHITELISTED: {
                                        "Java": True,
                                        "Python": True
                                    }
                                })
        self._rule_config.load()

        # check that the mock file changes were written
        self.assertEqual(1, len(self._rule_config._config[RulesConfig._ENABLED_ORDERED]))

        # initialize the gm
        a, b = java.get_rule(), python.get_rule()
        self._initialize(FullContentSet([a, b], [], []))

        # simulate a spoken "enable" command from the GrammarActivator:
        self._gm._change_rule_enabled("Python", True)
        # afterwards, the config should have Python enabled but not Java
        config = utilities.load_toml_file(TestGrammarManager._MOCK_PATH_RULES_CONFIG)
        self.assertNotIn("Java", config[RulesConfig._ENABLED_ORDERED])
        self.assertIn("Python", config[RulesConfig._ENABLED_ORDERED])
