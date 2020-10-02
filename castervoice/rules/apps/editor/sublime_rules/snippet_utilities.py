import re

from dragonfly import Choice

from castervoice.rules.apps.editor.sublime_rules.Function_like_utilities import  get_signature_arguments
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.additions import IntegerRefST

try : 
	from sublime_rules.sublime_snippets import Snippet
except :
    from castervoice.rules.apps.editor.sublime_rules.sublime_snippets import Snippet

def placeholder(field,default  = ""):
	"""Utility to generate snippet code for placeholders fields at runtime

	placeholder(1) = $1
	placeholder(1,"data") = ${1:data}
	placeholder((1,2),"data")  = ${1:${2:data}}
	placeholder((1,"INTERESTING"),"data")  = ${1:${INTERESTING:data}}
	
	Args:
	    field (Union[convertible to string,Tuple[convertible to string]]): field index
	    default (str, optional): default value
	
	Returns:
	    str: raw placeholder text
	"""
	if isinstance(field,tuple):
		tail = field[1:] if len(field) > 2 else field[1]
		return "${" + str(field[0]) + ":" + placeholder(tail,default)  + "}"
	else:
		if not default:
			return "$" + str(field)
		else:
			return "${" + str(field) + ":" + str(default)  + "}"

def regular(varname,regex,format_string,options  = "",ignore_case=False,replace_all=False,ignore_new_lines=True):
	"""Utility for generating snippet code for regular expression substitution.Produces

	${var_name/regex/format_string/options} or
	${var_name/regex/format_string}

	all arguments must be able to get casted into str()

	Args:
	    varname (str): The variable name for example 1,2
	    regex (str): Perl style regular expression
	    format_string (str): Perl style format string
	    options (str, optional): optional can take a combination of the following values
	    	- "i" : case insensitive
	    	- "g" : replace all appearances
	    	- "m" : do not ignore new lines
		ignore_case(bool): set True for a case insensitive regular expression(equivalent to options="i")
		replace_all(bool): set True for replacing all occurrences of regular expression(equivalent to options="g")
		ignore_new_lines(bool): set False to not ignore new lines in regular expression(equivalent to options="m")
	
	Returns: str
	"""
	if ignore_case  and "i" not in options:
		options = options + "i"
	if replace_all and "g" not in options:
		options = options + "g"
	if  not ignore_new_lines and "m" not in options:
		options = options + "m"
	arg = (varname,regex,format_string) + ((options,) if options else ())
	return "${" + "/".join(map(str, arg)) + "}"

def load_snippets(snippets,extras = [], defaults = {}):
	"""Utility in order to decorate grammars to quickly load snippets from a raw dictionary format
	
	Args:
	    snippets (TYPE): Description
	    extras (list, optional): Description
	    defaults (dict, optional): Description
	
	Returns:
	    TYPE: Description
	
	Raises:
	    TypeError: Description
	"""
	mapping,l,additional_extras = {},[],[]
	for k,v in snippets.items():
		if  not isinstance(k,str):
			raise  TypeError("snippet keys must be strings, instead received",k)
		if isinstance(v,str):
			mapping[k] = R(Snippet(v))
		elif isinstance(v,list):
			mapping[k + " <n>"] = R(Snippet(v)); l.append(len(v))
		elif callable(v):
			names,_ = get_signature_arguments(v)
			if "n" in names:
				l.append(10)
			mapping[k] = R(Snippet(v))
		elif isinstance(v,dict):
			if any( not isinstance(x,str) or not isinstance(y,str) for x,y in v.items()):
				raise  TypeError("the dictionary should be consisting only of strings, instead received",v)
			extra_names = {x.group(1) for x in re.finditer(r"<(.+)>",k)}
			assert len(extra_names) == 1,"when the value is a dictionary, must only contain one extra, instead received " + str(len(extra_names))
			name = list(extra_names)[0]
			additional_extras.append(Choice(name,v))
			mapping[k] = R(Snippet(lambda _snippet_internal:_snippet_internal,remap_data = {name:"_snippet_internal"}))
			# mapping[k] = R(Snippet('%({0})s'.format(name)))
		else:
			raise TypeError("")

	def decorator(c):
		c.mapping.update(mapping)
		c.extras.extend(extras + additional_extras)
		c.defaults.update(defaults)
		if l:
			e = next((x for x in c.extras if isinstance(x,IntegerRefST)),None)
			if e:
				c.extras.append(IntegerRefST("n",1,max([e._rule._element._max,max(l)])))
			else:
				c.extras.append(IntegerRefST("n",1,max(l)))

		return c
	return decorator


regex = {
	
}

