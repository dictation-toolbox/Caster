from unittest import TestCase

from castervoice.lib import utilities, settings
from tests.util import utilities_mocking

'''
BIIIIIIIIIIIIIG testing problem: I can't even import settings.py without it
creating a bunch of files. Need to shut all that stuff off unless some
function is called.
'''

class TestTransformersConfig(TestCase):
    def test_set_transformer_active(self):
        utilities_mocking.mock_toml_files()
        utilities.save_toml_file(settings.SETTINGS[])

        self.fail()

    def test_is_transformer_active(self):
        utilities_mocking.mock_toml_files()

        self.fail()
