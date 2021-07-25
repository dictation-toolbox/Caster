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

    def _setup_rules_config_file(self, loadable_true=[], enabled=[]):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        self._setup_config_file(utilities,
                                ["paths", "RULES_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_RULES_CONFIG,
                                {
                                    RulesConfig._ENABLED_ORDERED: enabled,
                                    RulesConfig._INTERNAL: [],
                                    RulesConfig._WHITELISTED: {
                                        rcn: True for rcn in loadable_true
                                    }
                                })
        self._rule_config.load()

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
        utilities_mocking.enable_mock_toml_files()
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

    def tearDown(self):
        from tests.test_util import utilities_mocking
        utilities_mocking.disable_mock_toml_files()

    def test_empty_initialize(self):
        """
        Should throw no errors.
        Should have nothing in the grammar container except the ManualGrammarReloadRule.
        """
        self._initialize(FullContentSet([], [], []))
        self.assertEqual(1, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(0, len(self._gm._grammars_container.ccr))

    def test_initialize_one_mergerule(self):
        from castervoice.rules.core.alphabet_rules import alphabet
        self._setup_rules_config_file(loadable_true=["Alphabet"], enabled=["Alphabet"])
        one_rule = alphabet.get_rule()
        self._initialize(FullContentSet([one_rule], [], []))
        self.assertEqual(2, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(1, len(self._gm._grammars_container.ccr))

    def test_initialize_two_compatible_global_mergerules(self):
        from castervoice.rules.core.alphabet_rules import alphabet
        from castervoice.rules.core.punctuation_rules import punctuation
        self._setup_rules_config_file(loadable_true=["Alphabet", "Punctuation"], enabled=["Alphabet", "Punctuation"])
        a = alphabet.get_rule()
        b = punctuation.get_rule()
        self._initialize(FullContentSet([a, b], [], []))
        self.assertEqual(2, len(self._gm._grammars_container.non_ccr.keys()))
        self.assertEqual(1, len(self._gm._grammars_container.ccr))

    def test_enable_rule_causes_a_save(self):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.rules.core.alphabet_rules import alphabet
        from castervoice.rules.core.punctuation_rules import punctuation

        # "write" the rules.toml file:
        self._setup_rules_config_file(loadable_true=["Alphabet", "Punctuation"], enabled=["Alphabet"])

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
        from castervoice.rules.ccr.java_rules import java
        from castervoice.rules.ccr.python_rules import python

        # "write" the rules.toml file:
        self._setup_rules_config_file(loadable_true=["Java", "Python"], enabled=["Java"])

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

    def test_knockout_with_companions_saves_correctly(self):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.rules.ccr.java_rules import java
        from castervoice.rules.ccr.java_rules import java2
        from castervoice.rules.ccr.python_rules import python
        from castervoice.rules.ccr.python_rules import python2
        from castervoice.rules.core.alphabet_rules import alphabet
        from castervoice.rules.apps.microsoft_office import outlook

        # "write" the companion config file
        self._setup_config_file(utilities,
                                ["paths", "COMPANION_CONFIG_PATH"],
                                TestGrammarManager._MOCK_PATH_COMPANION_CONFIG,
                                {
                                    "Java": ["JavaNon"],
                                    "Python": ["PythonNon"]
                                })

        # "write" the rules.toml file:
        self._setup_rules_config_file(loadable_true=["Alphabet", "OutlookRule", "Java", "JavaNon",
                                                     "Python", "PythonNon"],
                                      enabled=["Alphabet", "OutlookRule", "Java", "JavaNon"])

        # check that the mock file changes were written
        self.assertEqual(4, len(self._rule_config._config[RulesConfig._ENABLED_ORDERED]))

        # initialize the gm
        alphabet_rule, outlook_rule = alphabet.get_rule(), outlook.get_rule()
        python_rule, pythonnon_rule = python.get_rule(), python2.get_rule()
        java_rule, javanon_rule = java.get_rule(), java2.get_rule()
        self._initialize(FullContentSet([alphabet_rule, outlook_rule, python_rule, pythonnon_rule,
                                         java_rule, javanon_rule], [], []))

        # simulate a spoken "enable" command from the GrammarActivator:
        self._gm._change_rule_enabled("Python", True)
        """
        Afterwards, all of the following should be true:
        1. Python and PythonNon should each be in rules.toml exactly once
        2. Java and JavaNon should be in rules.toml zero times
        3. Alphabet and Outlook should still be in rules.toml
        """
        config = utilities.load_toml_file(TestGrammarManager._MOCK_PATH_RULES_CONFIG)
        enabled_ordered = config[RulesConfig._ENABLED_ORDERED]
        self.assertEqual(1, enabled_ordered.count("Python"))
        self.assertEqual(1, enabled_ordered.count("PythonNon"))
        self.assertEqual(0, enabled_ordered.count("Java"))
        self.assertEqual(0, enabled_ordered.count("JavaNon"))
        self.assertEqual(1, enabled_ordered.count("Alphabet"))
        self.assertEqual(1, enabled_ordered.count("OutlookRule"))

    def test_internal_rules_dont_create_duplicates(self):
        from castervoice.lib import utilities
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.rules.core.alphabet_rules import alphabet

        # "write" the rules.toml file:
        self._setup_rules_config_file(loadable_true=["Alphabet"],
                                      enabled=["GrammarActivatorRule", "ManualGrammarReloadRule"])

        # check that the mock file changes were written
        self.assertEqual(2, len(self._rule_config._config[RulesConfig._ENABLED_ORDERED]))

        # initialize the gm
        alphabet_rule = alphabet.get_rule()
        self._initialize(FullContentSet([alphabet_rule], [], []))

        """
        After initialization, there should only be one copy of each of these in rules.toml: 
        GrammarActivatorRule 
        ManualGrammarReloadRule
        """
        config = utilities.load_toml_file(TestGrammarManager._MOCK_PATH_RULES_CONFIG)
        enabled_ordered = config[RulesConfig._ENABLED_ORDERED]
        self.assertEqual(1, enabled_ordered.count("GrammarActivatorRule"))
        self.assertEqual(1, enabled_ordered.count("ManualGrammarReloadRule"))

    def test_disable_non_enabled_doesnt_crash(self):
        from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
        from castervoice.rules.ccr.java_rules import java
        from castervoice.rules.ccr.python_rules import python

        # "write" the rules.toml file:
        self._setup_rules_config_file(loadable_true=["Java", "Python"], enabled=["Java"])

        # check that the mock file changes were written
        self.assertEqual(1, len(self._rule_config._config[RulesConfig._ENABLED_ORDERED]))

        # initialize the gm
        a, b = java.get_rule(), python.get_rule()
        self._initialize(FullContentSet([a, b], [], []))

        # simulate a spoken "enable" command from the GrammarActivator:
        self._gm._change_rule_enabled("Python", False)
