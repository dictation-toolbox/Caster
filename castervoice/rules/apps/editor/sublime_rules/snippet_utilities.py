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

def regular(varname,regex,format_string,option  = ""):
	"""Utility for generating snippet code for regular expression substitution.Produces

	${var_name/regex/format_string/options} or
	${var_name/regex/format_string}

	all arguments must be able to get casted into str()

	Args:
	    varname (str): The variable name for example 1,2
	    regex (str): Perl style regular expression
	    format_string (str): Perl style format string
	    option (str, optional): optional can take one of the following values
	    	- "i" : case insensitive
	    	- "g" : replace all appearances
	    	- "m" : do not ignore new lines

	
	Returns: str
	"""
	arg = (varname,regex,format_string) + ((option,) if option else ())
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
	mapping,l = {},[]
	for k,v in snippets.items():
		if isinstance(v,str):
			mapping[k] = R(Snippet(v))
		elif isinstance(v,list):
			mapping[k + " <n>"] = R(Snippet(v)); l.append(len(v))
		elif callable(v):
			mapping[k] = R(Snippet(v))
		# elif isinstance(v,dict) and all(isinstance(x,str) for x in v):
			
		else:
			raise TypeError("")
	def decorator(c):
		c.mapping.update(mapping)
		c.extras.extend(extras)
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

