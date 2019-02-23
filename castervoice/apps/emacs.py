from dragonfly import (Grammar, Dictation)

from caster.lib import control
from caster.lib import settings
from caster.lib.actions import Key
from caster.lib.context import AppContext
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class EmacsRule(MergeRule):
    pronunciation = "E max"

    mapping = {
        "open file":
            R(Key("c-x, c-f"), rdescript="Emacs: Open File"),
        "save file":
            R(Key("c-x, c-s"), rdescript="Emacs: Save File"),
        "save as":
            R(Key("c-x, c-w"), rdescript="Emacs: Save As"),
        "save all":
            R(Key("c-x, s"), rdescript="Emacs: Save All"),
        "revert to file":
            R(Key("c-x, c-v"), rdescript="Emacs: Revert To File"),
        "revert buffer":
            R(Key("a-x"), rdescript="Revert Buffer"),
        "close buffer":
            R(Key("c-x, c-c"), rdescript="Close Buffer"),
        "undo":
            R(Key("c-underscore"), rdescript="Emacs: Undo"),
        "begin selection":
            R(Key("c-space"), rdescript="Emacs: Begin Selection"),
        "cancel selection":
            R(Key("c-g"), rdescript="Emacs: Cancel Selection"),
        "cut selection":
            R(Key("c-w"), rdescript="Emacs: Cut Selection"),
        "paste":
            R(Key("c-y"), rdescript="Emacs: Paste"),
        "copy number <n>":
            R(Key("c-x, r, s, %(n)d"), rdescript="Emacs: Copy Number"),
        "paste number <n>":
            R(Key("c-x, r, i, %(n)d"), rdescript="Emacs: Paste Number"),
        # delete
        "forward delete":
            R(Key("c-delete"), rdescript="Emacs: Forward Delete"),
        "delete word":
            R(Key("a-delete"), rdescript="Emacs: Delete Word"),
        "forward delete word":
            R(Key("a-d"), rdescript="Emacs: Forward Delete Word"),
        "word forward":
            R(Key("a-f"), rdescript="Emacs: Word Forward"),
        "word backward":
            R(Key("a-b"), rdescript="Emacs: Word Backward"),
        "line forward":
            R(Key("c-a"), rdescript="Emacs: Line Forward"),
        "line backward":
            R(Key("c-e"), rdescript="Emacs: Line Backward"),
        "paragraph forward":
            R(Key("a-lbrace"), rdescript="Emacs: Paragraph Forward"),
        "paragraph backward":
            R(Key("a-rbrace"), rdescript="Emacs: Paragraph Backward"),
        "document forward":
            R(Key("a-langle"), rdescript="Emacs: Document Forward"),
        "document backward":
            R(Key("a-rangle"), rdescript="Emacs: Document Backward"),
        "C function forward":
            R(Key("ac-a"), rdescript="Emacs: C Function Forward"),
        "C function backward":
            R(Key("ac-e"), rdescript="Emacs: C Function Forward"),
        "incremental search":
            R(Key("c-s"), rdescript="Emacs: Incremental Search"),
        "incremental reverse":
            R(Key("c-r"), rdescript="Emacs: Incremental Reverse"),
        "interactive search":
            R(Key("a-percent"), rdescript="Emacs: Interactive Search"),
        "go to line <n>":
            R(Key("a-x, %(n)d"), rdescript="Emacs: Go To Line"),
        "prior bracket":
            R(Key("escape:down, c-b, escape:up"), rdescript="Emacs: Prior Bracket"),
        "next bracket":
            R(Key("escape:down, c-f, escape:up"), rdescript="Emacs: Next Bracket"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="emacs", title="emacs")
grammar = Grammar("emacs", context=context)

if settings.SETTINGS["apps"]["emacs"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(EmacsRule())
    else:
        rule = EmacsRule(name="emacs")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
