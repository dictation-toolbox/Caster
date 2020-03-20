import json
import re

from dragonfly import RunCommand





############################## INTERFACE WITH SUBLIME ##############################

def send_sublime(command,data):
    RunCommand(["subl", "-b","--command",command + " " + json.dumps(data)],synchronous = True).execute()

############################## SUBLIME COMMAND ACTION ##############################



class SublimeCommand(RunCommand):
	"""docstring for SublimeCommand"""
	def __init__(self, command,data = {}):
		super(SublimeCommand, self).__init__(["subl", "-b","--command",command + " " + json.dumps(data)],synchronous = True)
	




















