import json
import os
import platform
import re
import subprocess


from copy import deepcopy

from dragonfly import RunCommand
from dragonfly.actions.action_base  import ActionBase, ActionError

from castervoice.rules.apps.editor.sublime_rules.Function_like_utilities import  get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function

########################################################################################################################
# General purpose sublime stuff, can be used regardless of snippets
########################################################################################################################

############################## BASIC INTERFACE WITH SUBLIME ##############################


def validate_subl():
    if platform.system() != 'Windows':
        return "subl"
    try:
        subprocess.check_call(["subl", "-h"],stdout=subprocess.PIPE,stderr=subprocess.PIPE) # For testing purposes you can invalidate to trigger failure
        return "subl"
    except Exception as e:
        try : 
            subprocess.check_call(["C:\\Program Files\\Sublime Text 3\\subl", "-h"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            print("Resorting to C:\\Program Files\\Sublime Text 3\\subl.exe")
            return  "C:\\Program Files\\Sublime Text 3\\subl"
        except :
            print("Sublime Text 3 `subl` executable was not in the Windows path")
            if not os.path.isdir(r'C:\\Program Files\\Sublime Text 3'):
                print("And there is no C:\\Program Files\\Sublime Text 3 directory to fall back to!")
            else:
                print("And it was not found under C:\\Program Files\\Sublime Text 3")
            print("Please add `subl` to the path manually")
            return "subl"

subl = validate_subl()


def send_sublime(c,data):
    RunCommand([subl,"-b", "--command",c + " " + json.dumps(data)],synchronous = True).execute()

############################## SUBLIME COMMAND ACTION ##############################

class SublimeCommand(RunCommand):
	"""docstring for SublimeCommand"""
	def __init__(self, command,data = {}):
		super(SublimeCommand, self).__init__([subl, "-b","--command",command + " " + json.dumps(data)],synchronous = True)
	


########################################################################################################################
# Actual snippet stuff, contains functions to send snippets, generate snippet text and dragonfly actions wrappers
########################################################################################################################

############################## LOW LEVEL SNIPPET INTERFACE WITH SUBLIME ##############################

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
	"remap_data":{},
}
try : 
	snippet_state
except :
	snippet_state = initial_snippet_state

def snippet_log(clear_those_not_set = True,**kwargs):
	global snippet_state 
	if clear_those_not_set:
		snippet_state = initial_snippet_state
		# snippet_state.update(initial_snippet_state)
		# snippet_state = initial_snippet_state.copy()
	snippet_state.update({k:v for k,v in kwargs.items() if k in snippet_state})
# 	print(snippet_state is initial_snippet_state)
	



############################## GENERATING AND HIGH-LEVEL INSERTING SNIPPETS ##############################

def filter_snippet_text(snippet_text):
	'''
	Filter out numerical placeholders that have their_default value in two locations
	For example:
		${1:data} = ${1:data} + $2
	will not be accepted by sublime!
	Precondition for these to work is that those default values are the same!
	'''
	def clean(text):
		temporary,skip,l = [],0,len(text)
		for i,(c,n) in enumerate(zip(text, text[1:])):
			if skip and i!=l-2:
				skip = skip - 1
				continue
			elif not skip and c=="\\" and n in ["\\","$","{","}"]:
				temporary += [" "," "]
				skip = 1
			elif i==l-2:
				if not skip: temporary.append(c)
				temporary.append(n)
			else:
				temporary.append(c)
		return "".join(temporary)

	def bracket_match(text):
		temporary,l,mapping = [],len(text),{}
		for i,c in enumerate(text):
			if c=="{" and i!=0 and text[i-1]=="$":
				temporary.append(i)
			elif c=="}":
				if temporary:
					m = len(temporary)
					mapping[temporary.pop()] = (i,m)
		return mapping





	def find_duplicates(text,mapping):
		temporary={}
		pattern = re.compile(r"\$\{(\d+):")
		l = pattern.finditer(text)
		for m in l:
			number = m.group(1)
			beginning = m.start(0) + 1
			ending,depth = mapping[beginning]
			try :
				temporary[number].append((beginning,ending,depth)) 
			except :
				temporary[number] = [(beginning,ending,depth)]
		return {k:v for k,v in temporary.items() if len(v)!=1} 



	def eliminate_duplicates(original,duplicates):
		temporary = list(original)
		print(original,duplicates)
		c = [(d,k,b,e) for k,v in duplicates.items() for b,e,d in v[1:]];c = sorted(c,reverse=True)
		# for k,v in duplicates.items():
		if True:
			for d,k,b,e in c:
				for i in range(b,e+1):
					temporary[i] = ""
				for i,letter in enumerate(k):
					temporary[b+i] = letter
		return "".join(temporary)

	text_after_escaping = clean(snippet_text)
	bracket_mapping = bracket_match(text_after_escaping)
	duplicates = find_duplicates(text_after_escaping,bracket_mapping)
	return eliminate_duplicates(snippet_text,duplicates)


def generate_snippet_text(snippet = "",data = {}):
	if isinstance(snippet,str):
		snippet_text = snippet
		extra_data = {}
	elif isinstance(snippet,list):
		if any(not isinstance(x,str) for x in snippet):
			raise TypeError("In generate_snippet_text snippet must be a string or list of strings or callable!Received ",type(snippet))
		n = data.get("n",1)
		snippet_text = snippet[n-1]
		extra_data = dict(n=n)
	elif callable(snippet):
		extra_data = get_only_proper_arguments(snippet, data)
		snippet_text = evaluate_function(snippet,data)
	else:
		raise TypeError("In generate_snippet_text snippet must be a string or list of strings or callable!Received ",type(snippet))
	# snippet_text = filter_snippet_text(snippet_text)
	return snippet_text,extra_data

def insert_snippet(snippet,data={},snippet_parameters = {},additional_log = {}):
	"""Summary
	
	Args:
	    snippet (Union[str,List[str],Callable[...,str]]): Description
	    data (dict, optional): Description
	    snippet_parameters (dict, optional): Description
	    additional_log (dict, optional): Description
	
	Raises:
	    TypeError: Description
	"""
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
	"""docstring for Snippet
	
	Attributes:
	    contents (Union[str,List[str],Callable[...,str]]): 
	    	The snippet to be inserted.It can be one of the following:
	    	- a raw string containing the snippet text
	    	- a list of strings, containing variations of the same snippet
	    	- a callable that will generate the snippet, optionally using the spoken data
	    remap_data (Dict[str,str]): 
	    	a dictionary containing entries of the form (old_name,new_name)
	    	enabling you to rename extras before they are passed to the snippet generation
	    	For instance, suppose you have a snippet
	    		lambda world: "$1 = " + world + " $2 " + world
	    	normally the world parameter should come from an extra named `world`.
	    	you can use
	    		remap_data ={"other_name":"world"}
	    force_data (TYPE): Description
	    snippet_parameters (TYPE): Description
	"""
	def __init__(self, contents,remap_data = {},snippet_parameters = {},force_data = {}):
		"""Summary
		
		Args:
		    contents (TYPE): Description
		    remap_data (dict, optional): Description
		    snippet_parameters (dict, optional): Description
		    force_data (dict, optional): Description
		"""
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
		send_sublime("quick_panel", dict(items=items))


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
	



########################################################################################################################
# decorator and backend needed for the self modifying snippet variants
########################################################################################################################




grammars_with_snippets = {}

def mark_as_snippet_grammar(*rule,**rename):
	def function(rule):
		grammars_with_snippets[rule] = {"extras":rule.extras,"defaults":rule.defaults,"rename":rename}
		return rule
	if len(rule)==1 and isinstance(rule[0],type):
		return function(rule[0])
	elif len(rule)==0: 
		return function
	else:
		raise ValueError("mark_as_snippet_grammar is not used correctly!")
	return function

























