import re, os, sys
import paths

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

SETS = []

class HelpSet():
    def __init__(self):
        self.executable=""
        self.commands=[]

def setup_help():
    try:
        global BASE_PATH
        global SETS
        os.chdir(BASE_PATH)
        pattern=re.compile("\s*(\"|').+(\"|'):\s*[A-Z]")
#         import pydevd;pydevd.settrace()
        for files in os.listdir("."):
            if files.endswith(".py"):
                has_command_map= False
                lines=[]
                filepath=BASE_PATH+files
                f = open(filepath)
                lines = f.readlines()
                f.close()
                help_set=HelpSet()
                help_set.executable=filepath
                print "\n"+filepath
                for line in lines:
                    if not pattern.search(line)== None:
                        separator=line.strip()[0]
                        command=line.split(separator)[1]
                        help_set.commands.append(command)
                        print command
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
                        