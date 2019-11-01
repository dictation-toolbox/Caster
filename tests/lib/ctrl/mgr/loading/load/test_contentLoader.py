from mock import Mock

from castervoice.lib.ctrl.mgr.loading.load import content_loader
from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
from tests.test_util import utilities_mocking, printer_mocking
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class _FakeImportedRuleModule(object):
    def __init__(self, content):
        self._content = content

    def get_rule(self):
        return self._content


class _FakeImportedHookModule(object):
    def __init__(self, content):
        self._content = content
        self.__file__ = "castervoice"

    def get_hook(self):
        return self._content


class _FakeContent(object):
    pass


def _raise(_):
    raise Exception("Test Exception")


class TestContentLoader(SettingsEnabledTestCase):

    _RULE_CONFIG_PATH = "/mock/rule/config/path"
    _RULE_MODULE_NAME = "rule_module"
    _HOOK_NAME = "hook_module"

    def setUp(self):
        self._set_setting(["paths", "RULES_CONFIG_PATH"], TestContentLoader._RULE_CONFIG_PATH)
        self._set_setting(["paths", "BASE_PATH"], "/mock/base/path")
        self._set_setting(["paths", "USER_DIR"], "/mock/user/dir")
        self.crg_mock = ContentRequestGenerator()
        utilities_mocking.mock_toml_files()
        self.rc_mock = RulesConfig()
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleOne"] = True
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleTwo"] = False
        self.cl = content_loader.ContentLoader(self.crg_mock)
        self.cl._get_reload_fn = Mock()
        self.cl._get_reload_fn.side_effect = [lambda x: x]
        self.cl._get_load_fn = Mock()

    def test_load_everything(self):
        #self.cl.load_everything()
        # TODO: this test
        pass

    def test_idem_import_module_reimport_success(self):
        rule_module = _FakeImportedRuleModule(_FakeContent)
        content_loader._MODULES = {TestContentLoader._RULE_MODULE_NAME: rule_module}
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        self.assertEqual(_FakeContent, rule_class)

    def test_idem_import_module_reimport_failure(self):
        rule_module = _FakeImportedRuleModule(_FakeContent)
        content_loader._MODULES = {TestContentLoader._RULE_MODULE_NAME: rule_module}
        spy = printer_mocking.printer_spy()
        self.cl._get_reload_fn = _raise
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        expected_error = "An error occurred while importing '"
        self.assertIsNone(rule_class)
        self.assertTrue(expected_error in spy.get_first())

    def test_idem_import_module_import_rule_success(self):
        rule_module = _FakeImportedRuleModule(_FakeContent)
        content_loader._MODULES = {}
        self.cl._get_load_fn.side_effect = [lambda x: rule_module]
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        self.assertEqual(_FakeContent, rule_class)

    def test_idem_import_module_import_hook_success(self):
        hook_module = _FakeImportedHookModule(_FakeContent)
        content_loader._MODULES = {}
        self.cl._get_load_fn.side_effect = [lambda x: hook_module]
        hook_class = self.cl.idem_import_module(TestContentLoader._HOOK_NAME, ContentType.GET_HOOK)
        self.assertEqual(_FakeContent, hook_class)

    def test_idem_import_module_import_failure(self):
        content_loader._MODULES = {}
        spy = printer_mocking.printer_spy()
        self.cl._get_load_fn = _raise
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        expected_error = "Could not import 'rule_module'. Module has errors:"
        self.assertIsNone(rule_class)
        self.assertTrue(expected_error in spy.get_first())

    def test_idem_import_module_attribute_error(self):
        hook_module = _FakeImportedHookModule(_FakeContent)
        content_loader._MODULES = {TestContentLoader._RULE_MODULE_NAME: hook_module}
        spy = printer_mocking.printer_spy()
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        expected_error = "No method named 'get_rule' was found on 'rule_module'. Did you forget to implement it?"
        self.assertIsNone(rule_class)
        self.assertEqual(expected_error, spy.get_first())
