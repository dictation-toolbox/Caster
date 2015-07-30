from dragonfly import Text
from caster.lib import utilities, control, settings
from caster.lib.pita import scanner, selector

OLD_ACTIVE_WINDOW_TITLE = None
ACTIVE_FILE_PATH = [None, None]
CHOICES = []
TEN = ["numb one", "numb two", "numb three", "numb four", "numb five", 
       "numb six", "numb seven", "numb eight", "numb nine", "numb ten"]
 
def empty():
    global CHOICES
    CHOICES = []
    control.nexus().intermediary.text("PITA Cancel")
# 
def make_selection(nw=[]):
    global CHOICES, TEN
    n = -1
    while len(nw)>2:# in the event the last words spoken were a command chain,
        nw.pop()    # get only the number trigger
    j = ""
    if len(nw)>0:
        j = " ".join(nw)
    if j in TEN:
        n = TEN.index(j)
    if n == -1: n = 0
    Text(CHOICES[n][1]).execute()
    control.nexus().intermediary.text("PITA Completion")



def pita(textnv):
    global OLD_ACTIVE_WINDOW_TITLE, ACTIVE_FILE_PATH

    filename, folders, title = utilities.get_window_title_info()
    active_has_changed = OLD_ACTIVE_WINDOW_TITLE != title

    # check to see if the active file has changed; if not, skip this step
    if active_has_changed:
        OLD_ACTIVE_WINDOW_TITLE = title
        ACTIVE_FILE_PATH = scanner.guess_file_based_on_window_title(filename, folders)

    if filename == None:
        utilities.report("pita: filename pattern not found in window title")
        return

    if ACTIVE_FILE_PATH[0] != None:
        global CHOICES
        CHOICES = selector.get_similar_symbol_name(str(textnv), scanner.DATA["directories"][ACTIVE_FILE_PATH[0]][ACTIVE_FILE_PATH[1]]["names"])
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            display = ""
            counter = 1
            for result in CHOICES:
                if counter>1: display+="\n"
                display+=str(counter)+" "+result[1]
                counter+=1
            control.nexus().intermediary.hint(display)





















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

def pita_filter(spoken, choices):
    return selector.get_similar_symbol_name(spoken, choices)

def pita_selection(choice):
    Text(choice).execute()
    control.nexus().intermediary.text("PITA Completion")