'''
Created on 18 Mar 2018

@author: gerrish
'''
from castervoice.lib.imports import *
from vhdl_strings import *

def binary_string(digit, amount):
    return Text(str(digit)*amount).execute()

class VHDLnon(MappingRule):
    mapping = {
        "entity":
            R(entity_string),
        "Architecture":
            R(architecture_string),
        "component":
            R(component_string),
        "component declaration":
            R(component_declaration_string),
        SymbolSpecs.SWITCH:
            R(case_string),
        SymbolSpecs.CASE:
            R(Text("case TOKEN is")),
        "process":
            R(process_string),
        "generate components":
            R(for_generate_string),
        "conditional component":
            R(if_generate_string),
    }


class VHDL(MergeRule):

    pronunciation = "VHDL"
    non = VHDLnon

    mapping = {
        SymbolSpecs.COMMENT:
            R(Text("--")),
        SymbolSpecs.IF:
            R(Text("if () then ") + Key("enter,enter") + Text("end if;") +
              Key("home,up,up")),
        SymbolSpecs.ELSE:
            R(Key("e,l,s,e,enter")),
        "alternate":
            R(Key("e,l,s,i, f,space,T,O,K,E,N,space,t,h,e,n,enter,tab")),
        SymbolSpecs.CASE:
            R(Text("case TOKEN is") + Key("enter,tab")),
        "when":
            R(Text("when ")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for  in to loop") + Key("left:12")),
        "generate":
            R(Text("GENERATE")),
        "Input":
            R(Text("in")),
        "Output":
            R(Text("out")),
        "Standard Logic":
            R(Text("std_logic")),
        "Standard Logic Vector":
            R(Text("std_logic_vector")),
        "Constant":
            R(Text("constant : ") + Key("left,left")),
        "Signal":
            R(Text("signal : ") + Key("left,left")),
        "integer":
            R(Text("integer TOKEN to TOKEN")),
        "type":
            R(Text("type :") + Key("left")),
        # Operators
        "Not Equal":
            R(Text("/=")),
        SymbolSpecs.NOT:
            R(Text("not")),
        SymbolSpecs.OR:
            R(Text("or")),
        "not and":
            R(Text("nand")),
        "XOR":
            R(Text("xor")),
        "X NOR":
            R(Text("xnor")),
        "Assignment":
            R(Text(" <= ") + Key("left")),
        "Association":
            R(Text(' => ') + Key("left")),
        "Concatenate":
            R(Text(" & ")),
        "Down To":
            R(Text("downto")),
        "Up To":
            R(Text("upto")),
        "Input":
            R(Text("in")),
        "Output":
            R(Text("out")),
        "Standard Logic":
            R(Text("std_logic")),
        "Standard Logic Vector":
            R(Text("std_logic_vector")),
        "Constant":
            R(Text("constant : ") + Key("left,left")),
        "Signal":
            R(Text("signal : ") + Key("left,left")),
        "integer":
            R(Text("integer TOKEN to TOKEN")),
        "type":
            R(Text("type :") + Key("left")),
        # Operators
        "Not Equal":
            R(Text("/=")),
        SymbolSpecs.NOT:
            R(Text("not")),
        SymbolSpecs.OR:
            R(Text("or")),
        "not and":
            R(Text("nand")),
        "XOR":
            R(Text("xor")),
        "X NOR":
            R(Text("xnor")),
        "Assignment":
            R(Text(" <= ") + Key("left")),
        "Association":
            R(Text(' => ') + Key("left")),
        "Concatenate":
            R(Text(" & ")),
        "Down To":
            R(Text("downto")),
        "Up To":
            R(Text("upto")),
        SymbolSpecs.COMMENT:
            R(Text("-- ")),
        "binary [<amount>] <digit>":
            R(Function(binary_string)),

        #VHDL specific
        "length":
            R(Text("length'")),
        SymbolSpecs.TO_INTEGER:
            R(Text("to_integer()") + Key("left")),
        "converts to signed":
            R(Text("signed()") + Key("left")),
        "converts to unsigned":
            R(Text("unsigned()") + Key("left")),
        "converts to unsigned specific":
            R(Text("conv_unsigned(,)") + Key("left:2")),
        "converts to integer specific":
            R(Text("conv_integer(,)") + Key("left:2")),
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

control.global_rule(VHDL())
