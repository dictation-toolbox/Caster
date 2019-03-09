# note: this module contains many more commands than anyone is likely to use.
# the user may want to disable some to avoid misfires

from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError, Playback, Mimic, Pause, WaitWindow)


from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.apps import reloader
from castervoice.apps import reloader

class VisualStudioRule(MergeRule):
    pronunciation = "visual studio"

    mapping = {
       
# could be made CCR
################################################
        "indent": Key("c-rbracket"),
        "out dent": Key("c-lbracket"),
        "copy line up": Key("sa-up"),
        "copy line down": Key("sa-down"),
        "move line down": Key("a-down"),
        "move line up": Key("a-up"),
        "match bracket": Key("cs-backslash"),
        "scroll line up": Key("c-up"),
        "scroll line down": Key("c-down"),
        "scroll page up": Key("a-pgup"),
        "scroll page down": Key("a-pgdown"),

        # multi-cursor and selection
        "add cursor above": Key("ca-up"),
        "add cursor below": Key("ca-down"),
        "tall cursor up": Key("csa-pgup"),
        "tall cursor down": Key("csa-pgdown"),
        "expand selection": Key("sa-right"),
        "shrink selection": Key("sa-left"),
        "select all [occurrences of] current selection": Key("c-l"),
        "select all [occurrences of] current word": Key("c-f2"),
        

# NONCCR
################################################

        # find and replace
        "replace": Key("c-h"),
        "find in files": Key("cs-f"),
        "replace in files": Key("cs-h"),
        "next find": Key("f3"),
        "previous find": Key("s-f3"),
        "select all occurrences of find match": Key("a-enter"),
        "add selection to next find match": Key("c-d"),
        "move last selection to next find match": Key("c-k, c-d"),
            # toggle case-sensitive/ regex / whole word alt +c/r/w I'm not sure what this means so I didn't make this command

        # languages editing
        "[go to] definition": Key("f12"),
        "peak definition": Key("a-f12"),
        "trigger parameter hands": Key("cs-space"),
        "mat (selection | that)": Key("c-k, c-f"), # format selection
        "(definition to side | side def)": Key("c-k, f12"), # open definition to the side
        "show references": Key("s-f12"),
        "rename symbol": Key("f2"),
        "(trim white | trim trailing white space)": Key("c-k, c-x"),
        "change file language": Key("c-k, m"),

        # editor management
        "close editor": Key("c-w"),
        "close folder": Key("c-k, f"),
        "split editor": Key("c-backslash"),
        "next [editor] group": Key("c-k, c-right"),
        "prior [editor] group": Key("c-k, c-left"),
        "move [editor] group left": Key("c-k, left"),
        "move [editor] group right": Key("c-k, right"),
        "focus <first_second_third> [group]": Key("c-%(first_second_third)s"),

        # collapsing
        "(fold | collapse) region": Key("cs-lbracket"),
        "(unfold | uncollapse) region": Key("cs-rbracket"),
        "(fold | collapse) [all] subregions": Key("c-k, c-lbracket"),
        "(unfold | uncollapse) [all] subregions": Key("c-k, c-rbracket"),
        "(fold | collapse) [all] regions": Key("c-k, c-0"),
        "(unfold | uncollapse) [all] regions": Key("c-k, c-j"),
        "toggle word wrap": Key("a-z"),

        # navigation
        "show all symbols": Key("c-t"),
        "go to symbol": Key("cs-o"),
        "show problems [panel]": Key("cs-m"),
        "next error": Key("f8"),
        "(prior | previous) error": Key("s-f8"),
        "toggle tab moves focus": Key("c-m"),

        # file management
        "new file": Key("c-n"),
        "new window": Key("c-w"),
        "close window": Key("a-f4"),
        "save as": Key("cs-s"),
        "save all": Key("c-k, s"),
        "next tab [<n>]":
            R(Key("c-pgdown"), rdescript="Visual Studio: Next Tab")*Repeat(extra="n"),
        "(prior tab | untab) [<n>]":
            R(Key("c-pgup"), rdescript="Visual Studio: Previous Tab")*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"), rdescript="Visual Studio: Close Tab")*Repeat(extra="n"),
        "(recent | er) tab [<n>]": Key("c-tab") * Repeat(extra='n'),
        "reopen tab": Key("cs-t"),
        "keep preview mode editor open": Key("c-k, enter"),
        "copy path": Key("c-k, p"),
        "reveal active file in Explorer": Key("c-k, r"),
        "show active file in new window": Key("c-k, o"),

        # display
        "[toggle] full screen":
            R(Key("sa-enter"), rdescript="Visual Studio: Fullscreen"),
        "[toggle] orientation": Key("sa-0"),
        "zoom in": Key("c-equal"),
        "zoom out": Key("c-minus"),
        "sidebar": Key("c-b"),
        "Explorer": Key("cs-e"),
        "search": Key("cs-f"),
        "source control": Key("cs-g"),
        "debug": Key("cs-d"),
        "extensions": Key("cs-x"),
        "replace and files": Key("cs-h"),
        "[toggle] search details": Key("cs-j"),
        "output panel": Key("cs-u"),
        "markdown preview": Key("cs-v"),
        "markdown preview side": Key("c-k, v"),
        "Zen mode": Key("c-k, z"), # note: use esc esc to exit

        # debug
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="Visual Studio: Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n"), rdescript="Visual Studio: Step Over"),
        "step into":
            R(Key("f11"), rdescript="Visual Studio: Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="Visual Studio: Step Out"),        
        "stopper": Key("s-f5"), # stop
        "continue": Key("f5"), # start/continue
        "show hover": Key("c-k, c-i"),
        "resume":
            R(Key("f5"), rdescript="Visual Studio: Resume"),
        "run tests":
            R(Key("c-r, t"), rdescript="Visual Studio: Run test(s)"),
        "run all tests":
            R(Key("c-r, a"), rdescript="Visual Studio: Run all tests"),
        "build solution":
            R(Key("cs-b"), rdescript="Visual Studio: Build solution"),
        "get latest [version]":
            R(Key("a-f, r, l"), rdescript="Visual Studio: Get Latest"),
        "(show | view) history":
            R(Key("a-f, r, h"), rdescript="Visual Studio: Show History"),
        "compare (files | versions)":
            R(Key("a-f, r, h"), rdescript="Visual Studio: Compare..."),
        "undo (checkout | pending changes)":
            R(Key("a-f, r, u"), rdescript="Visual Studio: Undo Pending Changes"),
        "[open] [go to] work item":
            R(Key("a-m, g"), rdescript="Visual Studio: Open Work Item"),
        "[add] [new] linked work item":
            R(Key("sa-l"), rdescript="Visual Studio: New Linked Work Item"),
        "(line | liner | go to line) <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter")),       
        
        # integrated terminal
        "[show] terminal": Key("c-backtick"),
        "new terminal": Key("cs-backtick"),
        "terminal scroll up": Key("c-up"),
        "terminal scroll down": Key("c-down"),
        "terminal page up": Key("s-pgup"),
        "terminal page down": Key("s-pgdown"),


        # I don't know what these are
        "(list | show) documents":
            R(Key("a-w, w"), rdescript="Visual Studio: List Documents"),
        "[focus] document (window | pane)":
            R(Key("a-w, w, enter"), rdescript="Visual Studio: Focus Document Pane"),
        "solution explorer":
            R(Key("ca-l"), rdescript="Visual Studio: Solution Explorer"),
        "team explorer":
            R(Key("c-backslash, c-m"), rdescript="Visual Studio: Team Explorer"),
        "source control explorer":
            R(Key("c-q") + Text("Source Control Explorer") + Key("enter"),
              rdescript="Visual Studio: Source Control Explorer"),
        "quick launch":
            R(Key("c-q"), rdescript="Visual Studio: Quick Launch"),
        

        # commenting
        "comment": R(Key("c-slash")),
        "comment line":
            R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Selection"),
        "comment block":
            R(Key("c-k, c-c"), rdescript="Visual Studio: Comment Block"),
        "(un | on) comment line":
            R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Selection"),
        "(un | on) comment block":
            R(Key("c-k/50, c-u"), rdescript="Visual Studio: Uncomment Block"),
        "(set | toggle) bookmark":
            R(Key("c-k, c-k"), rdescript="Visual Studio: Toggle Bookmark"),
        "next bookmark":
            R(Key("c-k, c-n"), rdescript="Visual Studio: Next Bookmark"),
        "prior bookmark":
            R(Key("c-k, c-p"), rdescript="Visual Studio: Previous Bookmark"),
        "collapse to definitions":
            R(Key("c-m, c-o"), rdescript="Visual Studio: Collapse To Definitions"),
        "toggle [section] outlining":
            R(Key("c-m, c-m"), rdescript="Visual Studio: Toggle Section Outlining"),
        "toggle all outlining":
            R(Key("c-m, c-l"), rdescript="Visual Studio: Toggle All Outlining"),
        
        
        # miscellaneous
        "black formatting": R(Key("sa-f")),           
        "run this line": Key("csa-l"),
        "join line": Key("csa-j"),
        "user settings": Key("c-plus"),
        "keyboard shortcuts": Key("c-k, c-s"),

        # requires gitlens extension
        "toggle blame": Key("cs-g, b"),
        "lens commit details": Key("cs-g, c"),
        "lens file history": Key("cs-g, h"),
        "lens repo status": Key("cs-g, s"),
        "toggle git lens": Key("cs-g, s-b"),

        # requires bookmark extension
        "mark prev": Key("ca-j"),
        "mark next": Key("ca-l"),

        # requires the keyboard-scroll extension (once=middle, twice=top, thrice=bottom)
        "center mass": Key("c-l"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
        Choice("first_second_third", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
            }),
        
    ]
    defaults = {"n": 1, "mim": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="code")
grammar = Grammar("Visual Studio", context=context)


if settings.SETTINGS["apps"]["visualstudio"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioRule())
    else:
        rule = VisualStudioRule(name="visualstudio")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
