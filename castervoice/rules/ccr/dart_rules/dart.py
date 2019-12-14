'''
Created on 2018-05-27 from javascript.py
@author: comodoro
'''
from dragonfly import Key

from castervoice.lib.actions import Text
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Dart(MergeRule):
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
            R(Text("for (var i = 0; i < TOKEN; i++)")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for (TOKEN in TOKEN)")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("int.parse()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("double.parse()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Text(".toString()")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left")),

        SymbolSpecs.IMPORT:
            R(Text("import ''") + Key("left")),

        SymbolSpecs.FUNCTION:
            R(Text("TOKEN() {}") + Key("left, enter")),

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

        # Dart specific
        "anon funk":
            R(Text("() => {}") + Key("left:1, enter")),
        "length":
            R(Text("length")),
        "self":
            R(Text("self")),
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
        "const":
            R(Text("const ")),
        "equals if null":
            R(Text(" ??= ")),
        "a sink":
            R(Text("async ")),
        "await":
            R(Text("await ")),
        "yield":
            R(Text("yield ")),
        "cascade":
            R(Key("enter") + Text("..")),
        "dock string":
            R(Text("/// ")),
        "var":
            R(Text("var TOKEN = ")),
    }

    extras = []
    defaults = {}


def get_rule():
    return Dart, RuleDetails(ccrtype=CCRType.GLOBAL)
