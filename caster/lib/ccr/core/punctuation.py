from dragonfly.actions.action_base import Repeat
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text

from caster.lib import control
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class Punctuation(MergeRule):
    pronunciation = CCRMerger.CORE[3]
    
    mapping = {
        "semper":                           R(Key("semicolon"), rdescript="Semicolon"),        
        "quotes":                           R(Key("dquote,dquote,left"), rdescript="Quotation Marks"),
        "thin quotes":                      R(Key("apostrophe,apostrophe,left"), rdescript="Thin Quotation Marks"),               
        "[is] greater than":                R(Key("rangle"), rdescript="> Comparison"),
        "[is] less than":                   R(Key("langle"), rdescript="< Comparison"),
        "[is] greater [than] [or] equal [to]":  R(Key("rangle, equals"), rdescript=">= Comparison"),
        "[is] less [than] [or] equal [to]":     R(Key("langle, equals"), rdescript="<= Comparison"),
        "[is] equal to":                    R(Key("equals,equals"), rdescript="Equality"),
        "equals":                           R(Key("equals"), rdescript="Equals Sign"),
        "prekris":                          R(Key("lparen, rparen, left"), rdescript="Parentheses"),
        "brax":                             R(Key("lbracket, rbracket, left"), rdescript="Square Brackets"),
        "curly":                            R(Key("lbrace, rbrace, left"), rdescript="Curly Braces"),
        "angle":                            R(Key("langle, rangle, left"), rdescript="Angle Brackets"),
        "plus":                             R(Text("+"), rdescript="Plus Sign"),
        "minus":                            R(Text("-"), rdescript="Dash"),
        "pipe (sim | symbol)":              R(Text("|"), rdescript="Pipe Symbol"),
        'ace [<npunc>]':                    R(Key("space"), rdescript="Space") * Repeat(extra="npunc"),
        "clamor":                           R(Text("!"), rdescript="Exclamation Mark"),
        "deckle":                           R(Text(":"), rdescript="Colon"),
        "starling":                         R(Key("asterisk"), rdescript="Asterisk"),
        "questo":                           R(Text("?"), rdescript="Question Mark"),
        "comma":                            R(Text(","), rdescript="Comma"),
        "carrot":                           R(Text("^"), rdescript="Carat"),                     
        "(period | dot)":                   R(Text("."), rdescript="Dot"),
        "atty":                             R(Text("@"), rdescript="At Sign"),
        "hash tag":                         R(Text("#"), rdescript="Hash Tag"),
        "apostrophe":                       R(Text("'"), rdescript="Apostrophe"),
        "underscore":                       R(Text("_"), rdescript="Underscore"),        
        "backslash":                        R(Text("\\"), rdescript="Back Slash"),
        "slash":                            R(Text("/"), rdescript="Forward Slash"),
        "Dolly":                            R(Text("$"), rdescript="Dollar Sign"),
        "modulo":                           R(Key("percent"), rdescript="Percent Sign"),
        'tabby [<npunc>]':                  R(Key("tab"), rdescript="Tab") * Repeat(extra="npunc"),
        "boom":                             R(Text(", "), rdescript="Comma + Space"),
        "ampersand":                        R(Key("ampersand"), rdescript="Ampersand"),
        
          }
 

    extras = [
            IntegerRefST("npunc", 0, 10),
    ]
    defaults = {
            "npunc": 1,
    }

control.nexus().merger.add_global_rule(Punctuation())
