from dragonfly import Mimic

from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class CSharp(MergeRule):
    pronunciation = "C sharp"

    mapping = {
        SymbolSpecs.IF:
            R(Key("i, f, lparen, rparen, leftbrace, enter,up,left")),
        SymbolSpecs.ELSE:
            R(Key("e, l, s, e, leftbrace, enter")),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch(){\ncase : break;\ndefault: break;") + Key("up,up,left,left")),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left")),
        SymbolSpecs.BREAK:
            R(Text("break;")),
        SymbolSpecs.DEFAULT:
            R(Text("default: ")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do {}") + Key("left, enter:2")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (int i=0; i<TOKEN; i++)")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("foreach (TOKEN in Collection)")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("Convert.ToInt32()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("Convert.ToDouble()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Text("Convert.ToString()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text("&&")),
        SymbolSpecs.OR:
            R(Text("||")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("Console.WriteLine()") + Key("left")),

        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN TOKEN(){}") + Key("left")),
        SymbolSpecs.CLASS:
            R(Text("class TOKEN{}") + Key("left")),
        #
        SymbolSpecs.COMMENT:
            R(Text("//")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left, left")),
        #
        SymbolSpecs.NULL:
            R(Text("null")),
        #
        SymbolSpecs.RETURN:
            R(Text("return")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # C# specific
        "using":
            R(Text("using")),
        "enum":
            R(Text("enum TOKEN {}") + Key("left")),
        "struct":
            R(Text("struct TOKEN {}") + Key("left")),
        "interface":
            R(Text("interface TOKEN {}") + Key("left")),
        "public":
            R(Text("public ")),
        "private":
            R(Text("private ")),
        "static":
            R(Text("static ")),
        "internal":
            R(Text("internal ")),
        "cast integer":
            R(Text("(int)") + Key("left")),
        "cast double":
            R(Text("(double)") + Key("left")),
        "constant":
            R(Text("const")),
        "array":
            R(Mimic("brackets")),
        "list":
            R(Text("List<>") + Key("left")),
        "var":
            R(Text("var TOKEN = TOKEN;")),
        "(lambda|goes to)":
            R(Text("=>")),
        "new new":
            R(Text("new ")),
        "integer":
            R(Text("int ")),
        "double":
            R(Text("double ")),
        "character":
            R(Text("char ")),
        "big integer":
            R(Text("Integer")),
        "string":
            R(Text("string ")),
        "ternary":
            R(Text("()?t:f") + (Key("left")*5)),
    }

    extras = []
    defaults = {}


def get_rule():
    return CSharp, RuleDetails(ccrtype=CCRType.GLOBAL)
