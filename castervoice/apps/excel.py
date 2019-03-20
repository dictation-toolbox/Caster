#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Microsoft Excel
<<<<<<< HEAD
You also can find some good vocola commands for Excel on Mark Lillibridge's Github: 
https://github.com/mdbridge/bit-bucket/tree/master/voice/my_commands/commands

=======
You also can find some good vocola commands for Excel on Mark Lillibridge's Github:
https://github.com/mdbridge/bit-bucket/tree/master/voice/my_commands/commands
Alex Boche 2019
>>>>>>> upstream/develop
"""
#---------------------------------------------------------------------------
import itertools

from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

# NATO alphabet dictionary
word_to_letter = {
    "Alpha": "a",
    "Bravo": "b",
    "Charlie": "c",
    "Delta": "d",
    "Echo": "e",
    "Foxtrot": "f",
    "Golf": "g",
    "Hotel": "h",
    "India": "i",
    "Juliet": "j",
    "Kilo": "k",
    "Lima": "l",
    "Mike": "m",
    "November": "n",
    "Oscar": "o",
    "Papa": "p",
    "Quebec": "q",
    "Romeo": "r",
    "Sierra": "s",
    "Tango": "t",
    "Uniform": "u",
    "Victor": "v",
    "X-ray": "x",
    "Yankee": "y",
    "Zulu": "z"
}


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
            R(Key("c-pgdown"), rdescript="Excel: next sheet")*Repeat(extra='n'),
        "(prior | previous) sheet [<n>]":
            R(Key("c-pgup"), rdescript="Excel: prior sheet")*Repeat(extra='n'),

        # this uses the NATO phonetic alphabet. if you want to change it ,
        # change the dictionary above called word_to_letter
        "[select] cell <column_1> <row_1>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s") + Key("enter"),
              rdescript="Excel: Select Cell with Given Coordinates e.g. Alpha Hotel 7"),
        "select <column_1> <row_1> through <column_2> <row_2>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") +
              Key("enter"),
              rdescript="Excel: Selects Range of Cells e.g. Bravo 5 Through Golf Yankee 10"),
        "go to cell":
            R(Key("c-g"), rdescript="Excel:Open 'go to' Dialogbox"),
        "select current column":
            R(Key("c-space"), rdescript="Excel: Select Current Column"),
        "select current row":
            R(Key("s-space"), rdescript="Excel: Select Current Row"),
        "top of column":
            R(Key("c-up"), rdescript="Excel: Go to Top of Column"),
        "beginning of row":
            R(Key("c-left"), rdescript="Excel: Go to Beginning of Row"),
        "insert stuff":
            R(Key("cs-plus"), rdescript="Excel: Insert Stuff"),
        "insert row":
            R(Key("cs-plus, a-r, enter"),
              rdescript="Excel: Inserts Entire Row Above Current Row"),
        "insert column":
            R(Key("cs-plus, a-c, enter"),
              rdescript="Excel: Inserts Entire Column to The Left of Current Column"),
        "insert cell [to the] left":
            R(Key("cs-plus, a-i, enter"),
              rdescript="Excel: Insert Single Cell to The Left of Current Cell"),
        "insert cell above":
            R(Key("cs-plus, a-d, enter"),
              rdescript="Excel: Insert Single Cell above Current Cell"),
        "insert pivot table":
            R(Key("a-n, v"), rdescript="Excel: Insert Pivot Table"),
        "insert pivot chart":
            R(Key("a-n, s, z, c"), rdescript="Excel: Insert Pivot Chart"),
        "add-ins":
            R(Key("a-t, i"), rdescript="Excel: Go to Add Ins"),
        "add border":
            R(Key("cs-ampersand"), rdescript="Excel: Add Border"),
        "arrange Windows":
            R(Key("a-w/10, a"), rdescript="Excel: Arrange Windows"),
        "auto sum":
            R(Key("a-equal"), rdescript="Excel: Auto Sum"),
        "freeze panes":
            R(Key("a-w, f"), rdescript="Excel: Freeze Panes"),

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
            R(Key("f2"), rdescript="Edits The Cell Rather Than Fully Replacing; Also Toggles Between Edit and Enter Mode"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
        IntegerRefST("m", 1, 10),
        IntegerRefST("numbers", 1, 100),
        IntegerRefST("row_1", 1, 100),
        IntegerRefST("row_2", 1, 100),
        # when I set the sequence length to 3 I got the grammar too complex Natlink error.
        Choice("column_1", make_sequence_dict_up_to_length(word_to_letter, 2)),
        Choice("column_2", make_sequence_dict_up_to_length(word_to_letter, 2)),
    ]
    defaults = {"n": 1, "dict": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="excel")
grammar = Grammar("excel", context=context)

if settings.SETTINGS["apps"]["excel"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(ExcelRule())
    else:
        rule = ExcelRule(name="excel")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
