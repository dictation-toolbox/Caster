from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Haxe(MergeRule):
    pronunciation = "hacks"

    mapping = {
        SymbolSpecs.IF:
            R(Key("i, f, lparen, rparen, left")),
        SymbolSpecs.ELSE:
            R(Key("e, l, s, e")),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch(){\ncase : TOKEN;\ndefault: TOKEN;") + Key("up,up,left,left")),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left")),
        SymbolSpecs.BREAK:
            R(Text("break;")),
        SymbolSpecs.DEFAULT:
            R(Text("default: ")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do TOKEN while()") + Key("left, enter:2")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (i in 0...TOKEN)")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for (TOKEN in TOKEN)")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("Std.int()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("Std.parseFloat()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Text("Std.string()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text("&&")),
        SymbolSpecs.OR:
            R(Text("||")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("trace()") + Key("left")),

        #
        SymbolSpecs.FUNCTION:
            R(Text("function ")),
        SymbolSpecs.CLASS:
            R(Text("class ")),
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
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # Haxe specific
        "import":
            R(Text("import ")),
        "new new":
            R(Text("new ")),
        "instance of":
            R(Text("Std.is()") + Key("left")),
        "anon funk":
            R(Text("->")),
        "map of":
            R(Text("Map<TOKEN, TOKEN>()")),
        "array of":
            R(Text("Array<TOKEN>()") + Key("left")),
        "far | variable":
            R(Text("var ")),
        "boolean":
            R(Text("Bool ")),
        "integer":
            R(Text("Int ")),
        "double":
            R(Text("Float ")),
        "dynamic":
            R(Text("Dynamic")),
        "void":
            R(Text("Void")),
        "string":
            R(Text("String ")),
        "public":
            R(Text("public ")),
        "private":
            R(Text("private ")),
        "static":
            R(Text("static ")),
        "this":
            R(Text("this")),
        "safe cast":
            R(Text("cast (TOKEN, TOKEN)")),
        "get class":
            R(Text("Type.getClass()") + Key("left")),
        "get name":
            R(Text("Type.getClassName()") + Key("left"))
    }

    extras = []
    defaults = {}


def get_rule():
    return Haxe, RuleDetails(ccrtype=CCRType.GLOBAL)
