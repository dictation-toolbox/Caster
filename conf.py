# Read The Docs Configuration file

import sys
if sys.version_info >= (3, 3):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = ['wxWidgets']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
