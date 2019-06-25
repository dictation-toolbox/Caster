'''
Created on May 26, 2017

@author: shippy
'''
from castervoice.lib.imports import *

class MatlabNon(MappingRule):
    mapping = {
        "section": R(Key("percent, percent, enter")),
    }


class Matlab(MergeRule):
    auto = [".M", ".m"]
    pronunciation = "matlab"
    non = MatlabNon

    mapping = {
        SymbolSpecs.IF:
            R(Text("if ")),
        SymbolSpecs.ELSE:
            R(Text("else ") + Key("enter")),
        #
        # (no switch in Matlab)
        SymbolSpecs.BREAK:
            R(Text("break")),
        #
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for m = 1:")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for ")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ")),
        # (no do-while in Matlab)
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("str2num()") + Key("left")),
        SymbolSpecs.TO_FLOAT:
            R(Text("str2num()") + Key("left")),
        SymbolSpecs.TO_STRING:
            R(Text("num2str()") + Key("left")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("~")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("disp()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("library()") + Key("left")),
        #
        SymbolSpecs.FUNCTION:
            R(Text("function [] = ") + Key("left:4")),
        SymbolSpecs.CLASS:
            R(Text("classdef ")),
        #
        SymbolSpecs.COMMENT:
            R(Key("percent")),
        SymbolSpecs.LONG_COMMENT:
            R(Key('percent, lbracket, enter:2, percent, rbracket') + Key("up")),
        #
        SymbolSpecs.NULL:
            R(Text("NaN")),
        #
        SymbolSpecs.RETURN:
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # Matlab specific
        "assign":
            R(Text(" = ")),
        "shell iffae | LFA":
            R(Text("elseif ")),
        "length of":
            R(Text("length()") + Key("left")),
        "sprint F":
            R(Text("sprintf()") + Key("left")),
    }

    extras = [
        Dictation("text"),
    ]
    defaults = {}


control.global_rule(Matlab())
