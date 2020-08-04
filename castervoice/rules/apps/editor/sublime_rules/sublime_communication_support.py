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


def send_sublime(c,data):
    RunCommand([subl,"-b", "--command",c + " " + json.dumps(data)],synchronous = True).execute()
