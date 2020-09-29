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


