'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Mimic

from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class CPP(MergeRule):
    pronunciation = "C plus plus"

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
            R(Text("for_each (TOKEN, TOKEN, TOKEN);")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("(int)")),
        SymbolSpecs.TO_FLOAT:
            R(Text("(double)")),
        SymbolSpecs.TO_STRING:
            R(Text("std::to_string()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text("&&")),
        SymbolSpecs.OR:
            R(Text("||")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("cout <<")),
        #
        SymbolSpecs.IMPORT:
            R(Text("#include")),
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

        # C++ specific
        "public":
            R(Text("public ")),
        "private":
            R(Text("private ")),
        "static":
            R(Text("static ")),
        "final":
            R(Text("final ")),
        "static cast integer":
            R(Text("static_cast<int>()") + Key("left")),
        "static cast double":
            R(Text("static_cast<double>()") + Key("left")),
        "([global] scope | name)":
            R(Text("::")),
        "Vic":
            R(Text("vector")),
        "pushback":
            R(Text("push_back")),
        "standard":
            R(Text("std")),
        "constant":
            R(Text("const")),
        "array":
            R(Mimic("brackets")),

        #http://www.learncpp.com/cpp-tutorial/67-introduction-to-pointers/
        "(reference to | address of)":
            R(Text("&")),
        "(pointer | D reference)":
            R(Text("*")),
        "member":
            R(Text("->")),
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
            R(Text("()?;") + (Key("left")*3)),
    }

    extras = []
    defaults = {}


def get_rule():
    return CPP, RuleDetails(ccrtype=CCRType.GLOBAL)
