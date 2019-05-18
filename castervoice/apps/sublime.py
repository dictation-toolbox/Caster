from dragonfly import (Choice, Dictation, Grammar, Repeat, Function)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.temporary import Store, Retrieve
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

def action_lines(action, n, nn):
    if nn:
        num_lines = int(nn)-int(n)+1 if nn>n else int(n)-int(nn)+1
        top_line = min(int(nn), int(n))
    else:
        num_lines = 1
        top_line = int(n)
    command = Key("c-g") + Text(str(top_line)) + Key("enter, s-down:" + str(num_lines) + ", " + action)
    command.execute()

class SublimeRule(MergeRule):
    pronunciation = "sublime"

    mapping = {
        "new file":
            R(Key("c-n"), rdescript="Sublime: New File"),
        "new window":
            R(Key("cs-n"), rdescript="Sublime: New Window"),
        "open file":
            R(Key("c-o"), rdescript="Sublime: Open File"),
        "open folder":
            R(Key("f10, f, down:2, enter"), rdescript="Sublime: Open Folder"),
        "open recent":
            R(Key("f10, f, down:3, enter"), rdescript="Sublime: Open Recent"),
        "save as":
            R(Key("cs-s"), rdescript="Sublime: Save As"),
        #
        "comment line":
            R(Key("c-slash"), rdescript="Sublime: Comment Line"),
        "comment block":
            R(Key("cs-slash"), rdescript="Sublime: Comment Block"),
        "outdent lines":
            R(Key("c-lbracket"), rdescript="Sublime: Outdent Lines"),
        "join lines":
            R(Key("c-j"), rdescript="Sublime: Join Lines"),
        "match bracket":
            R(Key("c-m"), rdescript="Sublime: Match Current Bracket"),
        #
        "(select | sell) all":
            R(Key("c-a"), rdescript="Sublime: Select All"),
        "(select | sell) scope [<n2>]":
            R(Key("cs-space"), rdescript="Sublime: Select Scope")*Repeat(extra="n2"),
        "(select | sell) brackets [<n2>]":
            R(Key("cs-m"), rdescript="Sublime: Select Brackets")*Repeat(extra="n2"),
        "(select | sell) indent":
            R(Key("cs-j"), rdescript="Sublime: Select Indent"),
        #
        "find":
            R(Key("c-f"), rdescript="Sublime: Find"),
        "get all":
            R(Key("a-enter"), rdescript="Sublime: Get All"),
        "replace":
            R(Key("c-h"), rdescript="Sublime: Find And Replace"),
        "edit lines":
            R(Key("cs-l"), rdescript="Sublime: Edit Selected Lines"),
        "edit next [<n3>]":
            R(Key("c-d/10"), rdescript="Sublime: Edit Next n")*Repeat(extra="n3"),
        "edit up [<n3>]":
            R(Key("ac-up"), rdescript="Sublime: Edit Up n")*Repeat(extra="n3"),
        "edit down [<n3>]":
            R(Key("ac-down"), rdescript="Sublime: Edit Down n")*Repeat(extra="n3"),
        "edit all":
            R(Key("a-f3"), rdescript="Sublime: Edit All Instances"),
        #
        "transform upper":
            R(Key("c-k, c-u"), rdescript="Sublime: Transform Upper"),
        "transform lower":
            R(Key("c-k, c-l"), rdescript="Sublime: Transform Lower"),
        #
        "line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter"), rdescript="Sublime: Line n"),
        "<action> line <n> [to <nn>]":
            R(Function(action_lines), rdescript="Sublime: Action lines"),
        "go to file":
            R(Key("c-p"), rdescript="Sublime: Go to file"),
        "go to <dict> [<filetype>]":
            R(Key("c-p") + Text("%(dict)s" + "%(filetype)s") + Key("enter"), rdescript="Sublime: go to <dict> [<filetype>]"),
        "go to word":
            R(Key("c-semicolon"), rdescript="Sublime: Go to word"),
        "go to symbol":
            R(Key("c-r"), rdescript="Sublime: Go to symbol"),
        "go to [symbol in] project":
            R(Key("cs-r"), rdescript="Sublime: Go to symbol in project"),

        "go to that":
            R(Store() + Key("cs-r") + Retrieve() + Key("enter"), rdescript="Sublime: Go to that"),
        "find that in project":
            R(Store() + Key("cs-f") + Retrieve() + Key("enter"), rdescript="Sublime: Find that in project"),
        "find that":
            R(Store() + Key("c-f") + Retrieve() + Key("enter"), rdescript="Sublime: Find that"),

        "command pallette":
            R(Key("cs-p"), rdescript="Sublime: Command Pallette"),
        #
        "fold":
            R(Key("cs-lbracket"), rdescript="Sublime: Fold"),
        "unfold":
            R(Key("cs-rbracket"), rdescript="Sublime: Unfold"),
        "unfold all":
            R(Key("c-k, c-j"), rdescript="Sublime: Unfold All"),
        "fold [level] <n2>":
            R(Key("c-k, c-%(n2)s"), rdescript="Sublime: Fold Level 1-9"),
        #
        "full screen":
            R(Key("f11"), rdescript="Sublime: Fullscreen"),
        "toggle side bar":
            R(Key("c-k, c-b"), rdescript="Sublime: Toggle sidebar"),
        "show key bindings":
            Key("f10, p, right, k"),
        "zoom in [<n2>]":
            R(Key("c-equal"), rdescript="Sublime: Zoom in")*Repeat(extra="n2"),
        "zoom out [<n2>]":
            R(Key("c-minus"), rdescript="Sublime: Zoom out")*Repeat(extra="n2"),
        #
        "(set | add) bookmark":
            R(Key("c-f2"), rdescript="Sublime: Set Bookmark"),
        "next bookmark":
            R(Key("f2"), rdescript="Sublime: Next Bookmark"),
        "previous bookmark":
            R(Key("s-f2"), rdescript="Sublime: Previous Bookmark"),
        "clear bookmarks":
            R(Key("cs-f2"), rdescript="Sublime: Clear Bookmarks"),
        #
        "build it":
            R(Key("c-b"), rdescript="Sublime: Build It"),
        #
        "record macro":
            R(Key("c-q"), rdescript="Sublime: Record Macro"),
        "play [back] macro [<n3>]":
            R(Key("cs-q/10"), rdescript="Sublime: Play Macro")*Repeat(extra="n3"),
        "(new | create) snippet":
            R(Key("ac-n"), rdescript="Sublime: New Snippet"),
        #
        "close tab":
            R(Key("c-w"), rdescript="Sublime: Close tab"),
        "next tab":
            R(Key("c-pgdown"), rdescript="Sublime: Next tab"),
        "previous tab":
            R(Key("c-pgup"), rdescript="Sublime: Previous tab"),
        "<nth> tab":
            R(Key("a-%(nth)s"), rdescript="Sublime: <nth> tab"),
        "column <cols>":
            R(Key("as-%(cols)s"), rdescript="Sublime: Column"),
        "focus <panel>":
            R(Key("c-%(panel)s"), rdescript="Sublime: Focus Panel n"),
        "move <panel>":
            R(Key("cs-%(panel)s"), rdescript="Sublime: Move File to Panel n"),
        #
        "open terminal":
            R(Key("cs-t"), rdescript="Sublime: Open Terminal Here"),

    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("nn", 1, 1000),
        IntegerRefST("n2", 1, 9),
        IntegerRefST("n3", 1, 21),
        Choice("action", {
            "select": "",
            "copy": "c-c",
            "cut": "c-x",
            "delete": "backspace",
            "replace": "c-v",
            }),
        Choice("nth", {
            "first"  : "1",
            "second" : "2",
            "third"  : "3",
            "fourth" : "4",
            "fifth"  : "5",
            "sixth"  : "6",
            "seventh": "7",
            "eighth" : "8",
            "ninth"  : "9",
            }),
        Choice("cols", {
            "one": "1",
            "two": "2",
            "three": "3",
            "grid": "5",
        }),
        Choice("panel", {
            "one": "1",
            "left": "1",
            "two": "2",
            "right": "2",
        }),
        Choice("filetype", {
            "pie | python": "py",
            "mark [down]": "md",
            "tech": "tex",
            "tommel": "toml",
        }),
    ]
    defaults = {
        "nn": None,
        "n2": 1,
        "n3": 1,
        "filetype": "",
    }


#---------------------------------------------------------------------------

context = AppContext(executable="sublime_text", title="Sublime Text")
grammar = Grammar("Sublime", context=context)

if settings.SETTINGS["apps"]["sublime"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(SublimeRule())
    else:
        rule = SublimeRule(name="sublime")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
