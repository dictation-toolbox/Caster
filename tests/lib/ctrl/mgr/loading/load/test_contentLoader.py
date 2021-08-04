import os
from mock import Mock
from castervoice.lib.ctrl.mgr.loading.load import content_loader
from castervoice.lib.ctrl.mgr.loading.load.content_request import ContentRequest
from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
from castervoice.lib.ctrl.mgr.loading.load.content_type import ContentType
from castervoice.lib.ctrl.mgr.loading.load.modules_access import SysModulesAccessor
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


class _FakeModulesAccessor(SysModulesAccessor):

    def __init__(self):
        self.modules = {}

    def has_module(self, module_name):
        return module_name in self.modules

    def get_module(self, module_name):
        return self.modules[module_name]


def _raise(_):
    raise Exception("Test Exception")


def _create_os_path(*tokens):
    return os.sep.join(tokens)


class TestContentLoader(SettingsEnabledTestCase):

    _RULE_CONFIG_PATH = _create_os_path("mock", "rule", "config", "path")

    _HOOK_NAME = "hook_module"

    _DEFAULT_PACKAGE_NAME = "some_module"
    _DEFAULT_MODULE_NAME = _DEFAULT_PACKAGE_NAME
    _DEFAULT_PACKAGE_PATH = _create_os_path("root", "castervoice", "asdf", _DEFAULT_PACKAGE_NAME)
    _QUALIFIED_MODULE_NAME = "castervoice.asdf.some_module.some_module"

    def setUp(self):
        self._set_setting(["paths", "RULES_CONFIG_PATH"], TestContentLoader._RULE_CONFIG_PATH)
        self._set_setting(["paths", "BASE_PATH"], _create_os_path("mock", "base", "path", "castervoice"))
        self._set_setting(["paths", "USER_DIR"], _create_os_path("mock", "user", "dir", "caster"))
        self.crg_mock = ContentRequestGenerator()
        utilities_mocking.enable_mock_toml_files()
        self.rc_mock = RulesConfig()
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleOne"] = True
        self.rc_mock._config[RulesConfig._WHITELISTED]["MockRuleTwo"] = False
        self.fake_modules_accessor = _FakeModulesAccessor()
        self.cl = content_loader.ContentLoader(self.crg_mock, Mock(), Mock(), self.fake_modules_accessor)
        self.spy, cleanup = printer_mocking.printer_spy()
        self.addCleanup(cleanup)

    def tearDown(self):
        utilities_mocking.disable_mock_toml_files()

    def _create_request(self, module_name, content_type, directory=_DEFAULT_PACKAGE_PATH,
                        content_class_name=None):
        """helper fn"""
        return ContentRequest(content_type, directory, module_name, content_class_name)

    def test_load_everything(self):
        #self.cl.load_everything()
        # TODO: this test
        pass

    def test_idem_import_module_import_rule_success(self):
        """import"""
        # setup mock import
        self.cl._module_load_fn.side_effect = [_FakeImportedRuleModule(_FakeContent)]

        # setup request
        request = self._create_request(TestContentLoader._DEFAULT_MODULE_NAME, ContentType.GET_RULE)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertEqual(_FakeContent, result)

    def test_idem_import_module_import_hook_success(self):
        """import"""
        # setup mock import
        self.cl._module_load_fn.side_effect = [_FakeImportedHookModule(_FakeContent)]

        # setup request
        request = self._create_request(TestContentLoader._HOOK_NAME, ContentType.GET_HOOK)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertEqual(_FakeContent, result)

    def test_idem_import_module_import_failure(self):
        """import"""
        # simulate load error
        self.cl._module_load_fn = _raise

        # setup request
        request = self._create_request(TestContentLoader._DEFAULT_MODULE_NAME, ContentType.GET_RULE)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertIsNone(result)
        expected_error = "Could not import '{}'. Module has errors:".format(TestContentLoader._QUALIFIED_MODULE_NAME)
        self.assertTrue(expected_error in self.spy.get_first())

    def test_idem_import_module_attribute_error(self):
        """import"""
        # setup mock import
        self.cl._module_load_fn.side_effect = [_FakeImportedHookModule(_FakeContent)]

        # setup request
        request = self._create_request(TestContentLoader._DEFAULT_MODULE_NAME, ContentType.GET_RULE)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertIsNone(result)
        expected_error = "No method named 'get_rule' was found on '{}'. Did you forget to implement it?".format(
            TestContentLoader._DEFAULT_MODULE_NAME)
        self.assertEqual(expected_error, self.spy.get_first())

    def test_idem_import_module_reimport_success(self):
        """reimport"""
        # setup fake sys.modules
        self.fake_modules_accessor.modules = \
            {TestContentLoader._QUALIFIED_MODULE_NAME: _FakeImportedRuleModule(_FakeContent)}
        # setup request
        request = self._create_request(TestContentLoader._DEFAULT_MODULE_NAME, ContentType.GET_RULE)
        # setup fake reload function
        self.cl._module_reload_fn.side_effect = lambda x: x

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertEqual(_FakeContent, result)

    def test_idem_import_module_reimport_failure(self):
        """reimport"""
        # setup fake sys.modules
        self.fake_modules_accessor.modules = \
            {TestContentLoader._QUALIFIED_MODULE_NAME: _FakeImportedRuleModule(_FakeContent)}
        # simulate reload error
        self.cl._module_reload_fn = _raise
        # setup request
        request = self._create_request(TestContentLoader._DEFAULT_MODULE_NAME, ContentType.GET_RULE)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertIsNone(result)
        self.assertTrue("An error occurred while importing '" in self.spy.get_first())

    def test_idem_import_module_qualification_failure(self):
        # setup invalid request
        request = ContentRequest(ContentType.GET_RULE, "adsf", TestContentLoader._DEFAULT_MODULE_NAME, None)

        # method under test
        self.cl.idem_import_module(request)

        # method under test
        result = self.cl.idem_import_module(request)

        # assertions
        self.assertIsNone(result)
        self.assertTrue("Invalid user content request path" in self.spy.get_first())
