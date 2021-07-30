from dragonfly import Function, Repeat, Choice, Dictation, MappingRule, Pause, ShortIntegerRef

from castervoice.lib.actions import Key, Mouse

from castervoice.lib import navigation
from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def _find_nth_token(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute()
    else:
        Key("enter:%(n)d").execute()
        print("no? %(n)d")
    Key('escape').execute()


class VSCodeNonCcrRule(MappingRule):
    mapping = {
        # Moving around a file
        "[(go to | jump | jump to)] line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter")),
        "<action> [line] <ln1> [by <ln2>]":
            R(Function(navigation.action_lines)),

        "go back [<n>]":
            R(Key("a-left") * Repeat(extra='n')),
        "go forward [<n>]":
            R(Key("a-right")) * Repeat(extra="n"),

        # Display
        # note that most of these can be turned on/off with the same command
        "[toggle] full screen":
            R(Key("f11")),
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
            R(Key("a-f, p, s, enter"), rdescript="VS Code: User/workspace Settings"),
        "snippets":
            R(Key("a-f, p, s:2, enter"), rdescript="VS Code: User Snippets"),
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
        "copy path":
            R(Key("c-k, p")),
        "[open] command palette [<text>]":
            R(Key("cs-p") + Text("%(text)s"), rdescript="VS Code: Command Palette"),
        "(open file | go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s"), rdescript="VS Code: Go to File without using dialogbox"),
        "open project [<text>]":
            R(Key("c-r") + Pause("30") + Text("%(text)s")),
        "open dialogue":
            R(Key("c-o"), rdescript="VS Code: open file dialogbox"),
        "open folder":
            R(Key("c-k, c-o"), rdescript="VS Code: Open folder"),
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
        "keep [preview] open":
            R(Key("c-k, enter")),
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
            R(Key("a-c"), rdescript="VS Code: Toggle Find Case Sensitive"),
        "toggle regex":
            R(Key("a-r"), rdescript="VS Code: Toggle Find Regular Expressions"),
        "toggle whole word":
            R(Key("a-w"), rdescript="VS Code: Toggle Find Whole Word"),

        "(find | jump [to]) next <text>":
            R(Function(_find_nth_token, n=1, direction="forward")),
        "(find | jump [to]) previous <text>":
            R(Function(_find_nth_token, n=1, direction="reverse")),
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
            R(Key("c-k, c-left")),
        "move tab left":
            R(Key("ca-left"),
            rdescript="VS Code: Move the current tab to the editor pane on the left."),
        "move tab right":
            R(Key("ca-right"),
            rdescript="VS Code: Move the current tab to the editor pane on the right."),
        "shift group left":
            R(Key("c-k, left"),
              rdescript="VS Code: Shift Current Group of Tabs to the Left E.g. Swap with Pane to the Left"),
        "shift group right":
            R(Key("c-k, right"),
              rdescript="VS Code: Shift Current Group of Tabs to the Right E.g. Swap with Pane to the Right"
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
        "format (that | selection)":
            R(Key("c-k, c-f")),
        "format (doc | document)":
            R(Key("sa-f")),
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
            R(Key("f5"), rdescript="VS Code: Start/Continue"),
        "(show hover|mouse hover|hover mouse)":
            R(Key("c-k, c-i"),
              rdescript="Show the little box as if you are hovering your mouse over the place where the cursor (As opposed to the mouse pointer) currently is"
              ),
        "[show] problems [panel]":
            R(Key("cs-m")),
        "next error":
            R(Key("f8")),  # doesn't seem to be working properly
        "(prior | previous) error":
            R(Key("s-f8")),
        "toggle tab moves focus":
            R(Key("c-m")),

        # Integrated Terminal

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
        "altar kick":
            R(Key("alt:down") + Mouse("left") + Key("alt:up")),

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
            R(Key("f1") + Text("join lines") + Key("enter")),

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
        ShortIntegerRef("ln1", 1, 1000),
        ShortIntegerRef("ln2", 1, 1000),
        ShortIntegerRef("n", 1, 1000),
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


def get_rule():
    details = RuleDetails(name="Visual Studio Code",
                          executable="code",
                          title="Visual Studio Code")
    return VSCodeNonCcrRule, details
