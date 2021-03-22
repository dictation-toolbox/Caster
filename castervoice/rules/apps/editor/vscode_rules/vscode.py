# thanks to Casper for contributing commands to this.
from dragonfly import Repeat, Dictation, Choice, ShortIntegerRef

from castervoice.lib.actions import Key

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class VSCodeCcrRule(MergeRule):
    pronunciation = "visual studio code ccr"

    mapping = {
        "[show] terminal":
            R(Key("c-backtick")),
        # Note: If you get the bad grammar grammar too complex error, move some of these commands into the non-CCR rule
        # cursor/line navigation
        "scroll up [<n>]":
            R(Key("c-up")*Repeat(extra='n'),
              rdescript="VS Code: Scroll Up One Line at a Time"),
        "scroll down [<n>]":
            R(Key("c-down")*Repeat(extra='n'),
              rdescript="VS Code: Scroll Down One Line at a Time"),
        "scroll page up [<n>]":
            R(Key("a-pgup")*Repeat(extra='n'),
              rdescript="VS Code: Scroll Up One Page Up at a Time"),
        "scroll page down [<n>]":
            R(Key("a-pgdown")*Repeat(extra='n'),
              rdescript="VS Code: Scroll Down One Page Down At a Time"),
        "comment [line]":
            R(Key("c-slash"), rdescript="VS Code: Line Comment"),
        "block comment":
            R(Key("sa-a"), rdescript="VS Code: Block Comment"),
        # Multi-cursor and selection
        "cursor above [<n>]":
            R(Key("ca-up")*Repeat(extra='n'), rdescript="VS Code: Insert Cursor Above"),
        "cursor below [<n>]":
            R(Key("ca-down")*Repeat(extra='n'), rdescript="VS Code: Insert Cursor Above"),
        "remove cursor":
            R(Key("csa-down"), rdescript="VS Code: Remove Cursor"
              ),  # not sure if this command works always; also try csa-up
        # csa-down/up seems to work sometimes to remove 1 of the cursors
        # but I don't really understand how this works
        "tall cursor up":
            R(Key("csa-pgup"), rdescript="VS Code: Add Cursors All The Way Up"),
        "tall cursor down":
            R(Key("csa-pgdown"), rdescript="VS Code: Add Cursors All The Way Down"),

        "expand  [<n>]": R(Key("sa-right"),
            rdescript="highlight current word(s)") * Repeat(extra='n'),
        "shrink  [<n>]": R(Key("sa-left"),
            rdescript="shrink the previous highlighting range or unhighlight") * Repeat(extra='n'),

        # Command below requires "brackets select" extension for VS code
        "select [in] brackets [<n>]":
            R(Key("ca-a")*Repeat(extra='n'),
              rdescript=
              "VS Code: Select in between parable punctuation inclusive using 'brackets select' extension"
              )*Repeat(extra='n'),
        "all current selection":
            R(Key("c-l"),
              rdescript="VS Code: Select All Occurrences of Current Selection"),
        "all current word":
            R(Key("c-f2"), rdescript="VS Code: Select All Occurrences of Current Word"),
        "select next [<n>]":
            R(Key("c-f3")*Repeat(extra='n'),
              rdescript="VS Code: Select Next Occurrence of Current Word"),
        "go to next [<n>]":
            R(Key("sa-right/2, c-f3, c-left/2, escape")*Repeat(extra='n'),
              rdescript="VS Code: Go to Next Occurrence of Current Word"),
        # may or may not want the escape afterwards to close the find box
        # note the above command might sometimes be off by one so you have to say one higher
        # than what you mean e.g. if the cursor is at the beginning of the word rather
        # than in the middle or end, you will have to say "next word two" to get to the next word
        "select prior [<n>]":
            R(Key("cs-f3"), rdescript="VS Code: Select Prior Occurrence of Current Word"),
        "go to prior [<n>]":
            R(Key("sa-right/2, cs-f3, c-left/2, escape")*Repeat(extra='n'),
              rdescript="VS Code: Go to Prior Occurrence of Current Word"),
        # may or may not want the escape afterwards to close the find box
        "cursor all":
            R(Key("cs-l"),
              rdescript="VS Code: Add Cursor to All Occurrences of Current Selection"),
        "next cursor [<n>]":
            R(Key("c-d")*Repeat(extra='n'),
              rdescript="VS Code: Add Cursor to Next Occurrence of Current Selection"),
        "skip next cursor [<n>]":
            R(Key("c-k,c-d") * Repeat(extra="n"),
            rdescript="VS Code: Skip Selection and Add Cursor to Next Occurrence of Current Selection",
        ),
        "indent [<n>]":
            R(Key("c-]"), rdescript="VS Code: Indent"),
        "(unindent|out dent) [<n>]":
            R(Key("c-["), rdescript="VS Code: Unindent"),
        "hard delete [<n>]":
            R(Key("s-del"), rdescript="VS Code: Eliminates Line not Just the Text on it"),
        "copy line up [<n>]":
            R(Key("sa-up")*Repeat(extra='n'), rdescript="VS Code: Duplicate Line Above"),
        "copy line down [<n>]":
            R(Key("sa-down")*Repeat(extra='n'),
              rdescript="VS Code: Duplicate Line Below"),
        "switch line down [<n>]":
            R(Key("a-down")*Repeat(extra='n'),
              rdescript="VS Code: Switch Line With the One Below it"),
        "switch line up [<n>]":
            R(Key("a-up")*Repeat(extra='n'),
              rdescript="VS Code: Switch Line With the One Above it"),
        "match bracket":
            R(Key("cs-backslash"), rdescript="VS Code: Jump to Matching Bracket"),

        # commands for selecting between parable characters using "quick and simple text selection" VScode extension (required)
        # repetition of these commands by saying the number expands the selection to include the text between the next (i.e. outer) set of parable characters of the given type
        "select between <between_parables> [<n>]":
            R(Key("c-k, %(between_parables)s")*Repeat(extra='n'),
              rdescript=
              "VS Code: Select between parentheses noninclusive using 'quick and simple text selection' VScode extension"
              ),
        "select around <around_parables> [<n>]":
            R(Key("c-k, %(around_parables)s")*Repeat(extra='n'),
              rdescript=
              "VS Code: Select between parentheses inclusive using 'quick and simple text selection' VScode extension"
              ),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 1, 10),
        Choice(
            "between_parables", {
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


def get_rule():
    details = RuleDetails(executable="code",
                          title="Visual Studio Code",
                          ccrtype=CCRType.APP)
    return VSCodeCcrRule, details
