from dragonfly.os_dependent_mock import MockAction
from dragonfly import AppContext
from castervoice.lib.dfplus.merge.mergerule import MergeRule
import mock
import sys
import types

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

class Alias(MergeRule):
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

    extras = [
        IntegerRefST("n", 1, 1000),
        Boolean("back"),
    ]

eclipse_context = AppContext(
    executable="javaw", title="Eclipse") | AppContext(
        executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")

module_names = ['win32gui', 'win32con']
for module_name in module_names:
    bogus_module = types.ModuleType(module_name)
    sys.modules[module_name] = bogus_module
mock.patch.object('win3gui', 'GetForegroundWindow', return_value='testing')
