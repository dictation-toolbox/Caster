from castervoice.lib.ctrl.mgr.loading.load import content_loader
from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
from tests.test_util import utilities_mocking
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class _FakeRule(object):
    pass


class _FakeImportedRuleModule(object):
    def __init__(self, content):
        self._content = content

    def get_rule(self):
        return self._content


class _FakeImportedHookModule(object):
    def __init__(self, content):
        self._content = content

    def get_hook(self):
        return self._content


class TestContentLoader(SettingsEnabledTestCase):

    _RULE_CONFIG_PATH = "/mock/rule/config/path"
    _RULE_MODULE_NAME = "rule_module"

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

    def test_load_everything(self):
        #self.cl.load_everything()
        pass

    def test_idem_import_module_reimport_success(self):
        '''
        scenarios to test:
        1. reimport / fn found -> return content of fn
        2. reimport / error -> return None, check error was printed
        3. import / fn found -> return content of fn
        3b. import non-rule success
        4. import / error -> return None, check error was printed
        5. AttributeError -> return None, check error was printed
        6. other error when calling getattr -> return None, check error was printed
        '''
        rule_module = _FakeImportedRuleModule(_FakeRule)
        content_loader._MODULES = {TestContentLoader._RULE_MODULE_NAME: rule_module}
        rule_class = self.cl.idem_import_module(TestContentLoader._RULE_MODULE_NAME, ContentType.GET_RULE)
        self.assertEqual(_FakeRule, rule_class)



