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
        "sem":                              R(Key("semicolon"), rdescript="Semicolon"),
        "seem":                             R(Text(" ; "), rdescript="Semicolon with trailing space"),
        "coat":                             R(Key("dquote"), rdescript="Quotation mark"),
        "coats":                            R(Key("dquote,dquote,left"), rdescript="Quotation Marks"),
        "bip":                              R(Text("'"), rdescript="Apostrophe"),
        "bips":                             R(Key("apostrophe,apostrophe,left"), rdescript="Thin Quotation Marks"),
        "lug":                              R(Key("langle"), rdescript="> Comparison"),
        "lang":                             R(Key("space, langle, space"), rdescript=" > "),
        "rug":                              R(Key("rangle"), rdescript="< Comparison"),
        "rang":                             R(Key("space, rangle, space"), rdescript=" < "),
        "greegal":                          R(Key("rangle, equals"), rdescript=">= Comparison"),
        "legal":                            R(Key("langle, equals"), rdescript="<= Comparison"),
        "treacle | treek":                  R(Text(" === "), rdescript="triple equals"),
        "neck":                             R(Text(" != "), rdescript="!="),
        "isn't":                            R(Text(" !== "), rdescript="!=="),
        "quiv":                             R(Key("space, equals, equals, space"), rdescript="Equality"),
        "ghee":                             R(Key("equals"), rdescript="Equals Sign"),
        "gall":                             R(Text(" = "), rdescript="Equals with space"),
        "pleek":                            R(Text(" += "), rdescript="Plus-equals"),
        "pren":                             R(Key("lparen, rparen, left"), rdescript="Parentheses"),
        "proo":                             R(Key("lparen, rparen"), rdescript="Parentheses without centering"),
        "leppa":                            R(Key("lparen"), rdescript="Left paren"),
        "reppa":                            R(Key("rparen"), rdescript="Right paren"),
        "scare":                            R(Key("lbracket, rbracket, left"), rdescript="Square Brackets"),
        "skoo":                             R(Key("lbracket, rbracket"), rdescript="Square Brackets without centering"),
        "legga":                            R(Key("lbracket"), rdescript="Left bracket"),
        "regga":                            R(Key("rbracket"), rdescript="Right bracket"),
        "brace":                            R(Key("lbrace, rbrace, left"), rdescript="Curly Braces"),
        "(bris | block)":                   R(Key("lbrace, enter"), rdescript="braces with enter"),
        "spray":                            R(Text("{  }") + Key("left:2"), rdescript="spaced brace"),
        "lebra":                            R(Key("lbrace"), rdescript="Left brace"),
        "rebra":                            R(Key("rbrace"), rdescript="Right brace"),
        "brack":                            R(Key("langle, rangle, left"), rdescript="Angle Brackets"),
        "prexter":                          R(Key("lparen, dquote, dquote, rparen, left, left"), rdescript="Parens with quotes"),
        "raisin":                           R(Key("lparen, lbrace, rbrace, rparen, left, left"), rdescript="Parens with braces"),
        "bars":                             R(Key("lbrace, lbrace"), rdescript="Double brace"),
        "plus":                             R(Text("+"), rdescript="Plus Sign"),
        "ploose":                           R(Text(" + "), rdescript="Plus Sign with space"),
        "dish":                             R(Text("-"), rdescript="Dash"),
        "dash":                             R(Text("-"), rdescript="Dash with space"),
        "pip":                              R(Text("|"), rdescript="Pipe Symbol"),
        "pipe":                             R(Text(" | "), rdescript="Pipe Symbol with space"),
        'ta [<npunc>]':                     R(Key("space"), rdescript="Space") * Repeat(extra="npunc"),
        "bang":                             R(Text("!"), rdescript="Exclamation Mark"),
        "fizz":                             R(Text(":"), rdescript="Colon"),
        "face":                             R(Text(" : "), rdescript="Colon with space"),
        "deaf":                             R(Text(": "), rdescript="Colon + trailing space"),
        "star":                             R(Key("asterisk"), rdescript="Asterisk"),
        "stare":                            R(Text(" * "), rdescript="Asterisk with space"),
        "quick":                            R(Text("?"), rdescript="Question Mark"),
        "quack":                            R(Text(" ? "), rdescript="Question Mark with space"),
        "swip":                             R(Text(","), rdescript="Comma"),
        "swipe":                            R(Text(", "), rdescript="Comma + Space"),
        "krat":                             R(Text("^"), rdescript="Carat"),
        "(period | dot)":                   R(Text("."), rdescript="Dot"),
        "(at a | add a)":                   R(Text("@"), rdescript="At Sign"),
        "(crunch | kunch)":                 R(Text("#"), rdescript="Hash Tag"),
        "score":                            R(Text("_"), rdescript="Underscore"),
        "zip":                              R(Text("\\"), rdescript="Back Slash"),
        "slish":                            R(Text("/"), rdescript="Forward Slash"),
        "slash":                            R(Text(" / "), rdescript="Forward Slash with space"),
        "cash":                             R(Text("$"), rdescript="Dollar Sign"),
        "cent":                             R(Key("percent"), rdescript="Percent Sign"),
        'tabby [<npunc>]':                  R(Key("tab"), rdescript="Tab") * Repeat(extra="npunc"),
        "tick":                             R(Text("`"), rdescript="Backtick"),
        "amp":                              R(Key("ampersand"), rdescript="Ampersand"),
        "comp":                             R(Key("equals, dquote"), rdescript="equals string"),
          }


    extras = [
            IntegerRefST("npunc", 0, 10),
    ]
    defaults = {
            "npunc": 1,
    }

control.nexus().merger.add_global_rule(Punctuation())