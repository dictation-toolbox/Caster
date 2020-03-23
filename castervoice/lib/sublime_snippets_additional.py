import json
import re

from copy import deepcopy

from dragonfly import RunCommand
from dragonfly.actions.action_base  import ActionBase, ActionError
from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)

from castervoice.lib.sublime import send_sublime
from castervoice.lib.Function_like_utilities import  get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function


grammars_with_snippets = {}

def mark_snippets(*args):
	names = set(args)
	def function(x):
		data = {}
		for y in x.extras:
			if isinstance(y,Choice) and y.name in names:
				data[y.name] = y
		grammars_with_snippets[x] = data
		return x
	return function










