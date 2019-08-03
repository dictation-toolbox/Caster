from dragonfly import Choice, Repeat

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

enclosure = {
    "quotes": "\"",
    "thin quotes": "'",
    "tickris": "`",
    "dunder": "__",
    "starry": "**",
    "spacer": " ",
    "dollz": "$",
    "(bling | blinger)": "$$",
    "prekris": ("(",")"),
    "precoat": ("(\"", "\""),
    "brax": ("[","]"),
    "curly": ("{","}"),
    "angle": ("<", ">"),
    "triple tick": ("```\n", "\n```"),
    "varib": ("`<", ">`"),
    }

def make_2tuple_into_string(input):
    if isinstance(input, tuple):
        return input[0] + input[1]
    else:
        return input
inv_dtpb = {make_2tuple_into_string(v): k for k, v in enclosure.iteritems()}

text_punc_dict = {
    "ace":                                                " ",
    "clamor":                                             "!",
    "chocky":                                            "\"",
    "hash tag":                                           "#",
    "Dolly":                                              "$",
    "modulo":                                             "%",
    "ampersand":                                          "&",
    "apostrophe | single quote | chicky":                 "'",
    "left " + inv_dtpb["()"]:                             "(",
    "right " + inv_dtpb["()"]:                            ")",
    "starling":                                           "*",
    "plus":                                               "+",
    "comma":                                              ",",
    "minus":                                              "-",
    "period | dot":                                       ".",
    "slash":                                              "/",
    "deckle":                                             ":",
    "semper":                                             ";",
    "[is] less than | left " + inv_dtpb["<>"]:            "<",
    "[is] less [than] [or] equal [to]":                  "<=",
    "equals":                                             "=",
    "[is] equal to":                                     "==",
    "[is] greater than | right " + inv_dtpb["<>"]:        ">",
    "[is] greater [than] [or] equal [to]":               ">=",
    "questo":                                             "?",
    "(atty | at symbol)":                                 "@",
    "left " + inv_dtpb["[]"]:                             "[",
    "backslash":                                         "\\",
    "right " + inv_dtpb["[]"]:                            "]",
    "carrot":                                             "^",
    "underscore":                                         "_",
    "ticky | ((left | right) " +  inv_dtpb["`"] + " )":  "`",
    "left " + inv_dtpb["{}"]:                             "{",
    "pipe (sim | symbol)":                                "|",
    "right " + inv_dtpb["{}"]:                            "}",
    "tilde":                                              "~",
}

class Punctuation(MergeRule):
    pronunciation = CCRMerger.CORE[3]

    mapping = {
        "[<long>] <text_punc> [<npunc>]":
            R(Text("%(long)s" + "%(text_punc)s" + "%(long)s"))*Repeat(extra="npunc"),
        # For some reason, this one doesn't work through the other function
        "[<long>] backslash [<npunc>]":
            R(Text("%(long)s" + "\\" + "%(long)s"))*Repeat(extra="npunc"),
        
        "tabby [<npunc>]":
            R(Key("tab"))*Repeat(extra="npunc"),
        "(back | shin) tabby [<npunc>]":
            R(Key("s-tab"))*Repeat(extra="npunc"),
        "boom [<npunc>]":
            R(Text(", "))*Repeat(extra="npunc"),
        "bam [<npunc>]":
            R(Text(". "))*Repeat(extra="npunc"),
        "ace [<npunc100>]":
            R(Text(" "))*Repeat(extra="npunc100"),
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
       
    ]
    defaults = {
        "npunc": 1,
        "npunc100": 1,
        "long": "",
    }

control.global_rule(Punctuation())
