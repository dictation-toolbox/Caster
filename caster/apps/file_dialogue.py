from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule,
                       Pause, Repeat, Text)
from dragonfly.actions.action_mimic import Mimic

from caster.lib import control, settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "[get] up [<n>]":
            R(Key("a-up"), rdescript="File Dialogue: Navigate up")*Repeat(extra="n"),
        "[get] back [<n>]":
            R(Key("a-left"), rdescript="File Dialogue: Navigate back")*Repeat(extra="n"),
        "[get] forward [<n>]":
            R(Key("a-right"), rdescript="File Dialogue: Navigate forward")*Repeat(extra="n"),
        "(files | file list)":
            R(Key("a-d, f6:3"), rdescript="File Dialogue: Files list"),
        "navigation [pane]":
            R(Key("a-d, f6:2"), rdescript="File Dialogue: Navigation pane"),
        "[file] name":
            R(Key("a-d, f6:5"), rdescript="File Dialogue: File name"),
    }
    extras = [IntegerRefST("n", 1, 10)]
    defaults = {
        "n": 1,
    }


context = AppContext(title="save file") | AppContext(title="save as") | AppContext(
    title="select folder") | AppContext(title="open file") | AppContext(title="select file")

grammar = Grammar("FileDialogue", context=context)
if settings.SETTINGS["apps"]["filedialogue"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
