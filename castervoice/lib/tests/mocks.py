import mock
import sys
import types

from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule

module_tree = {'win32con': [], 'win32ui': [], 'win32gui': ["GetForegroundWindow"],
        '_winreg': ['CloseKey', 'ConnectRegistry', 'HKEY_CLASSES_ROOT',
        'HKEY_CURRENT_USER', 'OpenKey', 'QueryValueEx'], 'dragonfly.windows.window':
        ['Window'], 'ctypes.windll': []}
for module_name, imports in module_tree.iteritems():
    bogus_module = types.ModuleType(module_name)
    sys.modules[module_name] = bogus_module
    for i in imports:
        setattr(bogus_module, i, mock.Mock(name='%s.%s' % (module_name, i)))

from dragonfly.os_dependent_mock import MockAction
from dragonfly import AppContext

from castervoice.lib.merge.mergerule import MergeRule

MockText = MockAction
MockKey = MockAction
MockFunction = MockAction
MockPause = MockAction

class Python(MergeRule):
    mapping = {
        "iffae": MockText("if :") + MockKey("left"),
        "yield": MockText("yield "),

    }

class Java(MergeRule):
    mapping = {
        "iffae": MockText("if () {") + MockKey("enter,up,left"),
        "dock string": MockText("/***/") + MockKey("left,left,enter"),
    }

class Javascript(MergeRule):
    mapping = {
        "iffae": MockText("if () {") + MockKey("enter,up,left"),
        "tick string": MockText("``") + MockKey("left"),
    }

class Bash(MergeRule):
    mapping = {
        "iffae":
            MockText("if [[  ]]; ") + MockKey("left/5:5"),
        "key do":
            MockText("do"),
    }

class AliasRule(BaseSelfModifyingRule):
    def __init__(self):
        BaseSelfModifyingRule.__init__(self)

class Alias(AliasRule):
    def __init__(self):
        BaseSelfModifyingRule.__init__(self)

    def _refresh(self, *args):
        mapping = {}
        mapping["alias"] = MockFunction(lambda : None)
        mapping["delete aliases"] = MockFunction(lambda: None)

class ChainAlias(AliasRule):
    pronunciation = "chain alias"

    def refresh(self, *args):
        mapping = {
            "alias":
                MockFunction(lambda: None),
            "delete aliases":
                MockFunction(lambda: None),
        }

class EclipseRule(MergeRule):
    pronunciation = "eclipse"

    mapping = {
            "open resource":                            MockKey("cs-r"),
            "open type":                                MockKey("cs-t"),
    }

class EclipseCCR(MergeRule):
    pronunciation = "eclipse jump"
    mwith = []
    mapping = {
            "Test 1": MockKey("c-l") + MockPause("50"),
            "Test 2": MockKey("c-l") + MockKey("right, cs-left"),

        }

eclipse_context = AppContext(
    executable="javaw", title="Eclipse") | AppContext(
        executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")

