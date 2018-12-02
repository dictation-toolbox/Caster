'''
Created on 18 Mar 2018

@author: gerrish
'''

from dragonfly import Mimic, MappingRule, Function, Choice
from caster.lib import control
from caster.lib.actions import Key, Text
from caster.ccr.standard import SymbolSpecs
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

from vhdl_strings import *


def binary_string(digit, amount):
    return Text(str(digit)*amount).execute()


class VHDLnon(MappingRule):
    mapping = {
        "entity":
            R(entity_string, rdescript="Vhdl: Entity"),
        "Architecture":
            R(architecture_string, rdescript="Vhdl: Entity"),
        "component":
            R(component_string, rdescript="VHDL: component"),
        "component declaration":
            R(component_declaration_string, rdescript="VHDL: component"),
        SymbolSpecs.SWITCH:
            R(case_string, rdescript="VHDL: case statement"),
        SymbolSpecs.CASE:
            R(Text("case TOKEN is")),
        "process":
            R(process_string, rdescript="VHDL: process"),
        "generate components":
            R(for_generate_string, rdescript="VHDL: generate block"),
        "conditional component":
            R(if_generate_string, rdescript="VHDL: generate block"),
    }


class VHDL(MergeRule):

    pronunciation = "VHDL"
    non = VHDLnon

    mapping = {
        SymbolSpecs.COMMENT:
            R(Text("--"), rdescript="VHDL: Comment"),
        SymbolSpecs.IF:
            R(Text("if () then ") + Key("enter,enter") + Text("end if;") +
              Key("home,up,up"),
              rdescript="VHDL: If"),
        SymbolSpecs.ELSE:
            R(Key("e,l,s,e,enter"), rdescript="VHDL: If"),
        "alternate":
            R(Key("e,l,s,i, f,space,T,O,K,E,N,space,t,h,e,n,enter,tab"),
              rdescript="VHDL: If"),
        SymbolSpecs.CASE:
            R(Text("case TOKEN is") + Key("enter,tab"), rdescript="VHDL: case"),
        "when":
            R(Text("when "), rdescript="VHDL: when"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for  in to loop") + Key("left:12"), rdescript="VHDL: For loop"),
        "generate":
            R(Text("GENERATE"), rdescript="VHDL: generate"),
        "Input":
            R(Text("in"), rdescript="VHDL: In"),
        "Output":
            R(Text("out"), rdescript="VHDL: Output"),
        "Standard Logic":
            R(Text("std_logic"), rdescript="VHDL: Standard Logic"),
        "Standard Logic Vector":
            R(Text("std_logic_vector"), rdescript="VHDL: Standard Logic Vector"),
        "Constant":
            R(Text("constant : ") + Key("left,left"), rdescript="VHDL: Constant"),
        "Signal":
            R(Text("signal : ") + Key("left,left"), rdescript="VHDL: Signal"),
        "integer":
            R(Text("integer TOKEN to TOKEN"), rdescript="VHDL: integer"),
        "type":
            R(Text("type :") + Key("left"), rdescript="VHDL: type"),
        # Operators
        "Not Equal":
            R(Text("/="), rdescript="VHDL: Not Equal"),
        SymbolSpecs.NOT:
            R(Text("not"), rdescript="VHDL: NOT"),
        SymbolSpecs.OR:
            R(Text("or"), rdescript="VHDL: OR"),
        "not and":
            R(Text("nand"), rdescript="VHDL: NAND"),
        "XOR":
            R(Text("xor"), rdescript="VHDL: XOR"),
        "X NOR":
            R(Text("xnor"), rdescript="VHDL: XNOR"),
        "Assignment":
            R(Text(" <= ") + Key("left"), rdescript="VHDL: Assignment"),
        "Association":
            R(Text(' => ') + Key("left"), rdescript="VHDL: Association"),
        "Concatenate":
            R(Text(" & "), rdescript="VHDL: Concatenate"),
        "Down To":
            R(Text("downto"), rdescript="VHDL: DownTo"),
        "Up To":
            R(Text("upto"), rdescript="VHDL: UpTo"),
        "Input":
            R(Text("in"), rdescript="VHDL: In"),
        "Output":
            R(Text("out"), rdescript="VHDL: Output"),
        "Standard Logic":
            R(Text("std_logic"), rdescript="VHDL: Standard Logic"),
        "Standard Logic Vector":
            R(Text("std_logic_vector"), rdescript="VHDL: Standard Logic Vector"),
        "Constant":
            R(Text("constant : ") + Key("left,left"), rdescript="VHDL: Constant"),
        "Signal":
            R(Text("signal : ") + Key("left,left"), rdescript="VHDL: Signal"),
        "integer":
            R(Text("integer TOKEN to TOKEN"), rdescript="VHDL: integer"),
        "type":
            R(Text("type :") + Key("left"), rdescript="VHDL: type"),
        # Operators
        "Not Equal":
            R(Text("/="), rdescript="VHDL: Not Equal"),
        SymbolSpecs.NOT:
            R(Text("not"), rdescript="VHDL: NOT"),
        SymbolSpecs.OR:
            R(Text("or"), rdescript="VHDL: OR"),
        "not and":
            R(Text("nand"), rdescript="VHDL: NAND"),
        "XOR":
            R(Text("xor"), rdescript="VHDL: XOR"),
        "X NOR":
            R(Text("xnor"), rdescript="VHDL: XNOR"),
        "Assignment":
            R(Text(" <= ") + Key("left"), rdescript="VHDL: Assignment"),
        "Association":
            R(Text(' => ') + Key("left"), rdescript="VHDL: Association"),
        "Concatenate":
            R(Text(" & "), rdescript="VHDL: Concatenate"),
        "Down To":
            R(Text("downto"), rdescript="VHDL: DownTo"),
        "Up To":
            R(Text("upto"), rdescript="VHDL: UpTo"),
        SymbolSpecs.COMMENT:
            R(Text("-- "), rdescript="VHDL: Add Comment"),
        "binary [<amount>] <digit>":
            R(Function(binary_string), rdescript="Vhdl: binary string"),

        #VHDL specific
        "length":
            R(Text("length'"), rdescript="VHDL: length"),
        SymbolSpecs.TO_INTEGER:
            R(Text("to_integer()") + Key("left"),
              rdescript="VHDL: conversion to integer"),
        "converts to signed":
            R(Text("signed()") + Key("left"), rdescript="VHDL: conversion to signed"),
        "converts to unsigned":
            R(Text("unsigned()") + Key("left"), rdescript="VHDL: conversion to unsigned"),
        "converts to unsigned specific":
            R(Text("conv_unsigned(,)") + Key("left:2"),
              rdescript="VHDL: conversion to unsigned"),
        "converts to integer specific":
            R(Text("conv_integer(,)") + Key("left:2"),
              rdescript="VHDL: conversion to integer"),
    }

    extras = [
        IntegerRefST("amount", 1, 128),
        Choice("digit", {
            "(zero|zeros)": 0,
            "(one|once)": 1
        }),
        IntegerRefST("digit", 0, 2)
    ]
    defaults = {}


control.nexus().merger.add_global_rule(VHDL())
