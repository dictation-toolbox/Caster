from dragonfly import Text
from caster.lib import utilities, control, settings
from caster.lib.pita import scanner, selector

OLD_ACTIVE_WINDOW_TITLE = None
ACTIVE_FILE_PATH = [None, None]
CHOICES = []
TEN = ["numb one", "numb two", "numb three", "numb four", "numb five"
       "numb six", "numb seven", "numb eight", "numb nine", "numb ten"]


 

def empty():
    global CHOICES
    CHOICES = []
# 
def make_selection(nnavi50, stack):
    global CHOICES
    n = int(nnavi50)
    if n>len(CHOICES):
        return
    if n==-1:
        ''''''
    Text(CHOICES[n-1][1]).execute()

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
        try:
            if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
                display = ""
                counter = 1
                for result in CHOICES:
                    if counter>1: display+="\n"
                    display+=str(counter)+" "+result[1]
                    counter+=1
                control.nexus().intermediary.hint(display)
        except Exception:
            utilities.simple_log()


#         Text(result)._execute()
