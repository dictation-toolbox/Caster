"""
Command-module for Microsoft Excel
You also can find some good vocola commands for Excel on Mark Lillibridge's Github:
https://github.com/mdbridge/bit-bucket/tree/master/voice/my_commands/commands
Alex Boche 2019
"""
from castervoice.lib.imports import *

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
def make_sequence_dict_fixed_length(dictionary, fixed_sequence_length):
    mapping = {}
    for tup in itertools.product(dictionary.keys(), repeat=fixed_sequence_length):
        mapping[" ".join(tup)] = "".join(dictionary[word] for word in tup)
    return mapping


def make_sequence_dict_up_to_length(dictionary, highest_length):
    # d will be a dict of whole number keys pointing to the corresponding fixed length dictionaries
    d = {}
    for i in range(1, highest_length + 1):
        d[i] = make_sequence_dict_fixed_length(dictionary, i)
    # output = {k: d[i][k] for k in d[i] for i in d}
    output = {}
    for i in d:
        for k in d[i]:
            output[k] = d[i][k]
    return output


class ExcelRule(MergeRule):
    pronunciation = "excel"

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
        IntegerRefST("n", 1, 10),
        IntegerRefST("m", 1, 10),
        IntegerRefST("numbers", 1, 100),
        IntegerRefST("row_1", 1, 100),
        IntegerRefST("row_2", 1, 100),
        # when I set the sequence length to 3 I got the grammar too complex Natlink error.
        Choice("column_1", make_sequence_dict_up_to_length(alphanumeric.caster_alphabet, 2)),
        Choice("column_2", make_sequence_dict_up_to_length(alphanumeric.caster_alphabet, 2)),
    ]
    defaults = {"n": 1, "dict": ""}


context = AppContext(executable="excel")
control.non_ccr_app_rule(ExcelRule(), context=context)