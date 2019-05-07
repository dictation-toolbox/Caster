from dragonfly.os_dependent_mock import MockAction
from castervoice.lib.dfplus.merge.mergerule import MergeRule

Text = MockAction
Key = MockAction
Function = MockAction

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
