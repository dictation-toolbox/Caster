from dragonfly import Repeat, Dictation, MappingRule, Mimic

from castervoice.lib.actions import Key, Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib import settings

file_dialogue_wait = "40"
if settings.settings(["miscellaneous", "file_dialogue_wait"]):
    file_dialogue_wait = str(settings.SETTINGS["miscellaneous"]["file_dialogue_wait"])

class ExplorerRule(MappingRule):
    mapping = {
        "address bar":
            R(Key("escape/" + file_dialogue_wait + ", c-l")),
        "new folder":
            R(Key("escape, c-l, tab/" + file_dialogue_wait + ":3, cs-n")),
        "new file":
            R(Key("escape, a-h, w")),
        "(show | file | folder) properties":
            R(Key("escape, a-enter")),
        "get up [<n>]":
            R(Key("escape, a-up"))*Repeat(extra="n"),
        "get back [<n>]": 
            R(Key("escape, a-left"))*Repeat(extra="n"),
        "get forward [<n>]": 
            R(Key("escape, a-right"))*Repeat(extra="n"),
        "search [<text>]":
            R(Key("escape, c-l, tab/" + file_dialogue_wait + "") + Text("%(text)s")),
        "(navigation | nav | left) pane":
            R(Key("escape/10, c-l, tab/" + file_dialogue_wait + ":2")),
        "(center|file|files|folder) (list | pane)":
            R(Key("escape/10, c-l, tab/" + file_dialogue_wait + ":3")),
            # for the sort command below,
            # once you've selected the relevant heading for sorting using the arrow keys, press enter
        "sort [headings]":
            R(Key("escape/10, c-l, tab/" + file_dialogue_wait + ":3, tab:1")),
    }
    extras = [IntegerRefST("n", 1, 10), Dictation("text")]
    defaults = {
        "n": 1,
    }

def get_rule():
    return ExplorerRule, RuleDetails(name="explorer", executable="explorer")
