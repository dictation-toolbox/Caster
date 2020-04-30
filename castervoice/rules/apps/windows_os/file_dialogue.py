from dragonfly import Repeat, Dictation, MappingRule

from castervoice.lib.actions import Key

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib import settings

file_dialogue_wait = "40"
if settings.settings(["miscellaneous", "file_dialogue_wait"]):
    file_dialogue_wait = str(settings.SETTINGS["miscellaneous"]["file_dialogue_wait"])


class FileDialogueRule(MappingRule):
    mapping = {
        "address bar":
            R(Key("c-l")),
        "new folder":
            R(Key("c-l, tab/" + file_dialogue_wait + ":3, tab:1, cs-n")),
        "(show | file | folder) properties":
            R(Key("a-enter")),
        "get up [<n>]": 
            R(Key("a-up"))*Repeat(extra="n"),
        "get back [<n>]":
            R(Key("a-left"))*Repeat(extra="n"),
        "get forward [<n>]": 
            R(Key("a-right"))*Repeat(extra="n"),
        "search [<text>]": 
            R(Key("c-l, tab/" + file_dialogue_wait + "") + Text("%(text)s")),
        "organize": 
            R(Key("c-l, tab/" + file_dialogue_wait + ":2, down/" + file_dialogue_wait + ":2")),
        "(navigation | nav | left) pane":
            R(Key("c-l, tab/" + file_dialogue_wait + ":3")),
        "(center|file|files|folder) (list | pane)": 
            R(Key("c-l, tab/" + file_dialogue_wait + ":3, tab:1")),
        "sort [headings]": 
            R(Key("c-l, tab/" + file_dialogue_wait + ":3, tab:2")),
        "file name": 
            R(Key("a-n")),
        "file type": 
            R(Key("c-l, tab/" + file_dialogue_wait + ":3, tab:4")),
    }
    extras = [IntegerRefST("n", 1, 10), Dictation("text")]
    defaults = {
        "n": 1,
    }


def get_rule():
    return FileDialogueRule, RuleDetails(name="file dialogue", title=["open", "save", "select"])
