from subprocess import Popen
import time

from dragonfly import *

from caster.lib import utilities, settings, ccr, context, control
from caster.lib.dfplus.hint.hintnode import NodeRule, NodeAction
from caster.lib.dfplus.hint.nodes import css
from caster.lib.dfplus.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.pita import selector, fn


grammar = Grammar('development')

# from Tkinter import *
# from tkColorChooser import askcolor 
def experiment(text):
    '''this function is for tests'''
    try:
        ''''''
        print str(text)
            
    except Exception:
        utilities.simple_log(False)

# 

def get_color():
    '''do asynchronously'''
#     print askcolor()

def get_similar_process_name(spoken_phrase, list_of_processes):
    best = (0, "")
    process = selector._abbreviated_string(spoken_phrase)
    
    unwanted_processes=["wininit", "csrss", "System Idle Process", "winlogon",  \
                        "SearchFilterHost", "conhost"]
    wanted_processes=[x for x in list_of_processes if x not in unwanted_processes]
#     print wanted_processes
    
    for w in wanted_processes:
        # make copies because _phrase_to_symbol_similarity_score is destructive (of spoken phrase)
        process_lower = process.lower()
        w_lower = w.lower()
        
        score = selector._phrase_to_symbol_similarity_score(process_lower, w_lower)
        if score > best[0]:
            best = (score, w)
     
    return best[1]

def dredge(id, text):
    print Window.get_foreground().executable
#     print Window.get_all_windows()

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
    grep="H:/PROGRAMS/NON_install/AstroGrep/AstroGrep.exe"
    Popen([grep, "/spath=\""+str(path) +"\"", "/stypes=\""+str(filetype)+"\"", "/stext=\""+str(c)+"\"", "/s"])


def close_last_spoken(spoken):
    first = spoken[0]
    Text("</"+first+">").execute()
def close_last_rspec(rspec):
    Text("</"+rspec+">").execute()

class DevRule(MappingRule):
    
    mapping = {
    # development tools
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "refresh ccr directory":        Function(ccr.refresh_from_files),  # will need to disable and reenable language
    "Agrippa <filetype> <path>":    Function(grep_this),
    
    # experimental/incomplete commands
    "zone test":                    R(Text("a")+Text("b")), 
    
    "experiment <text>":            Function(experiment),
    # 
    "dredge [<id> <text>]":         Function(dredge),
    
    "close last tag":               ContextSeeker([L(S(["cancel"], None),
                                                     S(["html spoken"], close_last_spoken, use_spoken=True), 
                                                     S(["span", "div"], close_last_rspec, use_rspec=True))
                                                   ]),
    "html":                         R(Text("<html>"), rspec="html spoken"), 
    "divider":                      R(Text("<div>"), rspec="div"),
    "span":                         R(Text("<span>"), rspec="span"),
    "backward seeker [<text>]":     ContextSeeker([L(S(["ashes"], Text, "ashes1 [%(text)s] "),
                                                      S(["bravery"], Text, "bravery1 [%(text)s] ")), 
                                                   L(S(["ashes"], Text, "ashes2 [%(text)s] "),
                                                      S(["bravery"], Text, "bravery2 [%(text)s] "))
                                                   ]), 
    "forward seeker [<text>]":      ContextSeeker(forward=
                                                  [L(S(["ashes"], Text, "ashes1 [%(text)s] "),
                                                      S(["bravery"], Text, "bravery1 [%(text)s] ")), 
                                                   L(S(["ashes"], Text, "ashes2 [%(text)s] "),
                                                      S(["bravery"], Text, "bravery2 [%(text)s] "))
                                                   ]),
    "never-ending":                 AsynchronousAction([L(S(["ashes", "charcoal"], print_time, None),
                                                      S(["bravery"], Text, "bravery1"))
                                                   ], time_in_seconds=0.2, repetitions=20),
    "ashes":                        RegisteredAction(Text("ashes fall "), rspec="ashes"),
    "bravery":                      RegisteredAction(Text("bravery is weak "), rspec="bravery"),
    "charcoal boy <text> [<n>]":    R(Text("charcoal is dirty %(text)s"), rspec="charcoal"),
                            

    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              IntegerRef("n", 1, 100),
              Choice("id",
                    {"R": 1, "M":2,
                     }),
              Choice("path",
                    {"natlink": "c:/natlink/natlink", "sea":"C:/",
                     }),
              Choice("filetype",
                    {"java": "*.java", "python":"*.py",
                     }),
#               RuleRef(css_rule, css_rule.master_node.text), 
             ]
    defaults = {
               "text": "", "id":None
               }


# grammar = None

def load():
    global grammar
#     grammar = Grammar('development')
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
