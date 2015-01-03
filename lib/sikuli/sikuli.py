import os

from dragonfly import (Grammar, MappingRule, Function)

from lib import settings
from lib.dragonfree import launch


grammar = None



def refresh_sikuli():
    unload()
    
    # rebuild from filenames
    mapping = {}
    
    natlink_available = False
    try:
        import natlink
        natlink_available = True
    except ImportError:
        # just do regular expression checking
        pass
    default_number = 0
    for f in os.listdir(settings.SETTINGS["paths"]["SIKULI_SCRIPTS_PATH"]):
        if f.endswith(".sikuli"):
            print f
            words = f.split(".")[0].split("_")
            # check to make sure the command is made of proper words
            can_be_pronounced = True
            for word in words:
                if natlink_available:
                    if natlink.getWordInfo(word, 7) == None:
                        can_be_pronounced = False
                        break
                else:
                    if word.isalpha() == False:
                        can_be_pronounced = False
                        break
            # PATH-TO-SIKULIsikuli-ide.exe -r xxxx.sikuli 
            if can_be_pronounced:
                mapping[" ".join(words)] = Function(launch.run, arguments=[settings.SETTINGS["SIKULI_IDE_PATH"], "-r", f])
          
#     grammar = Grammar("sikuli")
#     grammar.add_rule(MappingRule())
#     grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
