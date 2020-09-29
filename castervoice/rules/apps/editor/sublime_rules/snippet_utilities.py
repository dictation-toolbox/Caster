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

regex = {
	
}

