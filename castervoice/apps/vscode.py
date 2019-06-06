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
    pronunciation = "visual studio code continuous"
    mwith = CCRMerger.CORE

    mapping = {
        # Note: If you get the bad grammar grammar too complex error, move some of these commands into the non-CCR rule
        # cursor/line navigation
        "scroll up [<n>]":
            R(Key("c-up") * Repeat(extra='n'),
              rdescript="VS Code: Scroll Up One Line at a Time"),
        "scroll down [<n>]":
            R(Key("c-down") * Repeat(extra='n'),
              rdescript="VS Code: Scroll Down One Line at a Time"),
        "scroll page up [<n>]":
            R(Key("a-pgup") * Repeat(extra='n'),
              rdescript="VS Code: Scroll Up One Page Up at a Time"),
        "scroll page down [<n>]":
            R(Key("a-pgdown") * Repeat(extra='n'),
              rdescript="VS Code: Scroll Down One Page Down At a Time"),
        "(unindent|outdent) [<n>]":
            R(Key("s-tab") * Repeat(extra='n'), rdescript="VS Code: Unindent"),
        "comment line":
            R(Key("c-slash"), rdescript="VS Code: Line Comment"),
        "block comment":
            R(Key("sa-a"), rdescript="VS Code: Block Comment"),
        # Multi-cursor and selection
        "cursor above [<n>]":
            R(Key("ca-up") * Repeat(extra='n'),
              rdescript="VS Code: Insert Cursor Above"),
        "cursor below [<n>]":
            R(Key("ca-down") * Repeat(extra='n'),
              rdescript="VS Code: Insert Cursor Above"),
        "remove cursor":
            R(Key("csa-down"),
              rdescript="VS Code: Remove Cursor"),  # not sure if this command works always; also try csa-up
        # csa-down/up seems to work sometimes to remove 1 of the cursors
        # but I don't really understand how this works
        "tall cursor up":
            R(Key("csa-pgup"), rdescript="VS Code: Add Cursors All The Way Up"),
        "tall cursor down":
            R(Key("csa-pgdown"), rdescript="VS Code: Add Cursors All The Way Down"),
        # Command below requires "brackets select" extension for VS code
        "select [in] brackets [<n>]":
            R(Key("ca-a") * Repeat(extra='n'),
              rdescript="VS Code: Select in between parable punctuation inclusive using 'brackets select' extension"
              )*Repeat(extra='n'),
        "all current selection":
            R(Key("c-l"), rdescript="VS Code: Select All Occurrences of Current Selection"),
        "all current word":
            R(Key("c-f2"), rdescript="VS Code: Select All Occurrences of Current Word"),
        "select next [<n>]":
            R(Key("c-f3") * Repeat(extra='n'),
              rdescript="VS Code: Select Next Occurrence of Current Word"),
        "go to next [<n>]":
            R(Key("sa-right/2, c-f3, c-left/2, escape") * Repeat(extra='n'),
              rdescript="VS Code: Go to Next Occurrence of Current Word"),
        # may or may not want the escape afterwards to close the find box
        # note the above command might sometimes be off by one so you have to say one higher
        # than what you mean e.g. if the cursor is at the beginning of the word rather
        # than in the middle or end, you will have to say "next word two" to get to the next word
        "select prior [<n>]":
            R(Key("cs-f3"), rdescript="VS Code: Select Prior Occurrence of Current Word"),
        "go to prior [<n>]":
            R(Key("sa-right/2, cs-f3, c-left/2, escape") * Repeat(extra='n'),
              rdescript="VS Code: Go to Prior Occurrence of Current Word"),
        # may or may not want the escape afterwards to close the find box
        "cursor all":
            R(Key("cs-l"),
              rdescript="VS Code: Add Cursor to All Occurrences of Current Selection"),
        "next cursor [<n>]":
            R(Key("c-d") * Repeat(extra='n'),
              rdescript="VS Code: Add Cursor to Next Occurrence of Current Selection"),
        "indent [<n>]":
            R(Key("tab") * Repeat(extra='n'), rdescript="VS Code: Indent"),
        "hard delete [<n>]":
            R(Key("s-del"), rdescript="VS Code: Eliminates Line not Just the Text on it"),
        "copy line up [<n>]":
            R(Key("sa-up") * Repeat(extra='n'),
              rdescript="VS Code: Duplicate Line Above"),
        "copy line up [<n>]":
            R(Key("sa-down") * Repeat(extra='n'),
              rdescript="VS Code: Duplicate Line Below"),
        "switch line down [<n>]":
            R(Key("a-down") * Repeat(extra='n'),
              rdescript="VS Code: Switch Line With the One Below it"),
        "switch line up [<n>]":
            R(Key("a-up") * Repeat(extra='n'),
              rdescript="VS Code: Switch Line With the One Above it"),
        "match bracket":
            R(Key("cs-backslash"), rdescript="VS Code: Jump to Matching Bracket"),

        # commands for selecting between parable characters using "quick and simple text selection" VScode extension (required)
        # repetition of these commands by saying the number expands the selection to include the text between the next (i.e. outer) set of parable characters of the given type
        "select between <between_parables> [<n>]":
            R(Key("c-k, %(between_parables)s") * Repeat(extra='n'),
              rdescript="VS Code: Select between parentheses noninclusive using 'quick and simple text selection' VScode extension"
              ),
        "select around <around_parables> [<n>]":
            R(Key("c-k, %(around_parables)s") * Repeat(extra='n'),
              rdescript="VS Code: Select between parentheses inclusive using 'quick and simple text selection' VScode extension"
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


class VSCodeNonCcrRule(MergeRule):

    pronunciation = "Visual Studio Code Non Continuous"
    mapping = {

        # Moving around a file
        "[(go to | jump | jump to)] line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter"),
              rdescript="VS Code: Go to Line"),
        "go back <n>":
            R(Key("a-left") * Repeat(extra='n'), rdescript="VS Code: Go Back"),
        "go forward [<n>]":
            R(Key("a-right"), rdescript="VS Code: Go Forward") *
            Repeat(extra="n"),

        # Display
        # note that most of these can be turned on/off with the same command
        "[toggle] full screen":
            R(Key("sa-enter"), rdescript="VS Code: Fullscreen"),
        "toggle orientation":
            R(Key("sa-0"), rdescript="VS Code: Toggle Orientation"),
        "zoom in [<n>]":
            R(Key("c-equal") * Repeat(extra='n'), rdescript="VS Code: Zoom In"),
        "zoom out [<n>]":
            R(Key("c-minus") * Repeat(extra='n'), rdescript="VS Code: Zoom Out"),
        "sidebar":
            R(Key("c-b"), rdescript="VS Code: Sidebar"),
        "explorer":
            R(Key("cs-e"), rdescript="VS Code: Explorer"),
        "source control":
            R(Key("cs-g"), rdescript="VS Code: Source Control"),
        "keyboard shortcuts":
            R(Key("c-k, c-s"), rdescript="VS Code: Keyboard Shortcuts"),
        "key mappings":
            R(Key("c-k, c-s:2"), rdescript="VS Code: Key Mappings"),
        "settings":
            R(Key("a-f, p, s, enter"), rdescript="VS Code: User/workspace Settings"),
        "snippets":
            R(Key("a-f, p, s:2, enter"), rdescript="VS Code: User Snippets"),
        "extensions":
            R(Key("cs-x"), rdescript="VS Code: Extensions"),
        "search details":
            R(Key("cs-j"), rdescript="VS Code: Search Details"),
        "output panel":
            R(Key("cs-u"), rdescript="VS Code: Output Panel"),
        "markdown preview":
            R(Key("cs-v"), rdescript="VS Code: Markdown Preview"),
        "markdown preview side":
            R(Key("c-k, v"), rdescript="VS Code: Open Markdown Preview to the Side"),
        "Zen mode":
            # note: use esc esc to exit
            R(Key("c-k, z"), rdescript="VS Code: Zen mode"),

        # File Management
        "[open] command palette":
            R(Key("cs-p"), rdescript="VS Code: Command Palette"),
        "(open file | go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s"), rdescript="VS Code: Go to File without using dialogbox"),
        "open dialogue":
            R(Key("c-o"), rdescript="VS Code: open file dialogbox")
        "open folder": 
            R(Key("c-k, c-o"), rdescript="VS Code: Open folder"),
        "Save and close":
            R(Key("c-s/10, c-w"), rdescript="VS Code: Save And Close File"),
        "new file":
            R(Key("c-n"), rdescript="VS Code: New File"),
        "new window":
            R(Key("cs-n"), rdescript="VS Code: New Window"),
        "close window":
            R(Key("a-f4"), rdescript="VS Code: Close Window"),
        "close workspace":
            R(Key("c-k, f"), rdescript="VS Code: Close Workspace"),
        "close editor":
            R(Key("c-f4"), rdescript="VS Code: Close Editor"),
        "save as":
            R(Key("cs-s"), rdescript="VS Code: Save As"),
        "save all":
            R(Key("c-k, s"), rdescript="VS Code: Save all"),
        "next tab [<n>]":
            R(Key("c-pgdown") * Repeat(extra='n'), rdescript="VS Code: Next Tab"),
        "previous tab [<n>]":
            R(Key("c-pgup") * Repeat(extra='n'),
              rdescript="VS Code: Previous Tab"),
        "close tab [<n>]":
            R(Key("c-f4/20") * Repeat(extra='n'),
              rdescript="VS Code: Close Tab"),
        "(recent | R) tab [<n>]":
            R(Key("c-tab") * Repeat(extra='n'),
              rdescript="VS Code: Go to Most Recent Tab"),
        "reopen tab [<n>]":
            R(Key("cs-t") * Repeat(extra='n'),
              rdescript="VS Code: Reopen Most Recently Tab"),
        "Exit preview":
            R(Key("space, c-z"), rdescript="VS Code: Exit Preview"),
        "keep preview open":
            R(Key("c-k, enter"), rdescript="VS Code: Keep Preview Mode Editor Open"),
        "copy path":
            R(Key("c-k, p"), rdescript="VS Code: Copy Path of Active File"),
        "windows explorer here":
            R(Key("c-k, r"),
              rdescript="VS Code: open Windows Explorer to the Location of Active File"),
        "show active file in new window":
            R(Key("c-k, o"), rdescript="VS Code: Show Active File in New Window"),

        # Search
        "(search | find)":
            R(Key("c-f"), rdescript="VS Code: Find in File"),
        "replace":
            R(Key("c-h"), rdescript="VS Code: Replace"),
        "find in files":
            R(Key("cs-f"), rdescript="VS Code: Find in Files"),
        "replace in files":
            R(Key("cs-h"), rdescript="VS Code: Replace in Files"),
        "next find":
            R(Key("f3"), rdescript="VS Code: Go to Next Occurrence"),
        "(prior | previous) find":
            R(Key("s-f3"), rdescript="VS Code: Go to Previous Occurrence"),
        "select all occurrences":
            R(Key("a-enter"), rdescript="VS Code: Select all Occurrences of Find Match"),

        "toggle case sensitive":
            R(Key("a-c"), rdescript="VS Code: Toggle Find Case Sensitive"),
        "toggle regex":
            R(Key("a-r"), rdescript="VS Code: Toggle Find Regular Expressions"),
        "toggle whole word":
            R(Key("a-w"), rdescript="VS Code: Toggle Find Whole Word"),

        "(find | jump [to]) next <text>":
            R(Function(findNthToken, n=1, direction="forward"),
              rdescript="VS Code: Find Next"),
        "(find | jump [to]) previous <text>":
            R(Function(findNthToken, n=1, direction="reverse"),
              rdescript="VS Code: Find Previous"),
        "show all symbols":
            R(Key("c-t"), rdescript="VS Code: Show all Symbols"),
        "go to symbol":
            R(Key("cs-o"), rdescript="VS Code: Go to Symbol"),

        # Editor Management
        "close editor":
            R(Key("c-w"), rdescript="VS Code: Close Editor"),
        "close folder":
            R(Key("c-k, f"), rdescript="VS Code: Close Folder"),
        "split editor":
            R(Key("c-backslash"), rdescript="VS Code: Split Editor into 2 Panes"),
        "next pane":
            R(Key("c-k, c-right"), rdescript="VS Code: Move to Next Pane"),
        "(prior | previous | un) pane":
            R(Key("c-k, c-right"), rdescript="VS Code: Move to Next Pane"),
        "shift group left":
            R(Key("c-k, left"),
              rdescript="VS Code: Shift Current Group of Tabs to the Left E.g. Swap with Pane to the Left"),
        "shift group right":
            R(Key("c-k, right"),
              rdescript="VS Code: Shift Current Group of Tabs to the Right E.g. Swap with Pane to the Right"
              ),
        "<nth> tab":
            R(Key("c-%(nth)s"), rdescript="VS Code: Go to Nth Pane"),

        # Languages Editing
        "go to definition":
            R(Key("f12"), rdescript="VS Code: Go to Definition"),
        "go to required definition":
            R(Key("c-f12:2, c-right:5, left/50, f12"),
              rdescript="VS Code: Go to Required Definition"),
        "peak definition":
            R(Key("a-f12"), rdescript="VS Code: Peak Definition"),
        "trigger parameter hints":
            R(Key("cs-space"), rdescript="VS Code: Trigger Parameter Hints"),
        "format that":
            R(Key("c-k, c-f"), rdescript="VS Code: Format Selection"),
        "(definition to side | side def)":
            R(Key("c-k, f12"), rdescript="VS Code: Open Definition to the Side"),
        "show references":
            R(Key("s-f12"), rdescript="VS Code: Show References"),
        "rename symbol":
            R(Key("f2"), rdescript="VS Code: Rename Symbol"),
        "(trim white)":
            R(Key("c-k, c-x"), rdescript="VS Code: Trim Trailing White Space"),
        "change file language":
            R(Key("c-k, m"), rdescript="VS Code: Change File Language"),

        # Debugging
        "debug":
            R(Key("cs-d"), rdescript="VS Code: Debug"),
        "[toggle] breakpoint":
            R(Key("f9"), rdescript="VS Code: Breakpoint"),
        "step over [<n>]":
            R(Key("f10/50") * Repeat(extra='n'), rdescript="VS Code: Step Over"),
        "step into":
            R(Key("f11"), rdescript="VS Code: Step into"),
        "step out [of]":
            R(Key("s-f11"), rdescript="VS Code: Step Out"),
        "resume":
            R(Key("f5"), rdescript="VS Code: Resume"),
        "stopper":
            R(Key("s-f5"), rdescript="VS Code: Debug Stop"),
        "continue":
            R(Key("f5"), rdescript="VS Code: Start/Continue"),
        "(show hover|mouse hover|hover mouse)":
            R(Key("c-k, c-i"),
              rdescript="Show the little box as if you are hovering your mouse over the place where the cursor (As opposed to the mouse pointer) currently is"
              ),
        "[show] problems [panel]":
            R(Key("cs-m"), rdescript="VS Code: Show Problems Panel"),
        "next error":
            R(Key("f8"),
              rdescript="VS Code: Go to Next Error"),  # doesn't seem to be working properly
        "(prior | previous) error":
            R(Key("s-f8"), rdescript="VS Code: Go to Previous Error"),
        "toggle tab moves focus":
            R(Key("c-m"), rdescript="VS Code: Toggle Taboos Focus"),

        # Integrated Terminal
        "[show] terminal":
            R(Key("c-backtick"), rdescript="VS Code: Show Integrated Terminal"),
        "new terminal":
            R(Key("cs-backtick"), rdescript="VS Code: New Integrated Terminal"),
        "terminal scroll up":
            R(Key("c-up"), rdescript="VS Code: Terminal Scroll Up"),
        "terminal scroll down":
            R(Key("c-down"), rdescript="VS Code: Terminal Scroll Down"),
        "terminal page up":
            R(Key("s-pgup"), rdescript="VS Code: Terminal Page Up"),
        "terminal page down":
            R(Key("s-pgdown"), rdescript="VS Code: Terminal Page Down"),

        # Collapsing
        "(fold | collapse) region":
            R(Key("cs-lbracket"), rdescript="VS Code: Collapse Region"),
        "(unfold | uncollapse) region":
            R(Key("cs-rbracket"), rdescript="VS Code: Uncollapse Region"),
        "(fold | collapse) [all] subregions":
            R(Key("c-k, c-lbracket"), rdescript="VS Code: Collapse all Subregions"),
        "(unfold | uncollapse) [all] subregions":
            R(Key("c-k, c-rbracket"), rdescript="VS Code: Uncollapse all Subregions"),
        "(fold | collapse) [all] regions":
            R(Key("c-k, c-0"), rdescript="VS Code: Safe Collapse all Regions"),
        "(unfold | uncollapse) [all] regions":
            R(Key("c-k, c-j"), rdescript="VS Code: On Collapse all Regions"),
        "toggle word wrap":
            R(Key("a-z"), rdescript="VS Code: Toggle Word Wrap"),

        "run this line":
            R(Key("csa-l"), rdescript="VS Code: Run This Line"),
        "join line":
            R(Key("csa-j"), rdescript="VS Code: Join Line"),

        # requires gitlens extension
        "toggle blame":
            R(Key("cs-g, b"), rdescript="VS Code: Toggle Blame"),
        "lens commit details":
            R(Key("cs-g, c"), rdescript="VS Code: Lens Commit Details"),
        "lens file history":
            R(Key("cs-g, h"), rdescript="VS Code: Lens File History"),
        "lens repo status":
            R(Key("cs-g, s"), rdescript="VS Code: Lens Repo Status"),
        "toggle git lens":
            R(Key("cs-g, s-b"), rdescript="VS Code: Toggle Git Lens"),

        # requires bookmark extension
        "mark (prev | prior | previous)":
            R(Key("ca-j"), rdescript="VS Code: Mark Previous"),
        "mark next":
            R(Key("ca-l"), rdescript="VS Code: Mark Next"),
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


# ---------------------------------------------------------------------------

# initialise the rule.
context = AppContext(title="Visual Studio Code", executable="code")
grammar = Grammar("Visual Studio Code", context=context)
if settings.SETTINGS["apps"]["visualstudiocode"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(VSCodeCcrRule())
    else:
        control.nexus().merger.add_app_rule(VSCodeCcrRule(), context)
