# thanks to Casper for contributing commands to this.

from dragonfly import (Grammar, Context, AppContext, Dictation, Repeat, Function, Choice,
                       Mouse, Pause)

from castervoice.lib import settings, navigation, control
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger


def findNthToken(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute()
    else:
        Key("enter:%(n)d").execute()
        print("no? %(n)d")
    Key('escape').execute()


class VSCodeNonCcrRule(MergeRule):

    pronunciation = "Visual Studio Code Non Continuous"
    mapping = {

        # Moving around a file
        "[(go to | jump | jump to)] line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter")),
        "<action> [line] <ln1> [by <ln2>]":
            R(Function(navigation.action_lines)),

        "go back <n>":
            R(Key("a-left") * Repeat(extra='n')),
        "go forward [<n>]":
            R(Key("a-right")) * Repeat(extra="n"),

        # Display
        # note that most of these can be turned on/off with the same command
        "[toggle] full screen":
            R(Key("sa-enter")),
        "toggle orientation":
            R(Key("sa-0")),
        "zoom in [<n>]":
            R(Key("c-equal") * Repeat(extra='n')),
        "zoom out [<n>]":
            R(Key("c-minus") * Repeat(extra='n')),
        "sidebar":
            R(Key("c-b")),
        "explorer":
            R(Key("cs-e")),
        "source control":
            R(Key("cs-g")),
        "keyboard shortcuts":
            R(Key("c-k, c-s")),
        "key mappings":
            R(Key("c-k, c-s:2")),
        "settings":
            R(Key("a-f, p, s")),
        "snippets":
            R(Key("a-f, p, s:2")),
        "extensions":
            R(Key("cs-x")),
        "search details":
            R(Key("cs-j")),
        "output panel":
            R(Key("cs-u")),
        "markdown preview":
            R(Key("cs-v")),
        "markdown preview side":
            R(Key("c-k, v")),
        "Zen mode":
            # note: use esc esc to exit
            R(Key("c-k, z")),

        # File Management
        "[open] command palette":
            R(Key("cs-p")),
        "(open [file] | go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s")),
        "Save and close":
            R(Key("c-s/10, c-w")),
        "new file":
            R(Key("c-n")),
        "new window":
            R(Key("cs-n")),
        "close window":
            R(Key("a-f4")),
        "close workspace":
            R(Key("c-k, f")),
        "close editor":
            R(Key("c-f4")),
        "save as":
            R(Key("cs-s")),
        "save all":
            R(Key("c-k, s")),
        "next tab [<n>]":
            R(Key("c-pgdown") * Repeat(extra='n')),
        "previous tab [<n>]":
            R(Key("c-pgup") * Repeat(extra='n')),
        "close tab [<n>]":
            R(Key("c-f4/20") * Repeat(extra='n')),
        "(recent | R) tab [<n>]":
            R(Key("c-tab") * Repeat(extra='n')),
        "reopen tab [<n>]":
            R(Key("cs-t") * Repeat(extra='n')),
        "Exit preview":
            R(Key("space, c-z")),
        "keep preview open":
            R(Key("c-k, enter")),
        "copy path":
            R(Key("c-k, p")),
        "windows explorer here":
            R(Key("c-k, r")),
        "show active file in new window":
            R(Key("c-k, o")),

        # Search
        "(search | find)":
            R(Key("c-f")),
        "replace":
            R(Key("c-h")),
        "find in files":
            R(Key("cs-f")),
        "replace in files":
            R(Key("cs-h")),
        "next find":
            R(Key("f3")),
        "(prior | previous) find":
            R(Key("s-f3")),
        "select all occurrences":
            R(Key("a-enter")),

        "toggle case sensitive":
            R(Key("a-c")),
        "toggle regex":
            R(Key("a-r")),
        "toggle whole word":
            R(Key("a-w")),

        "(find | jump [to]) next <text>":
            R(Function(findNthToken, n=1, direction="forward")),
        "(find | jump [to]) previous <text>":
            R(Function(findNthToken, n=1, direction="reverse")),
        "show all symbols":
            R(Key("c-t")),
        "go to symbol":
            R(Key("cs-o")),

        # Editor Management
        "close editor":
            R(Key("c-w")),
        "close folder":
            R(Key("c-k, f")),
        "split editor":
            R(Key("c-backslash")),
        "next pane":
            R(Key("c-k, c-right")),
        "(prior | previous | un) pane":
            R(Key("c-k, c-right")),
        "shift group left":
            R(Key("c-k, left")),
        "shift group left":
            R(Key("c-k, right")
              ),
        "<nth> tab":
            R(Key("c-%(nth)s")),

        # Languages Editing
        "go to definition":
            R(Key("f12")),
        "go to required definition":
            R(Key("c-f12:2, c-right:5, left/50, f12")),
        "peak definition":
            R(Key("a-f12")),
        "trigger parameter hints":
            R(Key("cs-space")),
        "format that":
            R(Key("c-k, c-f")),
        "(definition to side | side def)":
            R(Key("c-k, f12")),
        "show references":
            R(Key("s-f12")),
        "rename symbol":
            R(Key("f2")),
        "(trim white)":
            R(Key("c-k, c-x")),
        "change file language":
            R(Key("c-k, m")),

        # Debugging
        "debug":
            R(Key("cs-d")),
        "[toggle] breakpoint":
            R(Key("f9")),
        "step over [<n>]":
            R(Key("f10/50") * Repeat(extra='n')),
        "step into":
            R(Key("f11")),
        "step out [of]":
            R(Key("s-f11")),
        "resume":
            R(Key("f5")),
        "stopper":
            R(Key("s-f5")),
        "continue":
            R(Key("f5")),
        "show hover":
            R(Key("c-k, c-i")),
        "[show] problems [panel]":
            R(Key("cs-m")),
        "next error":
            R(Key("f8")),  # doesn't seem to be working properly
        "(prior | previous) error":
            R(Key("s-f8")),
        "toggle tab moves focus":
            R(Key("c-m")),

        # Integrated Terminal
        "[show] terminal":
            R(Key("c-backtick")),
        "new terminal":
            R(Key("cs-backtick")),
        "terminal scroll up":
            R(Key("c-up")),
        "terminal scroll down":
            R(Key("c-down")),
        "terminal page up":
            R(Key("s-pgup")),
        "terminal page down":
            R(Key("s-pgdown")),

        # Collapsing
        "(fold | collapse) region":
            R(Key("cs-lbracket")),
        "(unfold | uncollapse) region":
            R(Key("cs-rbracket")),
        "(fold | collapse) [all] subregions":
            R(Key("c-k, c-lbracket")),
        "(unfold | uncollapse) [all] subregions":
            R(Key("c-k, c-rbracket")),
        "(fold | collapse) [all] regions":
            R(Key("c-k, c-0")),
        "(unfold | uncollapse) [all] regions":
            R(Key("c-k, c-j")),
        "toggle word wrap":
            R(Key("a-z")),

        "run this line":
            R(Key("csa-l")),
        "join line":
            R(Key("csa-j")),

        # requires gitlens extension
        "toggle blame":
            R(Key("cs-g, b")),
        "lens commit details":
            R(Key("cs-g, c")),
        "lens file history":
            R(Key("cs-g, h")),
        "lens repo status":
            R(Key("cs-g, s")),
        "toggle git lens":
            R(Key("cs-g, s-b")),

        # requires bookmark extension
        "mark (prev | prior | previous)":
            R(Key("ca-j")),
        "mark next":
            R(Key("ca-l")),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("ln1", 1, 1000),
        IntegerRefST("ln2", 1, 1000),
        IntegerRefST("n", 1, 1000),
        Choice("action", navigation.actions),
        Choice(
            "nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
            }),
    ]
    defaults = {"n": 1, "ln2": "",  "mim": "", "text": ""}


class VSCodeCcrRule(MergeRule):
    pronunciation = "visual studio code continuous"
    mwith = CCRMerger.CORE
    non = VSCodeNonCcrRule

    mapping = {
        # Note: If you get the bad grammar grammar too complex error, move some of these commands into the non-CCR rule
        # cursor/line navigation
        "scroll up [<n>]":
            R(Key("c-up") * Repeat(extra='n')),
        "scroll down [<n>]":
            R(Key("c-down") * Repeat(extra='n')),
        "scroll page up [<n>]":
            R(Key("a-pgup") * Repeat(extra='n')),
        "scroll page down [<n>]":
            R(Key("a-pgdown") * Repeat(extra='n')),
        "(unindent|outdent) [<n>]":
            R(Key("s-tab") * Repeat(extra='n')),
        "comment line":
            R(Key("c-slash")),
        "block comment":
            R(Key("sa-a")),
        # Multi-cursor and selection
        "cursor above [<n>]":
            R(Key("ca-up") * Repeat(extra='n')),
        "cursor below [<n>]":
            R(Key("ca-down") * Repeat(extra='n')),
        "remove cursor":
            R(Key("csa-down")),  # not sure if this command works always; also try csa-up
        # csa-down/up seems to work sometimes to remove 1 of the cursors
        # but I don't really understand how this works
        "tall cursor up":
            R(Key("csa-pgup")),
        "tall cursor down":
            R(Key("csa-pgdown")),
        # Command below requires "brackets select" extension for VS code
        "select [in] brackets [<n>]":
            R(Key("ca-a") * Repeat(extra='n')
              )*Repeat(extra='n'),
        "all current selection":
            R(Key("c-l")),
        "all current word":
            R(Key("c-f2")),
        "select next [<n>]":
            R(Key("c-f3") * Repeat(extra='n')),
        "go to next [<n>]":
            R(Key("sa-right/2, c-f3, c-left/2, escape") * Repeat(extra='n')),
        # may or may not want the escape afterwards to close the find box
        # note the above command might sometimes be off by one so you have to say one higher
        # than what you mean e.g. if the cursor is at the beginning of the word rather
        # than in the middle or end, you will have to say "next word two" to get to the next word
        "select prior [<n>]":
            R(Key("cs-f3")),
        "go to prior [<n>]":
            R(Key("sa-right/2, cs-f3, c-left/2, escape") * Repeat(extra='n')),
        # may or may not want the escape afterwards to close the find box
        "cursor all":
            R(Key("cs-l")),
        "next cursor [<n>]":
            R(Key("c-d") * Repeat(extra='n')),
        "indent [<n>]":
            R(Key("tab") * Repeat(extra='n')),
        "hard delete [<n>]":
            R(Key("s-del")),
        "copy line up [<n>]":
            R(Key("sa-up") * Repeat(extra='n')),
        "copy line up [<n>]":
            R(Key("sa-down") * Repeat(extra='n')),
        "switch line down [<n>]":
            R(Key("a-down") * Repeat(extra='n')),
        "switch line up [<n>]":
            R(Key("a-up") * Repeat(extra='n')),
        "match bracket":
            R(Key("cs-backslash")),

        # commands for selecting between parable characters using "quick and simple text selection" VScode extension (required)
        # repetition of these commands by saying the number expands the selection to include the text between the next (i.e. outer) set of parable characters of the given type
        "select between <between_parables> [<n>]":
            R(Key("c-k, %(between_parables)s") * Repeat(extra='n')
              ),
        "select around <around_parables> [<n>]":
            R(Key("c-k, %(around_parables)s") * Repeat(extra='n')
              ),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 10),
        Choice("between_parables", {
            "prekris": "lparen",
            "brax": "lbracket",
            "curly": "lbrace",
            "angle": "langle",
            "single": "squote",
            "quote": "dquote",
        }),
        Choice("around_parables", {
            "prekris": "rparen",
            "brax": "rbracket",
            "curly": "rbrace",
            "angle": "rangle",
        }),
    ]

    defaults = {"n": 1, "mim": "", "text": ""}



# ---------------------------------------------------------------------------

# initialise the rule.
context = AppContext(title="Visual Studio Code", executable="code")
grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VSCodeCcrRule())
    else:
        control.nexus().merger.add_app_rule(VSCodeCcrRule(), context)
