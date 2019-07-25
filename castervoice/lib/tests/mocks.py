import mock
import sys
import types

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
from castervoice.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from castervoice.lib.dfplus.merge.mergerule import MergeRule

Text = MockAction
Key = MockAction
Function = MockAction
Pause = MockAction

class Python(MergeRule):
    mapping = {
        "iffae": Text("if :") + Key("left"),
        "yield": Text("yield "),

    }

class Java(MergeRule):
    mapping = {
        "iffae": Text("if () {") + Key("enter,up,left"),
        "dock string": Text("/***/") + Key("left,left,enter"),
    }

class Javascript(MergeRule):
    mapping = {
        "iffae": Text("if () {") + Key("enter,up,left"),
        "tick string": Text("``") + Key("left"),
    }

class Bash(MergeRule):
    mapping = {
        "iffae":
            Text("if [[  ]]; ") + Key("left/5:5"),
        "key do":
            Text("do"),
    }

class AliasRule(SelfModifyingRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)

class Alias(AliasRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)

    def refresh(self, *args):
        mapping = {}
        mapping["alias"] = Function(lambda : None)
        mapping["delete aliases"] = Function(lambda: None)

class ChainAlias(AliasRule):
    pronunciation = "chain alias"

    def refresh(self, *args):
        mapping = {
            "alias":
                Function(lambda: None),
            "delete aliases":
                Function(lambda: None),
        }

class EclipseRule(MergeRule):
    pronunciation = "eclipse"

    mapping = {
            "open resource":                            Key("cs-r"),
            "open type":                                Key("cs-t"),
    }

class EclipseCCR(MergeRule):
    pronunciation = "eclipse jump"
    mwith = []
    mapping = {
            "Test 1":                         Key("c-l") + Pause("50"),
            "Test 2":                     Key("c-l")+Key("right, cs-left"),

        }

eclipse_context = AppContext(
    executable="javaw", title="Eclipse") | AppContext(
        executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")

