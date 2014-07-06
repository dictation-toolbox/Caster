import re, os, sys
import paths

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

SETS = {}
COMMAND_PATTERN=re.compile("\s*(\"|').+(\"|'):\s*[A-Z]")

class HelpSet():
    def __init__(self):
        self.executable=""
        self.commands=[]

def extract_command_names(path):
    global SETS
    f = open(path)
    lines = f.readlines()
    f.close()
    help_set=HelpSet()
    help_set.executable=path.split("\\")[-1]
#     print "\n"+path
    for line in lines:
        if not COMMAND_PATTERN.search(line)== None:
            separator=line.strip()[0]
            command=line.split(separator)[1]
            help_set.commands.append(command)
#             print command
    if len(help_set.commands) >0:
        SETS[help_set.executable]=help_set
    

def setup_help():
    try:
        global BASE_PATH
        global SETS
        print "Rereading commands from command files..."
        SETS={}
        os.chdir(BASE_PATH)
        banned_list=["_keyCodes.py","_languagesccr.py","_myclickLocations.py","_mycommon.py"
                     "_w.py","argparse.py"]
        for files in os.listdir("."):
            filename= files.split("\\")[-1]
            if files.endswith(".py") and not filename in banned_list:
                filepath=BASE_PATH+files
                extract_command_names(filepath)
        language_path=BASE_PATH+"\\languages"
        os.chdir(language_path)
        for files in os.listdir("."):
            filepath=language_path+"\\"+files
            extract_command_names(filepath)
            
#         for help_set in SETS:
#             print help_set.executable
#             for command in help_set.commands:
#                 print command
        print "Scan Complete!"
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]

def get_help(choice):
    #To do: create a WX window here,  print to it instead of the console
    filename=str(choice)
    if filename in SETS:
        print "\n Showing help for "+ filename
        for command in SETS[filename].commands:
            print command

setup_help()