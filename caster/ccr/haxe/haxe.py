from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class Haxe(MergeRule):
    pronunciation = "hacks"

    mapping = {
        SymbolSpecs.IF:
            R(Key("i, f, lparen, rparen, left"), rdescript="Haxe: If"),
        SymbolSpecs.ELSE:
            R(Key("e, l, s, e"), rdescript="Haxe: Else"),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch(){\ncase : TOKEN;\ndefault: TOKEN;") + Key("up,up,left,left"),
              rdescript="Haxe: Switch"),
        SymbolSpecs.CASE:
            R(Text("case :") + Key("left"), rdescript="Haxe: Case"),
        SymbolSpecs.BREAK:
            R(Text("break;"), rdescript="Haxe: Break"),
        SymbolSpecs.DEFAULT:
            R(Text("default: "), rdescript="Haxe: Default"),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("do TOKEN while()") + Key("left, enter:2"), rdescript="Haxe: Do Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ()") + Key("left"), rdescript="Haxe: While"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for (i in 0...TOKEN)"), rdescript="Haxe: For i Loop"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for (TOKEN in TOKEN)"), rdescript="Haxe: For Each Loop"),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("Std.int()") + Key("left"), rdescript="Haxe: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("Std.parseFloat()") + Key("left"),
              rdescript="Haxe: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("Std.string()") + Key("left"), rdescript="Haxe: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text("&&"), rdescript="Haxe: And"),
        SymbolSpecs.OR:
            R(Text("||"), rdescript="Haxe: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Haxe Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("trace()") + Key("left"), rdescript="Haxe: Print"),

        #
        SymbolSpecs.FUNCTION:
            R(Text("function "), rdescript="Haxe: Function"),
        SymbolSpecs.CLASS:
            R(Text("class "), rdescript="Haxe: Class"),
        #
        SymbolSpecs.COMMENT:
            R(Text("//"), rdescript="Haxe: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left, left"), rdescript="Haxe: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("null"), rdescript="Haxe: Null Value"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Haxe: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Haxe: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Haxe: False"),

        # Haxe specific
        "import":
            R(Text("import "), rdescript="Haxe: Import"),
        "new new":
            R(Text("new "), rdescript="Haxe: New"),
        "instance of":
            R(Text("Std.is()") + Key("left"), rdescript="Haxe: Infer Type"),
        "anon funk":
            R(Text("->"), rdescript="Haxe: Lambda"),
        "map of":
            R(Text("Map<TOKEN, TOKEN>()"), rdescript="Haxe: Map"),
        "array of":
            R(Text("Array<TOKEN>()") + Key("left"), rdescript="Haxe: Array"),
        "far | variable":
            R(Text("var "), rdescript="Haxe: Variable"),
        "boolean":
            R(Text("Bool "), rdescript="Haxe: Boolean"),
        "integer":
            R(Text("Int "), rdescript="Haxe: Big Integer"),
        "double":
            R(Text("Float "), rdescript="Haxe: Float"),
        "dynamic":
            R(Text("Dynamic"), rdescript="Haxe: Dynamic"),
        "void":
            R(Text("Void"), rdescript="Haxe: Void"),
        "string":
            R(Text("String "), rdescript="Haxe: String"),
        "public":
            R(Text("public "), rdescript="Haxe: Public"),
        "private":
            R(Text("private "), rdescript="Haxe: Private"),
        "static":
            R(Text("static "), rdescript="Haxe: Static"),
        "this":
            R(Text("this"), rdescript="Haxe: This"),
        "safe cast":
            R(Text("cast (TOKEN, TOKEN)"), rdescript="Haxe: Safe Cast"),
        "get class":
            R(Text("Type.getClass()") + Key("left"), rdescript="Haxe: Get Class"),
        "get name":
            R(Text("Type.getClassName()") + Key("left"), rdescript="Haxe: Get Class Name")
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(Haxe())
