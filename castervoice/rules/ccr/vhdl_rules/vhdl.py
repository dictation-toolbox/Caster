'''
Created on 18 Mar 2018

@author: gerrish
'''
from dragonfly import Function, Choice, ShortIntegerRef

from castervoice.lib.actions import Key, Text
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

try:  # Try  first loading  from caster user directory
    from vhdl_support import for_generate_string, if_generate_string, process_string, \
        case_string, component_declaration_string, component_string, architecture_string, entity_string
except ImportError:
    from castervoice.rules.ccr.vhdl_rules.vhdl_support import for_generate_string, if_generate_string, process_string, \
        case_string, component_declaration_string, component_string, architecture_string, entity_string

def binary_string(digit, amount):
    return Text(str(digit)*amount).execute()



class VHDL(MergeRule):

    pronunciation = "VHDL"

    mapping = {
        SymbolSpecs.COMMENT:
            R(Text("-- ")),
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
        ShortIntegerRef("amount", 1, 128),
        Choice("digit", {
            "(zero|zeros)": 0,
            "(one|once)": 1
        }),
        ShortIntegerRef("digit", 0, 2)
    ]
    defaults = {}


def get_rule():
    return VHDL, RuleDetails(ccrtype=CCRType.GLOBAL)
