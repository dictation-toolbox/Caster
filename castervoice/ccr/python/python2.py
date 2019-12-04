from dragonfly import MappingRule

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class PythonNon(MappingRule):
    mapping = {
        "with":
            R(Text("with ")),
        "open file":
            R(Text("open('filename','r') as f:")),
        "read lines":
            R(Text("content = f.readlines()")),
        "try catch":
            R(
                Text("try:") + Key("enter:2/10, backspace") + Text("except Exception:") +
                Key("enter")),
    }


def get_rule():
    return PythonNon, RuleDetails("python companion")
