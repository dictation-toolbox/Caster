from dragonfly import (Dictation, Grammar, IntegerRef, Key, MappingRule, Pause, Repeat,
                       Text)

from castervoice.lib import control, settings
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "up [<n>]":
            R(Key("a-up"), rdescript="File Dialogue: Navigate up")*Repeat(extra="n"),
        "back [<n>]":
            R(Key("a-left"), rdescript="File Dialogue: Navigate back")*Repeat(extra="n"),
        "forward [<n>]":
            R(Key("a-right"), rdescript="File Dialogue: Navigate forward")*
            Repeat(extra="n"),
        "search [<text>]":
            R(Key("c-l, tab") + Text("%(text)s"), rdescript="File Dialogue: Search"),
        "organize":
            R(Key("c-l, tab:2"), rdescript="File Dialogue: press 'organize' button"),
        "(left | navigation) pane":
            R(Key("c-l, tab:3"), rdescript="File dialogue: navigation pane"),
        "(center|file|files|folder) (list | pane)":
            R(Key("c-l, tab:4"), rdescript="File Dialogue: file list"),
        "files":
            R(Key("c-l, tab:4"), rdescript="File Dialogue: files list"),  # same as above
        "sort [headings]":
            R(Key("c-l, tab:5"), rdescript="File Dialogue: sort"),
        "[file] name":
            R(Key("c-l, tab:6"), rdescript="File Dialogue: filename"),
        "file type":
            R(Key("c-l, tab:7"), rdescript="File Dialogue: file type"),
    }
    extras = [IntegerRefST("n", 1, 10)]
    defaults = {
        "n": 1,
    }


dialogue_names = [
    "open",
    "select",
]

context = AppContext(title="save")
for name in dialogue_names:
    context = context | AppContext(title=name)

grammar = Grammar("FileDialogue", context=context)
if settings.SETTINGS["apps"]["filedialogue"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
