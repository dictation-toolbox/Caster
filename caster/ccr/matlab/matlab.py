'''
Created on May 26, 2017

@author: shippy
'''

from dragonfly import Dictation, MappingRule

from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class MatlabNon(MappingRule):
    mapping = {
        "section": R(Key("percent, percent, enter"), rdescript="Matlab: Section"),
    }


class Matlab(MergeRule):
    auto = [".M", ".m"]
    pronunciation = "matlab"
    non = MatlabNon

    mapping = {
        SymbolSpecs.IF:
            R(Text("if "), rdescript="Matlab: If"),
        SymbolSpecs.ELSE:
            R(Text("else ") + Key("enter"), rdescript="Matlab: Else"),
        #
        # (no switch in Matlab)
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Matlab: Break"),
        #
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for m = 1:"), rdescript="Matlab: For Each Loop"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for "), rdescript="Matlab: For i Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while "), rdescript="Matlab: While"),
        # (no do-while in Matlab)
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("str2num()") + Key("left"), rdescript="Matlab: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("str2num()") + Key("left"),
              rdescript="Matlab: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("num2str()") + Key("left"), rdescript="Matlab: Convert To String"),
        #
        SymbolSpecs.AND:
            R(Text(" && "), rdescript="Matlab: And"),
        SymbolSpecs.OR:
            R(Text(" || "), rdescript="Matlab: Or"),
        SymbolSpecs.NOT:
            R(Text("~"), rdescript="Matlab: Not"),
        #
        SymbolSpecs.SYSOUT:
            R(Text("disp()") + Key("left"), rdescript="Matlab: Print"),
        #
        SymbolSpecs.IMPORT:
            R(Text("library()") + Key("left"), rdescript="Matlab: Import"),
        #
        SymbolSpecs.FUNCTION:
            R(Text("function [] = ") + Key("left:4"), rdescript="Matlab: Function"),
        SymbolSpecs.CLASS:
            R(Text("classdef "), rdescript="Matlab: Class"),
        #
        SymbolSpecs.COMMENT:
            R(Key("percent"), rdescript="Matlab: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Key('percent, lbracket, enter:2, percent, rbracket') + Key("up"),
              rdescript="Matlab: Long Comment"),
        #
        SymbolSpecs.NULL:
            R(Text("NaN"), rdescript="Matlab: Null"),
        #
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Matlab: Return"),
        #
        SymbolSpecs.TRUE:
            R(Text("true"), rdescript="Matlab: True"),
        SymbolSpecs.FALSE:
            R(Text("false"), rdescript="Matlab: False"),

        # Matlab specific
        "assign":
            R(Text(" = "), rdescript="Matlab: Assignment"),
        "shell iffae | LFA":
            R(Text("elseif "), rdescript="Matlab: Else If"),
        "length of":
            R(Text("length()") + Key("left"), rdescript="Matlab: Length"),
        "sprint F":
            R(Text("sprintf()") + Key("left"), rdescript="Matlab: Length"),
    }

    extras = [
        Dictation("text"),
    ]
    defaults = {}


control.nexus().merger.add_global_rule(Matlab())
