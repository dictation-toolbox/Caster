from dragonfly.os_dependent_mock import Text, Key
from castervoice.lib.dfplus.merge.mergerule import MergeRule


class Python(MergeRule):
    mapping = {
        "sue iffae": Text("if :") + Key("left"),
        "yield": Text("yield "),

    }

class Java(MergeRule):
    mapping = {
        "sue iffae": Text("if ():") + Key("left:2"),
    }

class Bash(MergeRule):
    mapping = {
        "sue iffae": Text("[[  ]]") + Key("left/5:3"),
    }
