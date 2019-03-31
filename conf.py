# Read The Docs Configuration file
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = ['wxWidgets']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
