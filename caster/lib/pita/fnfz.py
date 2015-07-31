from dragonfly import Text

from caster.lib import utilities, control, settings
from caster.lib.dfplus.monkeypatch import Window
from caster.lib.pita import scanner, selector


def pita_list_provider():
    filename, folders, title = utilities.get_window_title_info()
    active_file_path = scanner.guess_file_based_on_window_title(filename, folders)
    if filename == None:
        utilities.report("pita: filename pattern not found in window title")
        return []
    if active_file_path[0] != None:
        return scanner.DATA["directories"][active_file_path[0]][active_file_path[1]]["names"]
    else:
        return []

def pita_filter(data, choices):
    return selector.get_similar_symbol_name(list(data["text"].words), choices)

def pita_selection(choice):
    Text(choice).execute()
    control.nexus().intermediary.text("PITA Completion")

#==================================================#==================================================
#==================================================#==================================================
#==================================================#==================================================

def dredge_list_provider():
    return [x.executable.split("\\")[-1][:-4] for x  in Window.get_all_windows()]

def dredge_filter(data, choices):
    ''''''

def dredge_selection(choice):
    ''''''





