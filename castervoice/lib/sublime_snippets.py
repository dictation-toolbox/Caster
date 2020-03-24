import json
import re

from copy import deepcopy

from dragonfly import RunCommand
from dragonfly.actions.action_base  import ActionBase, ActionError

from castervoice.lib.sublime import send_sublime
from castervoice.lib.Function_like_utilities import  get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function



############################## INTERFACE WITH SUBLIME ##############################

def send_snippet(contents, **kwargs):
	kwargs['contents'] = contents
	for k in kwargs:
		if not isinstance(kwargs[k],str):
			raise TypeError("In insert_snippet value for parameter" + k  + " should be string but I received " + type(kwargs[k]))
	send_sublime("insert_snippet",kwargs)



############################## SNIPPET STATE ##############################

initial_snippet_state = {
	"snippet_text":"",
	"snippet":[],
	"snippet_parameters":{},	
	"extra_data":{},
	"stack":[],
}

snippet_state = initial_snippet_state

def snippet_log(clear_those_not_set = True,**kwargs):
	global snippet_state 
	if clear_those_not_set:
		snippet_state = initial_snippet_state
	snippet_state.update({k:v for k,v in kwargs.items() if k in snippet_state})
	



############################## ACTUALLY INSERTED SNIPPETS ##############################

def generate_snippet_text(snippet = "",data = {}):
	if isinstance(snippet,str):
		snippet_text = snippet
		extra_data = {}
	elif isinstance(snippet,list):
		if any([not isinstance(x,str) for x in snippet]):
			raise TypeError("In insert_snippet snippet must be a string or list of strings or callable!")
		n = data.get("n",1)
		snippet_text = snippet[n-1]
		extra_data = dict(n=n)
	elif callable(snippet):
		extra_data = get_only_proper_arguments(snippet, data)
		snippet_text = evaluate_function(snippet,data)
	else:
		raise TypeError("In insert_snippet snippet must be a string or list of strings or callable!")
	return snippet_text,extra_data

def insert_snippet(snippet,data={},snippet_parameters = {},additional_log = {}):
	snippet_text,extra_data = generate_snippet_text(snippet,data)
	if callable(snippet_parameters):
		snippet_parameters = evaluate_function(snippet_parameters,dict(snippet=snippet_text))
	if not isinstance(snippet_parameters,dict):
			raise TypeError("In insert_snippet snippet_parameters must be a dictionary or a callable returning a dictionary")
	send_snippet(snippet_text,**snippet_parameters)
	data_log = dict(
		snippet_parameters = snippet_parameters,
		snippet_text = snippet_text,
		snippet = snippet,
		extra_data = extra_data,
	)
	data_log.update(additional_log)
	snippet_log(**data_log)






############################## SNIPPET CLASS ##############################

class Snippet(ActionBase):
	"""docstring for Snippet"""
	def __init__(self, contents,remap_data = {},snippet_parameters = {},force_data = {}):
		super(Snippet, self).__init__()
		self.contents = contents
		self.remap_data = remap_data
		self.snippet_parameters = snippet_parameters
		self.force_data = force_data

	def retrieve_contents_from_extras_if_needed(self,contents,data):
		if isinstance(contents,str) and  "$" not in contents:
			name = re.search(r"^%\((\w+)\)s$",contents).group(1)
			if name in data:
				return data[name]
			else:
				raise ValueError(r"contents is not a snippet nor of the form %(name)s")
		else:
			return contents

	def _execute(self,data):
		contents = self.retrieve_contents_from_extras_if_needed(self.contents,data)
		data = rename_data(data,self.remap_data)
		data.update(self.force_data)
		insert_snippet(contents,data,self.snippet_parameters)

############################## SNIPPET VARIANTS ##############################

class SnippetVariant(ActionBase):
	"""docstring for Snippet"""
	def __init__(self,**remap_data):
		super(SnippetVariant, self).__init__()
		self.remap_data = remap_data
		
		
	def _execute(self,data):
		contents = snippet_state["snippet"]
		extra_data = deepcopy(snippet_state["extra_data"])
		for k,v in self.remap_data.items():
			if k in data:
				extra_data[v] = data[k]
		insert_snippet(contents,extra_data,snippet_state["snippet_parameters"])


############################## DISPLAY VARIANTS QUICK PANEL ##############################


class DisplaySnippetVariants(ActionBase):
	"""docstring for DisplaySnippetVariants"""
	def __init__(self, name = "n",values = list(range(1,6))):
		super(DisplaySnippetVariants, self).__init__()
		self.name = name
		self.values = values
	
	def _execute(self,*args,**kwargs):
		data = deepcopy(snippet_state["extra_data"])
		snippet = snippet_state["snippet"]
		alternatives = []
		protection_counter = 0
		for value in self.values:
			data[self.name] = value
			x,_ = generate_snippet_text(snippet,data)
			alternatives.append(x)
			protection_counter += 1
			if protection_counter==20:
				break

		items = [{
				"caption":json.dumps(x),
				"command":"insert_snippet",
				"args":dict(contents=x,**snippet_state["snippet_parameters"])
			} for x in alternatives]
		send_sublime("quick_panel", dict(items=items))

		

############################## SNIPPET TRANSFORMATION ##############################

def apply_single_transformation(l,t):
	if isinstance(t,tuple):
		first = t[:2]
		last = t[2:]
		args = first + (l,) + last
		print("Args",args)
		return re.sub(*args)
	elif callable(t):
		return t(l)
	 


def transform_snippet(snippet_text,transformation):
	transformation = transformation if isinstance(transformation,list) else [transformation] 
	for t in transformation:
		snippet_text = apply_single_transformation(snippet_text,t)
	return snippet_text

class SnippetTransform(ActionBase):
	"""docstring for SnippetTransform"""
	def __init__(self, transformation, steps = 0):
		super(SnippetTransform, self).__init__()
		self.transformation = transformation
		self.steps = steps

	def retrieve_transformation_from_extras_if_needed(self,transformation,data):
		if isinstance(transformation,str) and  "%" in transformation:
			name = re.search(r"^%\((\w+)\)s$",transformation).group(1)
			if name in data:
				return data[name]
			else:
				raise ValueError(r"transformation is not a snippet nor of the form %(name)s")
		else:
			return transformation


	def _execute(self,data):
		transformation = self.retrieve_transformation_from_extras_if_needed(self.transformation,data)
		s = snippet_state["snippet_text"]
		for i in range(0,self.steps):
			s = snippet_state["stack"].pop()
		snippet_new = transform_snippet(s,transformation)
		# if self.steps>0:
		snippet_state["stack"].append(s)		
		insert_snippet(snippet_new,additional_log = {k:v for k,v in snippet_state.items() if k!="snippet_text"})
	



























