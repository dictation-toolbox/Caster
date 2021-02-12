from dragonfly import Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class IERule(MappingRule):
    mapping = {
        "address bar":
            R(Key("a-d")),
        "new folder":
            R(Key("cs-n")),
        "new file":
            R(Key("a-f, w, t")),
        "(show | file | folder) properties":
            R(Key("a-enter")),
        "get up":
            R(Key("a-up")),
        "get back":
            R(Key("a-left")),
        "get forward":
            R(Key("a-right")),
        "search [<text>]":
            R(Key("a-d, tab:1") + Text("%(text)s")),
        "(navigation | nav | left) pane":
            R(Key("a-d, tab:2")),
        "(center pane | (file | folder) (pane | list))":
            R(Key("a-d, tab:3")),
            # for the sort command below,
            # once you've selected the relevant heading for sorting using the arrow keys, press enter
        "sort [headings]":
            R(Key("a-d, tab:4")),

    }
    extras = [
        Dictation("text"),
        ShortIntegerRef("n", 1, 1000),
    ]
    defaults = {"n": 1}


def get_rule():
    return IERule, RuleDetails(name="explorer", executable="explorer")
