from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
from castervoice.lib.ctrl.mgr.rules_config import RulesConfig
from tests.test_util import utilities_mocking
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class TestContentLoader(SettingsEnabledTestCase):

    _RULE_CONFIG_PATH = "/mock/rule/config/path"

    def setUp(self):
        self._set_setting(["paths", "RULES_CONFIG_PATH"], TestContentLoader._RULE_CONFIG_PATH)
        self._set_setting(["paths", "BASE_PATH"], "/mock/base/path")
        self._set_setting(["paths", "USER_DIR"], "/mock/user/dir")
        self.crg_mock = ContentRequestGenerator()
        utilities_mocking.mock_toml_files()
        self.rc_mock = RulesConfig()
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleOne"] = True
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleTwo"] = False
        self.cl = ContentLoader(self.crg_mock)

    def test_load_everything(self):pass
        #self.cl.load_everything()
