import json
import re

from copy import deepcopy

from dragonfly import RunCommand
from dragonfly.actions.action_base  import ActionBase, ActionError
from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)

from castervoice.lib.sublime import send_sublime
from castervoice.lib.Function_like_utilities import  get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function


grammars_with_snippets = {}

def mark_as_snippet_grammar(rule):
	grammars_with_snippets[rule] = rule.extras
	return rule







