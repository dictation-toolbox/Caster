from dragonfly import (Function, Key, BringApp, Text, WaitWindow, IntegerRef, Dictation, Choice, Grammar, MappingRule)

from lib import utilities, settings
from lib.element import scanner, selector, strings


OLD_ACTIVE_WINDOW_TITLE = None
ACTIVE_FILE_PATH = [None, None]

def nothing_found():
    '''some kind of console or spoken warning here'''

def experiment(text):
    global OLD_ACTIVE_WINDOW_TITLE, ACTIVE_FILE_PATH
    '''this function is for tests'''
    try: 
        '''check to see if the active file has changed;
        if not, skip this step
        '''
        active_window_title = utilities.get_active_window_title().replace("\\", "/")
        active_has_changed = OLD_ACTIVE_WINDOW_TITLE != active_window_title
        filename = None
        path_folders = None
        
        
        if active_has_changed:
            OLD_ACTIVE_WINDOW_TITLE = active_window_title
            '''get name of active file and folders in path;
            will be needed to look up collection of symbols
            in scanner data'''
            # active file
            match_object = scanner.FILENAME_PATTERN.findall(active_window_title)
            if len(match_object) > 0:  
                filename = match_object[0]
            else:
                nothing_found()
                return
            # path folders
            path_folders = active_window_title.split("/")[:-1]
            ACTIVE_FILE_PATH = selector.guess_file_based_on_window_title(filename, path_folders)
        
        if ACTIVE_FILE_PATH[0] != None:
            print "fuzzy match: ", str(text), "->", strings.get_similar_symbol_name(str(text), scanner.DATA["directories"][ACTIVE_FILE_PATH[0]]["files"][ACTIVE_FILE_PATH[1]]["names"])
        else:
            print "ACTIVE_FILE_PATH: ", ACTIVE_FILE_PATH
            print "filename: ", filename
            print "path_folders: ", path_folders
        
    except Exception:
        utilities.simple_log(False)



class DevRule(MappingRule):
    
    mapping = {
    'refresh directory':            Function(utilities.clear_pyc),
    "(show | open) documentation":  BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) + WaitWindow(executable=settings.get_default_browser_executable()) + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),

    "open natlink folder":          BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
    "reserved word <text>":         Key("dquote,dquote,left") + Text("%(text)s") + Key("right, colon, tab/5:5") + Text("Text(\"%(text)s\"),"),
    "experiment <text>":            Function(experiment, extra="text"),
    }
    extras = [
              Dictation("text"),
              Dictation("textnv"),
              
             ]
    defaults = {
               "text": ""
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
