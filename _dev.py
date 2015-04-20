from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Repeat, Grammar, MappingRule, Choice, Mimic, FocusWindow)

from lib import utilities, settings, control, ccr
from lib.dfplus.state import ContextSeeker, CL, CS
from lib.pita import selector


if control.DEP.PSUTIL:
    import psutil


def experiment(text):
    '''this function is for tests'''
    try:
        ''''''
        
            
    except Exception:
        utilities.simple_log(False)

def get_top_parent(psutil_process):
    parent=psutil_process.parent()
    if parent==None:
        return psutil_process
    else:
        return get_top_parent(parent)

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
    if id==None:
        Mimic("press", "alt", "tab").execute()
    elif id==1:
        # proc
        if control.DEP.PSUTIL:
            l=[]
            d={}
            
            for proc in psutil.process_iter():
                try:
                    name=proc.name().split(".")[0]
#                     if name not in unwanted_processes:
                    l.append(name)
                    d[name]=proc.pid
                except Exception:
                    pass
            best=get_similar_process_name(str(text), l)
            p = d[best]
#             print d
            print text, "->", best, p#, utilities.get_active_window_title(p)
            try:
                utilities.focus_window(pid=p)
            except Exception:
                utilities.simple_log()
            
        else:
            utilities.availability_message("'dredge' command", "psutil")        
    elif id==2:
        # title
        ''''''
        utilities.get_active_window_title()
    

class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment <text>":            Function(experiment, extra="text"),
    
    "dredge [<id> <text>]":         Function(dredge), 
    
    # will need to disable and reenable language
    "refresh ccr directory":        Function(ccr._refresh_from_files), 
    
    "context seeker test":          ContextSeeker([CL(CS(["ashes"], Text, "ashes to ashes"), 
                                                      CS(["bravery"], Mimic, ["you", "can", "take", "our", "lives"]))
                                                   ], None), 
    
    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              IntegerRef("n", 1, 100),
              Choice("id",
                    {"R": 1, "M":2,
                     }),
             ]
    defaults = {
               "text": "", "id":None
               }


grammar = None

def load():
    grammar = Grammar('development')
    grammar.add_rule(DevRule())
    grammar.load()

if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
