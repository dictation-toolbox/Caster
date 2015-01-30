import win32api, win32con, re
import xmlrpclib

from dragonfly import (Function, Text, Grammar, BringApp, WaitWindow, Key,
                       IntegerRef, Dictation, Mimic, MappingRule)
from dragonfly.actions.action_focuswindow import FocusWindow

from asynch.hmc import squeue
from asynch.hmc import h_launch
from lib import  settings
from lib import control
from lib import utilities
from lib.dragonfree import launch


NATLINK_AVAILABLE=True
try:
    import natlink
except Exception:
    NATLINK_AVAILABLE=False
    
STRICT_PARSER = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.ELEMENT_LISTENING_PORT))

def kill():
    communicate().kill()

def retrieve(n):
    n = int(n) - 1
    Text(communicate().retrieve(n))._execute()

def scroll(n):  # n is the index of the list item to scroll to
    communicate().scroll(int(n)-1)
    
def rescan():
    communicate().rescan()

def sticky_from_unordered(n, n2):
    n = int(n) - 1  # index of word in unordered list
    if n < 10:
        n = n + 10
    n2 = int(n2) - 1  # index of target slot in sticky list
    communicate().sticky(n, n2, "")
    
def sticky_copy(n):
    n = int(n) - 1  # index of target slot in sticky list
    Mimic("copy", "one")._execute()
    communicate().sticky(1, n, control.MULTI_CLIPBOARD["1"])

def add_word():
    Mimic("copy", "one")._execute()
    communicate().add_name(control.MULTI_CLIPBOARD["1"])

def remove_word(n):
    n = int(n) - 1
    communicate().remove(n)

def focus_element():
    FocusWindow(title=settings.ELEMENT_VERSION)._execute()
    WaitWindow(title=settings.ELEMENT_VERSION)._execute()

def search():
    if utilities.window_exists(None, settings.ELEMENT_VERSION):
        squeue.add_query(homunculus_to_element)
        h_launch.launch(settings.QTYPE_INSTRUCTIONS, "enter_search_word")
        WaitWindow(title=settings.HOMUNCULUS_VERSION, timeout=5)._execute()
        FocusWindow(title=settings.HOMUNCULUS_VERSION)._execute()
        Key("tab")._execute()



def focus_extensions():
    focus_element()
    communicate().focus_extensions()

def focus_directory_box():
    focus_element()
    communicate().focus_directory_box()
    
def filter_strict_request_for_data():
    global NATLINK_AVAILABLE
    if NATLINK_AVAILABLE:
        strict_filter(communicate().filter_strict_request_for_data())
    else:
        utilities.report("Dragon required for this feature ('filter strict')")

def scan_new():
    focus_element()
    Key("home")._execute()

def homunculus_to_element(data):
    word = data.replace("\n", "").rstrip()
    communicate().search(word)

def strict_filter(directory):
    for f in directory["files"].values():
        acceptably_difficult_to_type = []
        for name in f["names"]:
            difficult_to_type = word_breakdown(name)
            if difficult_to_type:
                acceptably_difficult_to_type.append(name)
        f["names"] = acceptably_difficult_to_type
    
    communicate().filter_strict_return_processed_data(directory)
            
def word_breakdown(name):
    
    global STRICT_PARSER
    found_something_difficult_to_type = False
    capitals_changed_to_underscores = STRICT_PARSER.sub(r'_\1', name).lower()
    broken_by_underscores = capitals_changed_to_underscores.split("_")
    for name_piece in broken_by_underscores:
        if not name_piece == "" and len(name_piece) > 1:
            dragon_check = natlink.getWordInfo(name_piece, 7)
            if dragon_check == None:  # only add letter combinations that Dragon doesn't recognize as words
                found_something_difficult_to_type = True
                break
    return found_something_difficult_to_type


    
def send_key_to_element(action_type):  # for some reason, some events are untriggerable without a keypress it seems, hence this
    try:
        element_hwnd = utilities.get_window_by_title(settings.ELEMENT_VERSION)
    except Exception:
        utilities.simple_log(False)
    if action_type == "scan_new":
        win32api.SendMessage(element_hwnd, win32con.WM_KEYDOWN, win32con.VK_HOME, 0)
        win32api.PostMessage(element_hwnd, win32con.WM_KEYUP, win32con.VK_HOME, 0)

def enable_element():
    launch.run(["pythonw", settings.SETTINGS["paths"]["ELEMENT_PATH"]])
    
#SSticky copy threeky copy toage
class ElementUsageRule(MappingRule):
    mapping = {
    "L scroll to <n>":              Function(scroll, extra="n"),
    "L get <n>":                    Function(retrieve, extra="n"),
    "L sticky list <n> to <n2>":    Function(sticky_from_unordered, extra={"n", "n2"}),
    "L sticky copy [<n>]":          Function(sticky_copy, extra="n"),
    "L add word":                   Function(add_word),
    "L remove word <n>":            Function(remove_word, extra="n"),
    "L search":                     Function(search),
    "L extensions":                 Function(focus_extensions),
    "L scan new":                   Function(scan_new),
    "L change directory":           Function(focus_directory_box),
    "L rescan directory":           Function(rescan),
    "L filter strict":              Function(filter_strict_request_for_data),
    
    }   
    extras = [
              IntegerRef("n", 1, 200),
              IntegerRef("n2", 1, 100),
              Dictation("text"),
             ]
    defaults = {"n": 1, "n2": 1,
               "text": "",
               }

eur=ElementUsageRule()

class ElementLaunchRule(MappingRule):
    mapping = {
    "run element":                  Function(enable_element)+Function(eur.enable),
    "kill element":                 Function(kill)+Function(eur.disable),
    }   
    extras = []
    defaults = {}


elr=ElementLaunchRule()

grammar = Grammar('element')
grammar.add_rule(elr)
grammar.add_rule(eur)
grammar.load()

if not utilities.window_exists(classname= None, windowname=settings.ELEMENT_VERSION):
    eur.disable()
