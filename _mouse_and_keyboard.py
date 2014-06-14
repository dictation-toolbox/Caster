from dragonfly import ( Key, Text , Playback, Function, Repeat,
                        BringApp,IntegerRef, Grammar, Dictation,
                        MappingRule, Pause, Mouse)
import sys, win32api
from win32con import MOUSEEVENTF_WHEEL
import paths, utilities

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

    
def auto_spell(text):
    #To do: add capitalization, support for military alphabet
    # use a Choice to switch between modes
    try:
        base="".join(str(text).split(" ")).lower()
        Text(base)._execute()
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        
def scroll(text, n):
    direction=str(text)
    updown=-100
    if direction== "up" or direction == "north":
        updown= 100
    (x, y) = win32api.GetCursorPos()
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, updown*n, 0)

    
def copy_clip(n):
    base=str(n)
    Key( "c-"+base)._execute()
    Key( "c-c")._execute()
    
def paste_clip(n):
    base=str(n)
    Key( "c-"+base)._execute()
    Key( "c-v")._execute()
    
def test():
    #import pydevd;pydevd.settrace()
    BringApp("pythonw", paths.get_grid(), "--width","364" , "--height","182" , "--locationx","93" , 
             "--locationy","120" , "--rowheight","20" , "--columnwidth","20" , "--numrows","20" , 
             "--numcolumns","20","--sizeToClient",utilities.get_active_window_hwnd())._execute()

class MainRule(MappingRule):
    global MMT_PATH
    mapping = {

	
    #mouse control
    '(kick left|kick)': 			Playback([(["mouse", "left", "click"], 0.0)]),
	'kick mid': 				    Playback([(["mouse", "middle", "click"], 0.0)]),
	'kick right': 	                Playback([(["mouse", "right", "click"], 0.0)]),
    '(kick double|double kick)':    Playback([(["mouse", "double", "click"], 0.0)]),
    "shift right click":            Key("shift:down")+ Mouse("right")+ Key("shift:up"),
    "scroll [<text>] <n>":     Function(scroll, extra={'text', 'n'}),
    'grid app position mode':               BringApp("pythonw", paths.get_grid(), r"--positionMode"),
    'grid app test mode':               Function(test),
    
    
    #keyboard shortcuts
	"username":                    Text("synkarius"),
    "nat link":                     Text( "natlink" ),
    'save [work]':                  Key("c-s"),
    'enter':                        Key("enter"),
    "(down | south) [<n>]":                Key("down") * Repeat(extra="n"),
    "(up | north) [<n>]":                  Key("up") * Repeat(extra="n"),
    "(left | west) [<n>]":               Key("left") * Repeat(extra="n"),
    "(right | east) [<n>]":               Key("right") * Repeat(extra="n"),
    "fly (left | west | back) [<n>]":                Key("c-left") * Repeat(extra="n"),
    "fly [(right | east)] [<n>]":               Key("c-right") * Repeat(extra="n"),
    "color (left | west | back) [<n>]":                Key("cs-left") * Repeat(extra="n"),
    "color [(right | east)] [<n>]":               Key("cs-right") * Repeat(extra="n"),
    "color (up | north) [<n>]":               Key("shift:down, up, shift:up") * Repeat(extra="n"),
    "color (down | south) [<n>]":               Key("shift:down, down, shift:up") * Repeat(extra="n"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy":                             Key("c-c"),
    "cut":                              Key("c-x"),
    "select all":                       Key("c-a"),
    "drop":                            Key("c-v"),
    "delete [<n>]":                (Key("del")+Pause("5")) * Repeat(extra="n"),
    "clear [<n>]":                Key("backspace") * Repeat(extra="n"),
    "(cancel | escape)":                Key("escape"),
    
    # miscellaneous
    "copy clip [<n>]":         Key("c-%(n)d,c-c"),# shortcut for tenclips
    "paste clip [<n>]":         Key("c-%(n)d,c-v"),# shortcut for tenclips
    'auto spell <text>': Function(auto_spell, extra='text'),
    
    }
    extras = [
              IntegerRef("n", 1, 10000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
             ]
    defaults ={"n": 1,
               "text": ""
               }

grammar = Grammar('mouse_and_keyboard')
grammar.add_rule(MainRule())
grammar.load()
