from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Javascript(MergeRule):

    mapping = {

        # CCR PROGRAMMING STANDARD
        SymbolSpecs.IF:
            R(Text("if () {}") + Key("left, enter:2, up")),
        SymbolSpecs.ELSE:
            R(Text("else {}") + Key("left, enter:2, up")),
        #
        SymbolSpecs.SWITCH:
            R(Text("switch () {}") + Key("left, enter:2, up")),
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
            R(Text("for (var i=0; i<TOKEN; i++)")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for (TOKEN in TOKEN)")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("parseInt()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("parseFloat()") + Key("left")),
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
            R(Text("console.log()") + Key("left")),
        #
        # (no imports in javascript)
        #
        SymbolSpecs.FUNCTION:
            R(Text("function TOKEN() {};") + Key("left:2, enter")),
	    SymbolSpecs.CLASS:
            R(Text("class  {}") + Key("left/5:3")),
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

        # JavaScript specific
        "anon funk":
            R(Text("() => {}") + Key("left:1, enter")),
        "timer":
            R(Text("setInterval()") + Key("left")),
        "timeout":
            R(Text("setTimeout()") + Key("left")),
        "document":
            R(Text("document")),
        "index of":
            R(Text("indexOf()") + Key("left")),
        "has own property":
            R(Text("hasOwnProperty()") + Key("left")),
        "length":
            R(Text("length")),
        "self":
            R(Text("self")),
        "push":
            R(Text("push")),
        "inner HTML":
            R(Text("innerHTML")),
        "new new":
            R(Text("new ")),
        "continue":
            R(Text("continue")),
        "this":
            R(Text("this")),
        "try":
            R(Text("try {}") + Key("left, enter:2, up")),
        "catch":
            R(Text("catch(e) {}") + Key("left, enter:2, up")),
        "throw":
            R(Text("throw ")),
        "instance of":
            R(Text("instanceof ")),
        "var":
            R(Text("var ")),
        "const":
            R(Text("const ")),
        "Let":
            R(Text("let ")),
        "shell iffae":
            R(Text("else if ()") + Key("left")),
        "a sink":
            R(Text("async ")),
        "await":
            R(Text("await ")),
    }

    extras = []
    defaults = {}


def get_rule():
    return Javascript, RuleDetails(ccrtype=CCRType.GLOBAL)
