from dragonfly import (Key, Text, Choice)

from caster.lib import settings


def get_alphabet_choice(spec):
    return Choice(spec,
              {
            "arch": "a", 
            "brov": "b", 
            "chum": "c",
            "dell": "d",
            "etch": "e",
            "fox": "f",
            "goof": "g", 
            "hark": "h",
            "ice": "i",
            "jinks": "j",
            "koop": "k",
            "lug": "l",
            "moke": "m",
            "nerb": "n",
            "ork": "o",
            "pooch": "p",
            "quash": "q",
            "rosh": "r",
            "souk": "s",
            "teek": "t",
            "unks": "u",
            "verge": "v",
            "womp": "w",
            "trex": "x",
            "yang": "y",
            "zooch": "z",
               })

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
    result=[ "eins",
             "tsvai",
             "dry",
             "fear",
             "foonf",
             "zeks",
             "zeeben",
             "acht",
             "known"]
    if not settings.SETTINGS["miscellaneous"]["integer_remap_opt_in"]:
        result[1]="two"
        result[2]="three"
        result[3]="four"
        result[4]="five"
        result[7]="eight"
    return result

def numbers_map_1_to_9():
    result = {}
    l = numbers_list_1_to_9()
    for i in range(0, len(l)):
        result[l[i]] = i+1
    return result


def numbers2(wnKK):
    Text(str(wnKK)).execute()

def letters(big, dict1, dict2, letter):
    '''used with alphabet.txt'''
    d1 = str(dict1)
    if d1 != "":
        Text(d1).execute()
    if str(big) != "":
        Key("shift:down").execute()
    letter.execute()
    if str(big) != "":
        Key("shift:up").execute()
    d2 = str(dict2)
    if d2 != "":
        Text(d2).execute()
    
def letters2(big, letter):
    if str(big) != "":
        Key("shift:down").execute()
    Key(letter).execute()
    if str(big) != "":
        Key("shift:up").execute()
