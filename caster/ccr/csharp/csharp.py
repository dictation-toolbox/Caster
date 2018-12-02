'''
Created on Sep 26, 2015

@author: synkarius
'''

from dragonfly import Mimic

from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class CSharp(MergeRule):
    pronunciation = "C sharp"

    mapping = {
        SymbolSpecs.IF:
            R(Key("i, f, lparen, rparen, leftbrace, enter,up,left"), rdescript="C#: If"),
        SymbolSpecs.ELSE:
            R(Key("e, l, s, e, leftbrace, enter"), rdescript="C#: Else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch(){\ncase : break;\ndefault: break;") + Key("up,up,left,left"),
              rdescript="C#: Switch"),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left"), rdescript="C#: Case"),
        SymbolSpecs.BREAK:
            R(Text("break;"), rdescript="C#: Break"),
        SymbolSpecs.DEFAULT:
            R(Text("default: "), rdescript="C#: Default"),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do {}") + Key("left, enter:2"), rdescript="C#: Do Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left"), rdescript="C#: While"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (int i=0; i<TOKEN; i++)"), rdescript="C#: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("foreach (TOKEN in Collection)"), rdescript="C#: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("Convert.ToInt32()") + Key("left"),
              rdescript="C#: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("Convert.ToDouble()") + Key("left"),
              rdescript="C#: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("Convert.ToString()") + Key("left"),
              rdescript="C#: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text("&&"), rdescript="C#: And"),
        SymbolSpecs.OR:
            R(Text("||"), rdescript="C#: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="C# Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("Console.WriteLine()") + Key("left"), rdescript="C#: Print"),

        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN TOKEN(){}") + Key("left"), rdescript="C#: Function"),
        SymbolSpecs.CLASS:
            R(Text("class TOKEN{}") + Key("left"), rdescript="C#: Class"),
        #
        SymbolSpecs.COMMENT:
            R(Text("//"), rdescript="C#: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left, left"), rdescript="C#: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("null"), rdescript="C#: Null Value"),
        #
        SymbolSpecs.RETURN:
            R(Text("return"), rdescript="C#: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="C#: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="C#: False"),

        # C# specific
        "using":
            R(Text("using"), rdescript="C#: Using"),
        "enum":
            R(Text("enum TOKEN {}") + Key("left"), rdescript="C#: Enum"),
        "struct":
            R(Text("struct TOKEN {}") + Key("left"), rdescript="C#: Struct"),
        "interface":
            R(Text("interface TOKEN {}") + Key("left"), rdescript="C#: Struct"),
        "public":
            R(Text("public "), rdescript="C#: Public"),
        "private":
            R(Text("private "), rdescript="C#: Private"),
        "static":
            R(Text("static "), rdescript="C#: Static"),
        "internal":
            R(Text("internal "), rdescript="C#: Internal"),
        "cast integer":
            R(Text("(int)") + Key("left"), rdescript="C#:  Cast Integer"),
        "cast double":
            R(Text("(double)") + Key("left"), rdescript="C#: Cast Double"),
        "constant":
            R(Text("const"), rdescript="C#: Constant"),
        "array":
            R(Mimic("brackets"), rdescript="C#: Array"),
        "list":
            R(Text("List<>") + Key("left"), rdescript="C# List"),
        "var":
            R(Text("var TOKEN = TOKEN;"), rdescript="C# variable"),
        "(lambda|goes to)":
            R(Text("=>"), rdescript="C#: lambda"),
        "new new":
            R(Text("new "), rdescript="C#: New"),
        "integer":
            R(Text("int "), rdescript="C#: Integer"),
        "double":
            R(Text("double "), rdescript="C#: Double"),
        "character":
            R(Text("char "), rdescript="C#: Character"),
        "big integer":
            R(Text("Integer"), rdescript="C#: Big Integer"),
        "string":
            R(Text("string "), rdescript="C#: String"),
        "ternary":
            R(Text("()?t:f") + (Key("left")*5), rdescript="C#: Ternary"),
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(CSharp())
