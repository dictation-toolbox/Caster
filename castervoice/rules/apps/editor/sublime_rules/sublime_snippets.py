import json
import re



from copy import deepcopy

from dragonfly import RunCommand
from dragonfly.actions.action_base  import ActionBase, ActionError

from castervoice.rules.apps.editor.sublime_rules.Function_like_utilities import  (
	get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function
)
from castervoice.rules.apps.editor.sublime_rules.sublime_communication_support import  (
	send_sublime,send_snippet,send_quick_panel
)
from castervoice.rules.apps.editor.sublime_rules.snippet_generation_support import  (
	generate_snippet_text,insert_snippet,snippet_state,apply_single_transformation,transform_snippet
)



############################## SUBLIME COMMAND ACTION ##############################

class SublimeCommand(ActionBase):
	"""docstring for SublimeCommand"""
	def __init__(self, command,parameters = {}):
		super(SublimeCommand, self).__init__()
		if not isinstance(parameters,dict) and not callable(parameters):
			raise TypeError("In SublimeCommand parameters must be a dict or a callable")
		if not isinstance(command,str):
			raise TypeError("In SublimeCommand command must be a string")
		self.parameters = parameters
		self.command = command

	def _execute(self,data):
		try :
			command =  self.command % data 
		except :
			command =  self.command
		if isinstance(self.parameters,dict):
			p = self.parameters
		else:
			p = evaluate_function(self.parameters,data)
		send_sublime(command,p)
	


############################## SNIPPET CLASS ##############################

class Snippet(ActionBase):
	"""docstring for Snippet
	
	Attributes:
	    contents (Union[str,List[str],Callable[...,str]]): 
	    	The snippet to be inserted.It can be one of the following:
	    	- a raw string containing the snippet text
	    	- a list of strings, containing variations of the same snippet
	    	- a callable that will generate the snippet, optionally using the spoken data
	    	As a fourth option you can specify that you want to obtain the snippet contents
	    	(which can be in any of the above three forms) from an extra. As an example
	    		"snippet <something>":R(Snippet("%(something)s"))
	    	where
	    		Choice("something",{"hello":"Hello $1,My name is $2","there":"$1= there($1)"})
	    remap_data (Dict[str,str]): 
	    	a dictionary containing entries of the form (old_name,new_name)
	    	enabling you to rename extras before they are passed to the snippet generation
	    	For instance, suppose you have a snippet
	    		lambda world: "$1 = " + world + " $2 " + world
	    	normally the world parameter should come from an extra named `world`.
	    	However, suppose you want `world` to come from an extra named `other_name`
	    	Then in a manner similar to `Function` you can use
	    		remap_data ={"other_name":"world"}
	    snippet_parameters (Union[Dict,Callable[...,str]]):
	    	Parameters to pass along with a snippet. Can be either
	    	- a hardcoded dictionary contain the parameters
	    	- a callable that processes the extras spoken and returns the dictionary
	    	In the latter case, the semantics are like `Function`.
	"""
	def __init__(self, contents,remap_data = {},snippet_parameters = {}):
		super(Snippet, self).__init__()
		self.contents = contents
		self.remap_data = remap_data
		self.snippet_parameters = snippet_parameters

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
		insert_snippet(contents,data,self.snippet_parameters,additional_log = {"remap_data":self.remap_data})

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
		insert_snippet(contents,extra_data,snippet_state["snippet_parameters"],additional_log = {"remap_data":snippet_state["remap_data"]})


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
			try :
				data[self.name] = value
				x,_ = generate_snippet_text(snippet,data)
				alternatives.append(x)
				protection_counter += 1
				if protection_counter==20:
					break
			except:
				break

		items = [{
				"caption":json.dumps(x),
				"command":"insert_snippet",
				"args":dict(contents=x,**snippet_state["snippet_parameters"])
			} for x in alternatives]
		# send_sublime("quick_panel", dict(items=items))
		send_quick_panel(
			(json.dumps(x),"insert_snippet",dict(contents=x,**snippet_state["snippet_parameters"])) 
			for x in alternatives
		)


class DisplayMultipleSnippetVariants(ActionBase):
	"""docstring for DisplaySnippetVariants"""
	def __init__(self,values):
		super(DisplayMultipleSnippetVariants, self).__init__()
		self.values = values
	
	def _execute(self,*args,**kwargs):
		snippet = snippet_state["snippet"]
		alternatives = []
		protection_counter = 0
		for name,value in self.values.items():
			try :
				data = deepcopy(snippet_state["extra_data"])
				data[name] = value
				x,_ = generate_snippet_text(snippet,data)
				alternatives.append(x)
				protection_counter += 1
				if protection_counter==20:
					break
			except:
				break

		items = [{
				"caption":json.dumps(x),
				"command":"insert_snippet",
				"args":dict(contents=x,**snippet_state["snippet_parameters"])
			} for x in alternatives]
		send_sublime("quick_panel", dict(items=items))

		

############################## SNIPPET TRANSFORMATION ##############################

class SnippetTransform(ActionBase):
	"""Apply a transformation to the previous inserted snippet
	
	Attributes:
	    transformation (
	    		Union[str,Transformation,List[Transformation]] where
	    		Transformation = Union[Tuple,Callable[str,str]]
	    	): 
	    	the transformation to be applied to the last inserted snippet.One of
	    	- callable, that accepts a single parameter the snippet text and 
	    	  returns the final text
	    	- a tuple that describes a regular expression and  contains the arguments
	    	  you would pass to `re.sub` function ( excluding that snippet text of course)

	    	You can also pass at least

	    steps (int): Description
	"""
	def __init__(self, transformation, steps = 0):
		super(SnippetTransform, self).__init__()
		self.transformation = transformation
		self.steps = steps
		if  not isinstance(transformation,str):
			self.verify_transformation(transformation)

	def retrieve_transformation_from_extras_if_needed(self,data,transformation):
		if isinstance(transformation,str):
			temporary = []
			for m in re.finditer(r"%\((\w+)\)s",transformation):
				name = m.group(1)
				if name in data:
					t = data[name]
					if isinstance(t,list):
						temporary.extend(t)
					else:
						temporary.append(t)
				else:
					raise ValueError(r"transformation is not a snippet nor of the form %(name)s")
			if not temporary:
				raise ValueError("Empty transformation extracted from extra no %(name)s found :",transformation)
			return temporary
		else:
			return transformation

	def verify_transformation(self, transformation):
		if  not isinstance(transformation,(tuple,list)) and not callable(transformation):
			raise TypeError("transformation must be a tuple or callable or a list thereof, instead received",transformation)
		if isinstance(transformation,list):
			if any(x for x in transformation if  not isinstance(x,tuple) and  not callable(x)):
				raise TypeError("transformation must be a tuple or callable or a list thereof, instead received",transformation)


	def _execute(self,data):
		transformation = self.retrieve_transformation_from_extras_if_needed(data,self.transformation)
		self.verify_transformation(transformation)
		s = snippet_state["snippet_text"]
		for i in range(0,self.steps):
			s = snippet_state["stack"].pop()
		# by now s holds snippet we want to transform
		# and this stack no longer contains it!
		snippet_new = transform_snippet(s,transformation)
		snippet_state["stack"].append(s) # push s onto the stack
		insert_snippet(snippet_new,additional_log = {k:v for k,v in snippet_state.items() if k!="snippet_text"})
	





















