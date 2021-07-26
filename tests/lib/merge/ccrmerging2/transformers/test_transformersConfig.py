from castervoice.lib import utilities
from castervoice.lib.merge.ccrmerging2.transformers.transformers_config import TransformersConfig
from tests.test_util import utilities_mocking
from tests.test_util.settings_mocking import SettingsEnabledTestCase


class TestTransformersConfig(SettingsEnabledTestCase):

    _MOCK_PATH = "/mock/path"

    def setUp(self):
        self._set_setting(["paths", "TRANSFORMERS_CONFIG_PATH"],
                          TestTransformersConfig._MOCK_PATH)
        utilities_mocking.enable_mock_toml_files()
        utilities.save_toml_file({
            "MockTransformer": True,
            "OffTransformer": False
        }, TestTransformersConfig._MOCK_PATH)

    def tearDown(self):
        utilities_mocking.disable_mock_toml_files()

    def test_set_transformer_active(self):
        tc = TransformersConfig()
        self.assertFalse(tc.is_transformer_active("OffTransformer"))
        tc.set_transformer_active("OffTransformer", True)
        self.assertTrue(tc.is_transformer_active("OffTransformer"))

    def test_is_transformer_active(self):
        tc = TransformersConfig()
        self.assertTrue(tc.is_transformer_active("MockTransformer"))
        self.assertFalse(tc.is_transformer_active("OffTransformer"))

    def test_contains(self):
        tc = TransformersConfig()
        self.assertTrue("MockTransformer" in tc)
