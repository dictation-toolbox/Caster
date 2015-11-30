from dragonfly import Text
from dragonfly.windows.window import Window

from caster.lib import utilities
from caster.lib.dfplus.state.actions2 import SuperFocusWindow
from caster.lib.pita import scanner, selector


def pita_list_provider():
    filename, folders, title = utilities.get_window_title_info()
    active_file_path = scanner.guess_file_based_on_window_title(filename, folders)
    if filename is None:
        print("pita: filename pattern not found in window title")
        return []
    if active_file_path[0] is not None:
        return scanner.DATA["directories"][active_file_path[0]][active_file_path[1]]["names"]
    else:
        return []

def pita_filter(data, choices):
    return selector.get_similar_symbol_name(list(data["text"].words), choices)

def pita_selection(choice):
    Text(choice).execute()

#==================================================#==================================================
#==================================================#==================================================
#==================================================#==================================================

# executable match
def dredge_ex_list_provider():
    return list(set([x.executable.split("\\")[-1][:-4] for x  in Window.get_all_windows()]))

def dredge_ex_filter(data, choices):
    return selector.get_similar_process_names(list(data["text"].words), choices)

def dredge_ex_selection(choice):
    SuperFocusWindow(executable=choice+".exe").execute()

#==================================================

# title match
def dredge_tie_list_provider():
    return list(set([x.title for x  in Window.get_all_windows()]))

def dredge_tie_filter(data, choices):
    return selector.get_similar_window_names(list(data["text"].words), choices)

def dredge_tie_selection(choice):
    SuperFocusWindow(title=choice, rdescript="Focus: "+choice).execute()

