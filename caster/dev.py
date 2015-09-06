from subprocess import Popen
import time

from dragonfly import (FocusWindow, Function, Key, BringApp, Text, WaitWindow, Dictation, Choice, Grammar, MappingRule, IntegerRef, Paste)

from caster.lib import utilities, settings, ccr, context, navigation, control
from caster.lib.ccr2.recording.playback import PlaybackRule
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.communication import Communicator
from caster.lib.dfplus.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from caster.lib.dfplus.state.actions2 import ConfirmAction, BoxAction
from caster.lib.dfplus.state.short import L, S, R


grammar = Grammar('development')

# from Tkinter import * 
# from tkColorChooser import askcolor 
def experiment(text):
    '''this function is for tests'''
    comm = Communicator()
    comm.get_com("status").error(0)

# 

def get_color():
    '''do asynchronously'''
#     print askcolor()





LAST_TIME=0
def print_time():
    global LAST_TIME
    print time.time()-LAST_TIME
    LAST_TIME=time.time()

COUNT=5
def countdown():
    global COUNT
    print COUNT
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
    print settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")
    try:
        BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"]).execute()
    except Exception:
        utilities.simple_log()
        
def abc():
    print "success 100"

def xyz(data):
    print data




control.nexus().macros_grammar.unload()
a = PlaybackRule()

control.nexus().macros_grammar.add_rule(a)

control.nexus().macros_grammar.load()

a.refresh()



class DevRule(MappingRule):
    
    mapping = {
    # development tools
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          R(BringApp("C:/Windows/explorer.exe", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")), rdescript="Open Natlink Folder"),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "refresh ccr directory":        Function(ccr.refresh_from_files),  # will need to disable and reenable language
    "Agrippa <filetype> <path>":    Function(grep_this),
    
    # experimental/incomplete commands
    
    "experiment <text>":            Function(experiment),
    "short talk number <n2>":       Text("%(n2)d"), 
#     "dredge [<id> <text>]":         Function(dredge),
    
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
    
    "test box action":              BoxAction(xyz, rdescript="Test Box Action", box_type=settings.QTYPE_DEFAULT, 
                                              log_failure=True),
    
    "test dragonfly paste":         Paste("some text"),
     
    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              IntegerRefST("n", 1, 5),
              Choice("id",
                    {"R": 1, "M":2,
                     }),
              Choice("path",
                    {"natlink": "c:/natlink/natlink", "sea":"C:/",
                     }),
              Choice("filetype",
                    {"java": "*.java", "python":"*.py",
                     }),
              IntegerRefST("n2", 1, 100)
             ]
    defaults = {
               "text": "", "id":None
               }

# .ending
def load():
    global grammar
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
