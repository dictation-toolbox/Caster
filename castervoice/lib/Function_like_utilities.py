import inspect

import six

############################## UTILITIES TO WRAP FUNCTION CALLS ##############################
#
# these functions are based on the dragonfly implementation for Function action, which does not
# support returning the return value of the function called
#
##############################################################################################


def get_signature_arguments(function):
	if six.PY2:
		# pylint: disable=deprecated-method
		argspec = inspect.getargspec(function)
	else:
		argspec = inspect.getfullargspec(function)
	args, varkw = argspec[0], argspec[2]
	filter_keywords = not varkw
	valid_keywords = set(args)
	return valid_keywords, filter_keywords


def get_only_proper_arguments(function,data):
	valid_keywords, filter_keywords = get_signature_arguments(function)
	arguments = data.copy()
	if filter_keywords:
		invalid_keywords = set(arguments.keys()) - valid_keywords
		for key in invalid_keywords:
			del arguments[key]
	return arguments

def rename_data(data,remap_data):
	if isinstance(data, dict):
		renamed = data.copy()
	else:
		raise TypeError("evaluate_function received instead of a dictionary " + type(data) + " in data")

	# Remap specified names.
	for old_name, new_name in remap_data.items():
		if old_name in data:
			renamed[new_name] = renamed.pop(old_name)
	return renamed
	

def evaluate_function(function,data = {},remap_data = {}):
	renamed = rename_data(data,remap_data)
	arguments = get_only_proper_arguments(function,renamed)
	try:
		return function(**arguments)
	except Exception as e:
		raise


