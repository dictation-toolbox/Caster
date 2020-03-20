import json

from copy import deepcopy

from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from castervoice.lib.sublime import send_sublime,SublimeCommand
from castervoice.lib.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants




# 
# global controll grammar WIP
#
class SublimeSnippetControllRule(MappingRule):
    pronunciation = "sublime snippet control"
    mapping = {
    	"variant <n>":
    		R(Key("c-z") + SnippetVariant(n="n")),
    	"display variants":
    		R(Key("c-z") + DisplaySnippetVariants()),

    	# "next field":R(SublimeCommand("next_field")),
    	# "previous field":R(SublimeCommand("prev_field")),
    }
    extras = [
        IntegerRefST("n",1,10),
    ]
    defaults = {"n":1}




#---------------------------------------------------------------------------


def get_rule():
    return SublimeSnippetControllRule, RuleDetails(name="sublime snippet control", executable=["sublime_text"])
    
