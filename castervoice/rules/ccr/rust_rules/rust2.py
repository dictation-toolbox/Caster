from dragonfly import MappingRule, Choice

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class RustNon(MappingRule):
    mapping = {
        "macro format string":
            R(Text("format!()") + Key("left")),
        "macro panic":
            R(Text("panic!()") + Key("left")),
        "macro assertion":
            R(Text("assert_eq!()") + Key("left")),
        "macro debug":
            R(Text("dbg!(&)") + Key("left")),
        "ternary":
            R(Text("if TOKEN == TOKEN { TOKEN } else { TOKEN }")),
        "function [<return>]":
            R(Text("fn TOKEN(TOKEN)%(return)s{}")),
        "infinite loop":
            R(Text("loop {}") + Key("left")),
        "unwrap":
            R(Text(".unwrap()"))
    }
    extras = [
        Choice("return", {"return": " -> TOKEN "}),
    ]
    defaults = {"return": " "}


def get_rule():
    return RustNon, RuleDetails(name="rust companion")
