from unittest import TestCase
from castervoice.lib import printer
from castervoice.lib.util import recognition_history
from tests.test_util import utilities_mocking


class ModulesTestCase(TestCase):

    def setUp(self):
        utilities_mocking.enable_mock_toml_files()

    def tearDown(self):
        utilities_mocking.disable_mock_toml_files()

    def _rule_modules(self):
        """
        Child test classes should override this
        """
        return []

    def _run_rule_modifications_for_testing(self, rule_class):
        """
        Child test classes may override this
        """
        pass

    def test_instantiation(self):
        for module in self._rule_modules():
            printer.out("Test instantiating {}".format(str(module)))
            content = module.get_rule()
            rule_class = content[0]
            self._run_rule_modifications_for_testing(rule_class)
            rule_class()

    @classmethod
    def setUpClass(cls):
        # mock the recognition history factory method
        recognition_history.get_and_register_history = lambda x: None
