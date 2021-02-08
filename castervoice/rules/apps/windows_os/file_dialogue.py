from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class FileDialogueRule(MappingRule):
    mapping = {
        "up [<n>]": R(Key("a-up"))*Repeat(extra="n"),
        "back [<n>]": R(Key("a-left"))*Repeat(extra="n"),
        "forward [<n>]": R(Key("a-right"))*Repeat(extra="n"),
        "search [<text>]": R(Key("c-l, tab") + Text("%(text)s")),
        "organize": R(Key("c-l, tab:2")),
        "(left | navigation) pane": R(Key("c-l, tab:3")),
        "(center|file|files|folder) (list | pane)": R(Key("c-l, tab:4")),
        "sort [headings]": R(Key("c-l, tab:5")),
        "[file] name": R(Key("a-n")),
        "file type": R(Key("c-l, tab:7")),

    }
    extras = [ShortIntegerRef("n", 1, 10), Dictation("text")]
    defaults = {
        "n": 1,
    }


def get_rule():
    return FileDialogueRule, RuleDetails(name="file dialogue", title=["open", "save", "select"])
