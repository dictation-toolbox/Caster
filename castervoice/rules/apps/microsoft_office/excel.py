"""
Command-module for Microsoft Excel
You also can find some good vocola commands for Excel on Mark Lillibridge's Github:
https://github.com/mdbridge/bit-bucket/tree/master/voice/my_commands/commands
Alex Boche 2019
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, ShortIntegerRef

from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

class ExcelRule(MappingRule):
    mapping = {
        "next sheet [<n>]":
            R(Key("c-pgdown"))*Repeat(extra='n'),
        "(prior | previous) sheet [<n>]":
            R(Key("c-pgup"))*Repeat(extra='n'),
        "[select] cell <column_1> <row_1>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s") + Key("enter")),
        "select <column_1> <row_1> through <column_2> <row_2>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") +
              Key("enter")),
        "go to cell":
            R(Key("c-g")),
        "select current column":
            R(Key("c-space")),
        "select current row":
            R(Key("s-space")),
        "top of column":
            R(Key("c-up")),
        "beginning of row":
            R(Key("c-left")),
        "insert stuff":
            R(Key("cs-plus")),
        "insert row":
            R(Key("cs-plus, a-r, enter")),
        "insert column":
            R(Key("cs-plus, a-c, enter")),
        "insert cell [to the] left":
            R(Key("cs-plus, a-i, enter")),
        "insert cell above":
            R(Key("cs-plus, a-d, enter")),
        "insert pivot table":
            R(Key("a-n, v")),
        "insert pivot chart":
            R(Key("a-n, s, z, c")),
        "add-ins":
            R(Key("a-t, i")),
        "add border":
            R(Key("cs-ampersand")),
        "arrange Windows":
            R(Key("a-w/10, a")),
        "auto sum":
            R(Key("a-equal")),
        "freeze panes":
            R(Key("a-w, f")),

        # From Mark Lillibridge regarding the edit cell command below:
        # There are at least two modes, edit (blue background) and enter (yellow background).
        # In enter mode for formulas, arrow keys select a
        # cell (range if shifted), whereas in edit mode, they move the cursor
        # inside the formula.  For non-formulas, in enter mode, the arrows
        # finished entering the current cell and move to another cell.
        #
        #  and "edit cell" initially switch to edit mode then
        # toggle thereafter for the given cell.  Typing initially puts you in
        # enter mode.
        #

        # edit cell: always edits directly in cell (blue background)

        #
        # this has the effect of pressing F2 without DNS around.
        #
        # Want "edit directly in cell" option turned off:
        #   Office button->advanced-> turn off allow editing directly in cells
        # (Dragon handles edit in cell directly badly)
        #
        # First time, edits current cell via formula bar.  Unlike with
        # editing directly in a cell, this highlights ranges and cells used.
        "toggle edit cell":
            R(Key("f2")),
    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("n", 1, 10),
        ShortIntegerRef("row_1", 1, 100),
        ShortIntegerRef("row_2", 1, 100),
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2")
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return ExcelRule, RuleDetails(name="excel", executable="excel")