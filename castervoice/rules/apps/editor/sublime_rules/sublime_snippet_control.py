import json

from copy import deepcopy

from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

try:
    from sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,send_sublime,SublimeCommand
except ImportError:
    from castervoice.rules.apps.editor.sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,send_sublime,SublimeCommand




# 
# global controll grammar WIP
#
class SublimeSnippetControllRule(MappingRule):
    pronunciation = "sublime snippet control"
    mapping = {
    	# "variant <n>":
    	# 	R(Key("c-z") + SnippetVariant(n="n")),
    	# "display variants":
    	# 	R(Key("c-z") + DisplaySnippetVariants()),

    	# "next field":R(SublimeCommand("next_field")),
    	# I often use the following to avoid problems
    	# with tabs and auto complete, but inside a CCR
    	# "okay [<n>]":
            # R(Key("left,right,tab"))*Repeat(extra="n"), 

    	# "previous field":R(SublimeCommand("prev_field")),
    }
    extras = [
        IntegerRefST("n",1,10),
    ]
    defaults = {"n":1}




#---------------------------------------------------------------------------


# def get_rule():
    # return SublimeSnippetControllRule, RuleDetails(name="sublime snippet control", executable=["sublime_text"])
    
