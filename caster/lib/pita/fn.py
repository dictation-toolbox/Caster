from dragonfly import Text
from caster.lib import utilities, control, settings
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