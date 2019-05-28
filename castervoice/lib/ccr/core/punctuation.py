from dragonfly import Choice, Repeat

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

text_punc_dict = {
    "semper":                               ";",
    "[is] greater than":                    ">",  
    "[is] less than":                       "<",
    "[is] greater [than] [or] equal [to]": ">=",
    "[is] less [than] [or] equal [to]":    "<=",
    "[is] equal to":                       "==",
    "equals":                               "=",
    "plus":                                 "+",
    "minus":                                "-",
    "pipe (sim | symbol)":                  "|",
    "ace":                                  " ",
    "clamor":                               "!",     
    "deckle":                               ":",
    "starling":                             "*",  
    "questo":                               "?", 
    "comma":                                ",",  
    "carrot":                               "^", 
    "(period | dot)":                       ".", 
    "(atty | at symbol)":                   "@", 
    "hash tag":                             "#",
    "apostrophe | single quote | chicky":   "'",   
    "underscore":                           "_",
    "backslash":                           "\\", 
    "slash":                                "/",
    "Dolly":                                "$",
    "modulo":                               "%",
    "ampersand":                            "&",
    "tilde":                                "~",
    "(left prekris | lay)":                 "(",
    "(right prekris | ray)":                ")",
    "(left brax | lack)":                   "[",
    "(right brax | rack)":                  "]",
    "(left angle | lang)":                  "<",
    "(right angle | rang)":                 ">",
    "(left curly | lace)":                  "{",
    "(right curly | race)":                 "}",
    "ticky":                                "`",
    "chocky":                              "\"",
}

double_text_punc_dict = {
    "quotes":                            "\"\"",
    "thin quotes":                         "''",
    "bakes":                               "``",
    "prekris":                             "()",
    "brax":                                "[]",
    "curly":                               "{}",
    "angle":                               "<>",
}

class Punctuation(MergeRule):
    pronunciation = CCRMerger.CORE[3]

    mapping = {
        "[<long>] <text_punc> [<npunc>]": 
            R(Text("%(long)s" + "%(text_punc)s" + "%(long)s"))*Repeat(extra="npunc"),
        "<double_text_punc>": 
            R(Text("%(double_text_punc)s") + Key("left")),
        'tabby [<npunc>]':
            R(Key("tab"), rdescript="Core: Tab")*Repeat(extra="npunc"),
        'lay tabby [<npunc>]':
            R(Key("s-tab"), rdescript="Core: Shift Tab")*Repeat(extra="npunc"),
        "boom [<npunc>]":
            R(Text(", "), rdescript="Core: Comma + Space")*Repeat(extra="npunc"),
    }

    extras = [
        IntegerRefST("npunc", 0, 10),
        Choice(
            "long", {
                "long": " ",
            }),
        Choice(
            "text_punc", text_punc_dict),
        Choice(
            "double_text_punc", double_text_punc_dict)
    ]
    defaults = {
        "npunc": 1,
        "long": "",
    }

control.nexus().merger.add_global_rule(Punctuation())
