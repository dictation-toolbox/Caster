from dragonfly import Choice, Repeat

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

text_punc_dict = {
    "ace":                                  " ",
    "clamor":                               "!",     
    "chocky":                              "\"",
    "hash tag":                             "#",
    "Dolly":                                "$",
    "modulo":                               "%",
    "ampersand":                            "&",
    "apostrophe | single quote | chicky":   "'",   
    "left prekris":                         "(",
    "right prekris":                        ")",
    "starling":                             "*",  
    "plus":                                 "+",
    "comma":                                ",",  
    "minus":                                "-",
    "period | dot":                       ".", 
    "slash":                                "/",
    "deckle":                               ":",
    "semper":                               ";",
    "[is] less than | left angle":          "<",
    "[is] less [than] [or] equal [to]":    "<=",
    "equals":                               "=",
    "[is] equal to":                       "==",
    "[is] greater than | right angle":      ">",  
    "[is] greater [than] [or] equal [to]": ">=",
    "questo":                               "?", 
    "(atty | at symbol)":                   "@", 
    "left brax":                            "[",
    "backslash":                           "\\", 
    "right brax":                           "]",
    "carrot":                               "^", 
    "underscore":                           "_",
    "ticky":                                "`",
    "left curly":                           "{",
    "pipe (sim | symbol)":                  "|",
    "right curly":                          "}",
    "tilde":                                "~",
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
        "tabby [<npunc>]":
            R(Key("tab"), rdescript="Core: Tab")*Repeat(extra="npunc"),
        "(back | shin) tabby [<npunc>]":
            R(Key("s-tab"), rdescript="Core: Shift Tab")*Repeat(extra="npunc"),
        "boom [<npunc>]":
            R(Text(", "), rdescript="Core: Comma + Space")*Repeat(extra="npunc"),
        "ace [<npunc100>]":
            R(Text(" "), rdescript="Core: Space")*Repeat(extra="npunc100"),
    }

    extras = [
        IntegerRefST("npunc", 0, 10),
        IntegerRefST("npunc100", 0, 100),
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
