from dragonfly import Choice, Repeat

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class Punctuation(MergeRule):
    pronunciation = CCRMerger.CORE[3]

    mapping = {
        "semper":
            R(Key("semicolon"), rdescript="Core: Semicolon"),
        "quotes":
            R(Key("dquote,dquote,left"), rdescript="Core: Quotation Marks"),
        "thin quotes":
            R(Key("apostrophe,apostrophe,left"), rdescript="Core: Thin Quotation Marks"),
        "[is] greater than":
            R(Key("rangle"), rdescript="Core: > Comparison"),
        "[is] less than":
            R(Key("langle"), rdescript="Core: < Comparison"),
        "[is] greater [than] [or] equal [to]":
            R(Key("rangle, equals"), rdescript="Core: >= Comparison"),
        "[is] less [than] [or] equal [to]":
            R(Key("langle, equals"), rdescript="Core: <= Comparison"),
        "[is] equal to":
            R(Key("equals,equals"), rdescript="Core: Equality"),
        "prekris":
            R(Key("lparen, rparen, left"), rdescript="Core: Parentheses"),
        "brax":
            R(Key("lbracket, rbracket, left"), rdescript="Core: Square Brackets"),
        "curly":
            R(Key("lbrace, rbrace, left"), rdescript="Core: Curly Braces"),
        "angle":
            R(Key("langle, rangle, left"), rdescript="Core: Angle Brackets"),
        "[<long>] equals":
            R(Text("%(long)s" + "=" + "%(long)s"), rdescript="Core: Equals Sign"),
        "[<long>] plus":
            R(Text("%(long)s" + "+" + "%(long)s"), rdescript="Core: Plus Sign"),
        "[<long>] minus":
            R(Text("%(long)s" + "-" + "%(long)s"), rdescript="Core: Dash"),
        "pipe (sim | symbol)":
            R(Text("|"), rdescript="Core: Pipe Symbol"),
        "long pipe (sim | symbol)":
            R(Text(" | "), rdescript="Core: Pipe Symbol surrounded by spaces"),
        'ace [<npunc>]':
            R(Key("space"), rdescript="Core: Space")*Repeat(extra="npunc"),
        "clamor":
            R(Text("!"), rdescript="Core: Exclamation Mark"),
        "deckle":
            R(Text(":"), rdescript="Core: Colon"),
        "long deckle":
            R(Key("right") + Text(": "), rdescript="Core: move right type colon then space"),
        "starling":
            R(Key("asterisk"), rdescript="Core: Asterisk"),
        "questo":
            R(Text("?"), rdescript="Core: Question Mark"),
        "comma":
            R(Text(","), rdescript="Core: Comma"),
        "carrot":
            R(Text("^"), rdescript="Core: Carat"),
        "(period | dot)":
            R(Text("."), rdescript="Core: Dot"),
        "atty":
            R(Text("@"), rdescript="Core: At Sign"),
        "hash tag":
            R(Text("#"), rdescript="Core: Hash Tag"),
        "apostrophe":
            R(Text("'"), rdescript="Core: Apostrophe"),
        "underscore":
            R(Text("_"), rdescript="Core: Underscore"),
        "backslash":
            R(Text("\\"), rdescript="Core: Back Slash"),
        "slash":
            R(Text("/"), rdescript="Core: Forward Slash"),
        "Dolly":
            R(Text("$"), rdescript="Core: Dollar Sign"),
        "modulo":
            R(Key("percent"), rdescript="Core: Percent Sign"),
        'tabby [<npunc>]':
            R(Key("tab"), rdescript="Tab")*Repeat(extra="npunc"),
        "(back tabby | shin tabby) [<npunc>]": R(Key("s-tab"),
            rdescript="shift + tab") * Repeat(extra='npunc'),   
        "boom":
            R(Text(", "), rdescript="Core: Comma + Space"),
        "ampersand":
            R(Key("ampersand"), rdescript="Core: Ampersand"),
        "tilde":
            R(Key("tilde"), rdescript="Core: Tilde"),

    }

    extras = [
        IntegerRefST("npunc", 0, 10),
        Choice("long", {
              "long": " ",
        }),

    ]
    defaults = {
        "npunc": 1,
        "long": "",
    }


control.nexus().merger.add_global_rule(Punctuation())
