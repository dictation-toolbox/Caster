from dragonfly import Dictation, Choice

from castervoice.lib import utilities
from castervoice.lib.actions import Text, Key
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.util import recognition_history

_DBL_FIX_HISTORY = recognition_history.get_and_register_history(1)


def fix_dragon_double():
    try:
        lr = _DBL_FIX_HISTORY[len(_DBL_FIX_HISTORY) - 1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del").execute()
    except Exception:
        utilities.simple_log(False)


def cap_dictation(dictation):
    input_list = str(dictation).split(" ")
    output_list = []
    for i in range(len(input_list)):
        if input_list[i] == "cap":
            input_list[i + 1] = input_list[i + 1].title()
        else:
            output_list.append(input_list[i])
    Text(" ".join(output_list)).execute()


# extras are common to both classes in this file
def extras_for_whole_file():
    return [
        Dictation("text"),
        IntegerRefST("n10", 1, 10),
        Choice("first_second_third", {
            "first": 0,
            "second": 1,
            "third": 2,
            "fourth": 3,
            "fifth": 4,
            "six": 5,
            "seventh": 6
        }),
    ]


def defaults_for_whole_file():
    return {
        "n10": 1,
        "text": "",
    }
