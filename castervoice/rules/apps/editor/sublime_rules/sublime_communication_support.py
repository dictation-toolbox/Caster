import json
import os
import platform
import re
import subprocess

from dragonfly import RunCommand


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


def send_sublime(command,parameters = {},synchronous = True):
	"""send any sublime command with arbitrary parameters
	
	Args:
	    command (str): the name of the command to execute
	    parameters (dict, optional): the parameters to pass to the command, must be json serializable
	    synchronous (bool, optional): whether the command should be executed in a synchronous manner
	
	"""
	if  not isinstance(command,str):
		raise TypeError("command must be a string instead received ",command)
	if  not isinstance(parameters,dict):
		raise TypeError("parameters must be a dict instead received ",parameters)
	try : 
		parameters = json.dumps(parameters) 
	except :
		raise TypeError("parameters must be json serializable, received ",parameters)
	RunCommand([subl,"-b", "--command",command + " " + parameters],synchronous = synchronous).execute()

def send_snippet(contents,**kw):
	kw["contents"] = contents
	send_sublime("insert_snippet",kw)

def send_quick_panel(items):
	"""displaying a list of choices in the quick panel and executed different action depending 
	on what the user chose
	
	Args:
	    items (TYPE): an iterable of tuples representing a choice and consisting of three parts
	    	- caption (str): the text displayed to the user
	    	- command (str): the name of the command to execute, if this item is chosen
	    	- args (dict): the parameters to pass to the command, must be json serializable
	
	"""
	result = []
	for caption,command,args in items:
		if  not isinstance(caption,str):
			raise TypeError("caption must be a string instead received ",caption)
		if  not isinstance(command,str):
			raise TypeError("command must be a string instead received ",command)
		if  not isinstance(args,dict):
			raise TypeError("args must be a dict instead received ",args)
		try : 
			json.dumps(args)
		except :
			raise TypeError("args must be json serializable, received ",args)
		result.append(dict(caption=caption,command=command,args=args))
	send_sublime("quick_panel",dict(items=result))
