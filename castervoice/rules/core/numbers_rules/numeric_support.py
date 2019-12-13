from castervoice.lib import settings
from castervoice.lib.actions import Text

def word_number(wn):
    numbers_to_words = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    }
    Text(numbers_to_words[int(wn)]).execute()


def numbers_list_1_to_9():
    result = ["one", "torque", "traio", "fairn", "faif", "six", "seven", "eigen", "nine"]
    if not settings.SETTINGS["miscellaneous"]["integer_remap_opt_in"]:
        result[1] = "two"
        result[2] = "three"
        result[3] = "four"
        result[4] = "five"
        result[7] = "eight"
    return result


def numbers_map_1_to_9():
    result = {}
    l = numbers_list_1_to_9()
    for i in range(0, len(l)):
        result[l[i]] = i + 1
    return result


def numbers2(wnKK):
    Text(str(wnKK)).execute()
