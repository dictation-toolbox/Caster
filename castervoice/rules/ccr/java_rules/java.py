from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Java(MergeRule):

    pronunciation = "java"

    mapping = {
        SymbolSpecs.IF:
            R(Text("if() {") + Key("enter,up,left")),
        SymbolSpecs.ELSE:
            R(Text("else {") + Key("enter")),
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
            R(Text("for (TOKEN TOKEN : TOKEN)")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("Integer.parseInt()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("Double.parseDouble()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Key("dquote, dquote, plus")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("java.lang.System.out.println()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("import ")),
        #
        SymbolSpecs.FUNCTION:
            R(Text("TOKEN() {}") + Key("left")),
        SymbolSpecs.CLASS:
            R(Text("class {}") + Key("left/5:2")),
        #
        SymbolSpecs.COMMENT:
            R(Text("//")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/**/") + Key("left,left")),
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

        # Java specific
        "it are in":
            R(Text("Arrays.asList(TOKEN).contains(TOKEN)")),
        "try states":
            R(Text("try")),
        "arrow":
            R(Text("->")),
        "public":
            R(Text("public ")),
        "private":
            R(Text("private ")),
        "static":
            R(Text("static ")),
        "final":
            R(Text("final ")),
        "void":
            R(Text("void ")),
        "cast to double":
            R(Text("(double)()") + Key("left")),
        "cast to integer":
            R(Text("(int)()") + Key("left")),
        "new new":
            R(Text("new ")),
        "integer":
            R(Text("int ")),
        "big integer":
            R(Text("Integer ")),
        "double tie":
            R(Text("double ")),
        "big double":
            R(Text("Double ")),
        "string":
            R(Text("String ")),
        "boolean":
            R(Text("boolean ")),
        "sub string":
            R(Text("substring")),
        "ternary":
            R(Text("()?:") + Key("left:3")),
        "this":
            R(Text("this")),
        "array list":
            R(Text("ArrayList")),
        "continue":
            R(Text("continue")),
        "sue iffae":
            R(Text("if ()") + Key("left")),
        "sue shells":
            R(Text("else") + Key("enter")),
        "shell iffae":
            R(Text("else if ()") + Key("left")),
        "throw exception":
            R(Text("throw new Exception()") + Key("left")),
        "character at":
            R(Text("charAt")),
        "is instance of":
            R(Text(" instanceof ")),
        "dock string":
            R(Text("/***/") + Key("left,left,enter")),
    }

    extras = []
    defaults = {}


def get_rule():
    return Java, RuleDetails(ccrtype=CCRType.GLOBAL)
