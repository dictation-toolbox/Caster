# thanks to Casper for contributing commands to this.

from dragonfly import (Grammar, Context, AppContext, Dictation, Repeat, Function, Choice,
                       Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
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


class VSCodeCcrRule(MergeRule):
    #pronunciation = "visual studio code continuous"
    mwith = CCRMerger.CORE

    mapping = {
        # note: if you get the bad grammar grammar too complex error, move some of these commands into the non-CCR rule
        # cursor/line navigation
        "scroll up [<n>]":
            R(Key("c-up"), rdescript="scroll up one line at a time")*Repeat(extra='n'),
        "scroll down [<n>]":
            R(Key("c-down"), rdescript="scroll down one line at a time")*
            Repeat(extra='n'),
        "scroll page up [<n>]":
            R(Key("a-pgup"), rdescript="scroll up one page up at a time")*
            Repeat(extra='n'),
        "scroll page down [<n>]":
            R(Key("a-pgdown"), rdescript="scroll down one page down at a time")*
            Repeat(extra='n'),
        "(Unindent|outdent) [<n>]":
            R(Key("s-tab"), rdescript="Visual Studio Code: Unindent")*Repeat(extra="n"),
        "Comment line":
            R(Key("c-slash"), rdescript="Visual Studio Code: Line Comment"),
        "Block comment":
            R(Key("sa-a"), rdescript="Visual Studio Code: Block Comment"),

        # multi-cursor and selection
        "cursor above [<n>]":
            R(Key("ca-up"), rdescript="insert cursor above")*Repeat(extra='n'),
        "cursor below [<n>]":
            R(Key("ca-down"), rdescript="insert cursor above")*Repeat(extra='n'),
        "remove cursor":
            R(Key("csa-down"),
              rdescript=""),  #not sure if this command works always; also try csa-up
        # csa-down/up seems to work sometimes to remove 1 of the cursors
        # but I don't really understand how this works
        "tall cursor up":
            R(Key("csa-pgup"), rdescript="add cursors all the way up"),
        "tall cursor down":
            R(Key("csa-pgdown"), rdescript="add cursors all the way down"),

        # # command below requires "brackets select" extension for VS code
        "select [in] brackets [<n>]":
            R(Key("ca-a"),
              rdescript=
              "select in between parable punctuation inclusive using 'brackets select' extension"
              )*Repeat(extra='n'),
        "all current selection":
            R(Key("c-l"), rdescript="select all occurrences of current selection"),
        "all current word":
            R(Key("c-f2"), rdescript="select all occurrences of current word"),
        "select next [<n>]":
            R(Key("c-f3"), rdescript="select next occurrence of current word")*
            Repeat(extra='n'),
        "go to next [<n>]":
            R(Key("sa-right/2, c-f3, c-left/2, escape"),
              rdescript="go to next occurrence of current word")*Repeat(extra='n'),
        # may or may not want the escape afterwards to close the find box
        # note the above command might sometimes be off by one so you have to say one higher
        # than what you mean e.g. if the cursor is at the beginning of the word rather
        # than in the middle or end, you will have to say "next word two" to get to the next word
        "select prior [<n>]":
            R(Key("cs-f3"), rdescript="select prior occurrence of current word")*
            Repeat(extra='n'),
        "go Sueto prior [<n>]":
            R(Key("sa-right/2, cs-f3, c-left/2, escape"),
              rdescript="go to prior occurrence of current word")*Repeat(extra='n'),
        # may or may not want the escape afterwards to close the find box
        "cursor all":
            R(Key("cs-l"),
              rdescript="add cursor to all occurrences of current selection"),
        "next cursor [<n>]":
            R(Key("c-d"), rdescript="add cursor to next occurrence of current selection")*
            Repeat(extra='n'),
        "indent [<n>]":
            R(Key("tab"), rdescript="Visual Studio Code: Indent")*Repeat(extra="n"),
        "hard delete [<n>]":
            R(Key("s-del"), rdescript="eliminates line not just the text on it")*
            Repeat(extra='n'),
        "copy line up [<n>]":
            R(Key("sa-up"), rdescript="duplicate line above")*Repeat(extra='n'),
        "copy line up [<n>]":
            R(Key("sa-down"), rdescript="duplicate line below")*Repeat(extra='n'),
        "switch line down [<n>]":
            R(Key("a-down"), rdescript="switch line with the one below it")*
            Repeat(extra='n'),
        "switch line up [<n>]":
            R(Key("a-up"), rdescript="switch line with the one above it")*
            Repeat(extra='n'),
        "match bracket":
            R(Key("cs-backslash"), rdescript="jump to matching bracket"),

        # commands for selecting between parable characters using "quick and simple text selection" VScode extension (required)
        # repetition of these commands by saying the number expands the selection to include the text between the next (i.e. outer) set of parable characters of the given type
        "select between <between_parables> [<n>]":
            R(Key("c-k, %(between_parables)s"),
              rdescript=
              "select between parentheses noninclusive using 'quick and simple text selection' VScode extension"
              )*Repeat(extra='n'),
        "select around <around_parables> [<n>]":
            R(Key("c-k, %(around_parables)s"),
              rdescript=
              "select between parentheses inclusive using 'quick and simple text selection' VScode extension"
              )*Repeat(extra='n'),
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


class VisualStudioCodeNonCcrRule(MergeRule):
    pronunciation = "Visual Studio code non-continuous"
    mapping = {
        # moving around a file
        "[(go to | jump | jump to)] line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter"),
              rdescript="Visual Studio Code: Go to Line"),
        "Go back <n>":
            R(Key("a-left"), rdescript="Visual Studio Code: Go Back")*Repeat(extra="n"),
        "Go forward [<n>]":
            R(Key("a-right"), rdescript="Visual Studio Code: Go Forward")*
            Repeat(extra="n"),

        # display
        # note that most of these can be turned on/off with the same command
        "[toggle] full screen":
            R(Key("sa-enter"), rdescript="VS Code: Fullscreen"),
        "toggle orientation":
            R(Key("sa-0"), rdescript="toggle orientation"),
        "zoom in [<n>]":
            R(Key("c-equal"), rdescript="zoom in")*Repeat(extra='n'),
        "zoom out [<n>]":
            R(Key("c-minus"), rdescript="zoom out")*Repeat(extra='n'),
        "sidebar":
            R(Key("c-b"), rdescript="sidebar"),
        "explorer":
            R(Key("cs-e"), rdescript="Explorer"),
        "source control":
            R(Key("cs-g"), rdescript="source control"),
        "keyboard shortcuts":
            R(Key("c-k, c-s"), rdescript="keyboard shortcuts"),
        "key mappings":
            R(Key("c-k, c-s:2"), rdescript="key mappings"),
        "settings":
            R(Key("a-f, p, s"), rdescript="user/workspace settings"),
        "snippets":
            R(Key("a-f, p, s:2"), rdescript="user snippets"),
        "extensions":
            R(Key("cs-x"), rdescript="extensions"),
        "search details":
            R(Key("cs-j"), rdescript="search details"),
        "output panel":
            R(Key("cs-u"), rdescript="output panel"),
        "markdown preview":
            R(Key("cs-v"), rdescript="markdown preview"),
        "markdown preview side":
            R(Key("c-k, v"), rdescript="open markdown preview to the side"),
        "Zen mode":
            R(Key("c-k, z"), rdescript="Zen mode"),  # note: use esc esc to exit

        # File management
        "[open] command palette":
            R(Key("cs-p"), rdescript="Visual Studio Code: Command Palette"),
        "(Open [file] | Go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s"), rdescript="Visual Studio Code: Go To File"),
        "Save and close":
            R(Key("c-s/10, c-w"), rdescript="Visual Studio Code: Save And Close File"),
        "new file":
            R(Key("c-n"), rdescript="new file"),
        "new window":
            R(Key("cs-n"), rdescript="new window"),
        "close window":
            R(Key("a-f4"), rdescript="close window"),
        "close workspace":
            R(Key("c-k, f"), rdescript="close workspace"),
        "close editor":
            R(Key("c-f4"), rdescript="close editor"),
        "save as":
            R(Key("cs-s"), rdescript="save as"),
        "save all":
            R(Key("c-k, s"), rdescript="Save all"),
        "next tab [<n>]":
            R(Key("c-pgdown"), rdescript="Visual Studio Code: Next Tab")*
            Repeat(extra="n"),
        "previous tab [<n>]":
            R(Key("c-pgup"), rdescript="Visual Studio Code: Previous Tab")*
            Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-f4/20"), rdescript="Visual Studio: Close Tab")*Repeat(extra="n"),
        "(recent | R) tab [<n>]":
            R(Key("c-tab"), rdescript="go to most recent tab")*Repeat(extra='n'),
        "reopen tab [<n>]":
            R(Key("cs-t"), rdescript="reopen most recently tab")*Repeat(extra='n'),
        "Exit preview":
            R(Key("space, c-z"), rdescript="Visual Studio Code: Exit Preview"),
        "keep preview mode editor open":
            R(Key("c-k, enter"), rdescript="keep preview mode editor open"),
        "copy path":
            R(Key("c-k, p"), rdescript="copy path of active file"),
        "windows explorer here":
            R(Key("c-k, r"),
              rdescript="open Windows Explorer to the location of active file"),
        "show active file in new window":
            R(Key("c-k, o"), rdescript="show active file in new window"),

        # Search
        "(search | find)":
            R(Key("c-f"), rdescript="Visual Studio Code: Find in File"),
        "replace":
            R(Key("c-h"), rdescript="replace"),
        "find in files":
            R(Key("cs-f"), rdescript="find in files"),
        "replace in files":
            R(Key("cs-h"), rdescript="replace in files"),
        "next find":
            R(Key("f3"), rdescript="go to next occurrence"),
        "(prior | previous) find":
            R(Key("s-f3"), rdescript="go to previous occurrence"),
        "select all occurrences":
            R(Key("a-enter"), rdescript="select all occurrences of find match"),

        "toggle case sensitive":
            R(Key("a-c"), rdescript="toggle case-sensitive"),
        "toggle regex":
            R(Key("a-r"), rdescript="toggle regular expressions"),
        "toggle whole word":
            R(Key("a-w"), rdescript="toggle whole word"),

        "(Find | Jump [to]) next <text>":
            R(Function(findNthToken, n=1, direction="forward"),
              rdescript="Visual Studio Code: Find Next"),
        "(Find | Jump [to]) previous <text>":
            R(Function(findNthToken, n=1, direction="reverse"),
              rdescript="Visual Studio Code: Find Previous"),
        "show all symbols":
            R(Key("c-t"), rdescript="show all symbols"),
        "go to symbol":
            R(Key("cs-o"), rdescript="go to symbol"),

        # editor management
        "close editor":
            R(Key("c-w"), rdescript="close editor"),
        "close folder":
            R(Key("c-k, f"), rdescript="close folder"),
        "split editor":
            R(Key("c-backslash"), rdescript="split editor into 2 panes"),
        "next pane":
            R(Key("c-k, c-right"), rdescript="move to next pane"),
        "(prior | previous | un) pane":
            R(Key("c-k, c-right"), rdescript="move to next pane"),
        "shift group left":
            R(Key("c-k, left"),
              rdescript=
              "shift current group of tabs to the left e.g. swap with pane to the left"),
        "shift group left":
            R(Key("c-k, right"),
              rdescript=
              "shift current group of tabs to the right e.g. swap with pane to the right"
              ),
        "<nth> tab":
            R(Key("c-%(nth)s"), rdescript="go to nth pane"),

        # languages editing
        "Go to definition":
            R(Key("f12"), rdescript="Visual Studio Code: Go to Definition"),
        "Go to required definition":
            R(Key("c-f12:2, c-right:5, left/50, f12"),
              rdescript="Visual Studio Code: Go to Required Definition"),
        "peak definition":
            R(Key("a-f12"), rdescript="peak definition"),
        "trigger parameter hints":
            R(Key("cs-space"), rdescript="trigger parameter hints"),
        "format that":
            R(Key("c-k, c-f"), rdescript="format selection"),
        "(definition to side | side def)":
            R(Key("c-k, f12"), rdescript="open definition to the side"),
        "show references":
            R(Key("s-f12"), rdescript="show references"),
        "rename symbol":
            R(Key("f2"), rdescript="rename symbol"),
        "(trim white)":
            R(Key("c-k, c-x"), rdescript="trim trailing white space"),
        "change file language":
            R(Key("c-k, m"), rdescript="change file language"),

        # Debugging
        "debug":
            R(Key("cs-d"), rdescript="debug"),
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="Visual Studio Code:Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50")*Repeat(extra="n"), rdescript="Visual Studio Code:Step Over"),
        "step into":
            R(Key("f11"), rdescript="Visual Studio Coade:Step Into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="Visual Studio Code:Step Out"),
        "resume":
            R(Key("f5"), rdescript="Visual Studio Code:Resume"),
        "stopper":
            R(Key("s-f5"), rdescript="debug stop"),
        "continue":
            R(Key("f5"), rdescript="start/continue"),
        "show hover":
            R(Key("c-k, c-i"),
              rdescript=
              "show the little box as if you are hovering your mouse over the place where the cursor ( as opposed to the mouse pointer) currently is"
              ),
        "[show] problems [panel]":
            R(Key("cs-m"), rdescript="show problems panel"),
        "next error":
            R(Key("f8"),
              rdescript="go to next error"),  # doesn't seem to be working properly
        "(prior | previous) error":
            R(Key("s-f8"), rdescript="go to previous error"),
        "toggle tab moves focus":
            R(Key("c-m"), rdescript="toggle taboos focus"),


        # integrated terminal
        "[show] terminal":
            R(Key("c-backtick"), rdescript="show integrated terminal"),
        "new terminal":
            R(Key("cs-backtick"), rdescript="new integrated terminal"),
        "terminal scroll up":
            R(Key("c-up"), rdescript="terminal scroll up"),
        "terminal scroll down":
            R(Key("c-down"), rdescript="terminal scroll down"),
        "terminal page up":
            R(Key("s-pgup"), rdescript="terminal page up"),
        "terminal page down":
            R(Key("s-pgdown"), rdescript="terminal page down"),

        # collapsing
        "(fold | collapse) region":
            R(Key("cs-lbracket"), rdescript="collapse region"),
        "(unfold | uncollapse) region":
            R(Key("cs-rbracket"), rdescript="uncollapse region"),
        "(fold | collapse) [all] subregions":
            R(Key("c-k, c-lbracket"), rdescript="collapse all subregions"),
        "(unfold | uncollapse) [all] subregions":
            R(Key("c-k, c-rbracket"), rdescript="uncollapse all subregions"),
        "(fold | collapse) [all] regions":
            R(Key("c-k, c-0"), rdescript="safe collapse all regions"),
        "(unfold | uncollapse) [all] regions":
            R(Key("c-k, c-j"), rdescript="on collapse all regions"),
        "toggle word wrap":
            R(Key("a-z"), rdescript="toggle word wrap"),

        "run this line":
            R(Key("csa-l"), rdescript="run this line"),
        "join line":
            R(Key("csa-j"), rdescript="join line"),

        # requires gitlens extension
        "toggle blame":
            R(Key("cs-g, b"), rdescript="toggle blame"),
        "lens commit details":
            R(Key("cs-g, c"), rdescript="lens commit details"),
        "lens file history":
            R(Key("cs-g, h"), rdescript="lens file history"),
        "lens repo status":
            R(Key("cs-g, s"), rdescript="lens repo status"),
        "toggle git lens":
            R(Key("cs-g, s-b"), rdescript="toggle git lens"),

        # requires bookmark extension
        "mark (prev | prior | previous)":
            R(Key("ca-j"), rdescript="Mark previous"),
        "mark next":
            R(Key("ca-l"), rdescript="Mark next"),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
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
    defaults = {"n": 1, "mim": "", "text": ""}


#---------------------------------------------------------------------------

# Initialise the rule.
context = AppContext(title="Visual Studio Code")

grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VisualStudioCodeRule())
    else:
        control.nexus().merger.add_app_rule(VisualStudioCodeRule(), context)