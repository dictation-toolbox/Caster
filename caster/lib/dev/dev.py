'''

This file is for experimentation. Everything in here should be considered
unstable and not ready for production.






'''

from subprocess import Popen
import time

from dragonfly import (Function, Key, BringApp, Text, WaitWindow, Dictation, Choice, Grammar, MappingRule, Paste)

from caster.lib import utilities, settings, context, control
from caster.lib.dev import devgen
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.communication import Communicator
from caster.lib.dfplus.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from caster.lib.dfplus.state.actions2 import ConfirmAction, BoxAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.tests.complexity import run_tests


grammar = Grammar('development')


# from Tkinter import * 
# from tkColorChooser import askcolor 
def experiment(text):
    '''this function is for tests'''
    comm = Communicator()
    comm.get_com("status").error(0)

def get_color():
    '''do asynchronously'''
#     print(askcolor())

LAST_TIME=0
def print_time():
    global LAST_TIME
    print(time.time()-LAST_TIME)
    LAST_TIME=time.time()

COUNT=5
def countdown():
    global COUNT
    print(COUNT)
    COUNT-=1
    return COUNT==0

def grep_this(path, filetype):
    c = None
    tries=0
    while c==None:
        tries+=1
        results = context.read_selected_without_altering_clipboard()
        error_code = results[0]
        if error_code==0:
            c = results[1]
            break
        if tries>5:
            return False
    grep="D:/PROGRAMS/NON_install/AstroGrep/AstroGrep.exe"
    Popen([grep, "/spath=\""+str(path) +"\"", "/stypes=\""+str(filetype)+"\"", "/stext=\""+str(c)+"\"", "/s"])


def close_last_spoken(spoken):
    first = spoken[0]
    Text("</"+first+">").execute()
def close_last_rspec(rspec):
    Text("</"+rspec+">").execute()
    
def bring_test():
    print(settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\"))
    try:
        BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"]).execute()
    except Exception:
        utilities.simple_log()
        

class StackTest(MappingRule):
    '''test battery for the ContextStack'''
    mapping = {
        "close last tag":               ContextSeeker([L(S(["cancel"], None),
                                                         S(["html spoken"], close_last_spoken, use_spoken=True), 
                                                         S(["span", "div"], close_last_rspec, use_rspec=True))
                                                       ]),
        "html":                         R(Text("<html>"), rspec="html spoken"), 
        "divider":                      R(Text("<div>"), rspec="div"),
        "span":                         R(Text("<span>"), rspec="span"),
        "backward seeker [<text>]":     ContextSeeker([L(S(["ashes"], Text("ashes1 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery1 [%(text)s] "))), 
                                                       L(S(["ashes"], Text("ashes2 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery2 [%(text)s] ")))
                                                       ]), 
        "forward seeker [<text>]":      ContextSeeker(forward=
                                                      [L(S(["ashes"], Text("ashes1 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery1 [%(text)s] "))), 
                                                       L(S(["ashes"], Text("ashes2 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery2 [%(text)s] ")))
                                                       ]),
        "never-ending":                 AsynchronousAction([L(S(["ashes", "charcoal"], print_time, None),
                                                          S(["bravery"], Text, "bravery1"))
                                                       ], time_in_seconds=0.2, repetitions=20, 
                                                           finisher=Text("finisher successful")),
        "ashes":                        RegisteredAction(Text("ashes fall "), rspec="ashes"),
        "bravery":                      RegisteredAction(Text("bravery is weak "), rspec="bravery"),
        "charcoal boy <text> [<n>]":    R(Text("charcoal is dirty %(text)s"), rspec="charcoal"),
                                
        "test confirm action":          ConfirmAction(Key("a"), rdescript="Confirm Action Test"),
        
        "test box action":              BoxAction(lambda data: None, rdescript="Test Box Action", box_type=settings.QTYPE_DEFAULT, 
                                                  log_failure=True),
    }
    extras = [
              Dictation("text"),
              IntegerRefST("n", 1, 5)
             ]
    defaults = {"text": ""}

class DevelopmentHelp(MappingRule):
    mapping = {
        # caster development tools
        "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),
        "open natlink folder":          R(BringApp("C:/Windows/explorer.exe", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")), rdescript="Open Natlink Folder"),
        "refresh debug file":           Function(devgen.refresh),  
        "Agrippa <filetype> <path>":    Function(grep_this),
        "run rule complexity test":     Function(lambda: run_tests())
    }
    extras = [
              Dictation("text"),
              Choice("path",
                    {"natlink": "c:/natlink/natlink", "sea":"C:/",
                     }),
              Choice("filetype",
                    {"java": "*.java", "python":"*.py",
                     })
             ]
    defaults = {"text": ""}

class Experimental(MappingRule):
    
    mapping = {
        # experimental/incomplete commands
        
        "experiment <text>":            Function(experiment),
        "short talk number <n2>":       Text("%(n2)d"), 
    #     "dredge [<id> <text>]":         Function(dredge),
        "test dragonfly paste":         Paste("some text"),
     
    }
    extras = [
              Dictation("text"),
              IntegerRefST("n2", 1, 100)
             ]
    defaults = {"text": ""}

# .ending
def load():
    global grammar
    grammar.add_rule(StackTest())
    grammar.add_rule(DevelopmentHelp())
    grammar.add_rule(Experimental())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()