import re

from castervoice.rules.apps.editor.sublime_rules.Function_like_utilities import  get_signature_arguments,get_only_proper_arguments,rename_data,evaluate_function
from castervoice.rules.apps.editor.sublime_rules.sublime_communication_support import  send_sublime,send_snippet,send_quick_panel


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
	snippet_state = initial_snippet_state.copy()

def snippet_log(clear_those_not_set = True,**kwargs):
	global snippet_state 
	if clear_those_not_set:
		snippet_state.update(initial_snippet_state)
	snippet_state.update({k:v for k,v in kwargs.items() if k in snippet_state})

	







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