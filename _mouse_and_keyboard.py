from dragonfly import ( Key, Text , Playback, Function, Repeat,
                        BringApp,IntegerRef, Grammar, Dictation,
                        MappingRule, Pause, Mouse, Choice)
import sys, win32api, win32gui
from win32con import MOUSEEVENTF_WHEEL
from win32api import GetSystemMetrics
import paths, utilities

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

    
def auto_spell(mode, text):
    # to do: add support for other modes
    format_mode=str(mode)
    if format_mode == "spell":
        base="".join(str(text).split(" ")).lower()
        Text(base)._execute()
        
def scroll(direction, n):
    updown=-100
    if str(direction)== "up":
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
    
def grid_to_window():
    #import pydevd;pydevd.settrace()
    BringApp("pythonw", paths.get_grid(), "--rowheight","20" , "--columnwidth","20" , "--numrows","20" , 
             "--numcolumns","20","--sizeToClient",utilities.get_active_window_hwnd())._execute()
             
def grid_full():
    screen_width = GetSystemMetrics (0)
    screen_height =GetSystemMetrics (1)
    BringApp("pythonw", paths.get_grid(),
        "--width",str((screen_width - 20)),"--height",str((screen_height - 30)),"--locationx","10","--locationy","15", 
        "--rowheight","20" , "--columnwidth","20" , "--numrows","20", "--numcolumns","20")._execute()
    
def pixel_jump(direction,n2):
    x,y= win32gui.GetCursorPos()
    d=str(direction)
    if d=="up":
        y=y-n2
    elif dir=="down":
        y=y+n2
    elif d=="left":
        x=x-n2
    elif d=="right":
        x=x+n2
    Mouse("["+ str(x)+ ", "+str(y)+ "]").execute()
    
class MainRule(MappingRule):
    mapping = {

	
    #mouse control
    '(kick left|kick)': 			Playback([(["mouse", "left", "click"], 0.0)]),
# 	'kick mid': 				    Playback([(["mouse", "middle", "click"], 0.0)]),# doesn't work, use a Python function
	'kick right': 	                Playback([(["mouse", "right", "click"], 0.0)]),
    '(kick double|double kick)':    Playback([(["mouse", "double", "click"], 0.0)]),
    "shift right click":            Key("shift:down")+ Mouse("right")+ Key("shift:up"),
    "scroll [<direction>] <n>":     Function(scroll, extra={'direction', 'n'}),
    'grid position mode':           BringApp("pythonw", paths.get_grid(), r"--positionMode"),
    'grid wrap':                    Function(grid_to_window),
    'grid':                         Function(grid_full),
    "pixel <direction> <n2>":        Function(pixel_jump, extra={"direction","n2"}),
    
    #keyboard shortcuts
	"username":                     Text("synkarius"),
    "nat link":                     Text( "natlink" ),
    'save [work]':                  Key("c-s"),
    'enter [<n>]':                  Key("enter")* Repeat(extra="n"),
    'space [<n>]':                  Key("space")* Repeat(extra="n"),
    "down [<n>]":                   Key("down") * Repeat(extra="n"),
    "up [<n>]":                     Key("up") * Repeat(extra="n"),
    "left [<n>]":                   Key("left") * Repeat(extra="n"),
    "right [<n>]":                  Key("right") * Repeat(extra="n"),
    "fly (left | back) [<n>]":      Key("c-left") * Repeat(extra="n"),
    "fly [right] [<n>]":            Key("c-right") * Repeat(extra="n"),
    "color (left | back) [<n>]":    Key("cs-left") * Repeat(extra="n"),
    "color [right] [<n>]":          Key("cs-right") * Repeat(extra="n"),
    "color up [<n>]":               Key("shift:down, up, shift:up") * Repeat(extra="n"),
    "color down [<n>]":             Key("shift:down, down, shift:up") * Repeat(extra="n"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy":                         Key("c-c"),
    "cut":                          Key("c-x"),
    "select all":                   Key("c-a"),
    "drop [<n>]":                   Key("c-v")* Repeat(extra="n"),
    "delete [<n>]":                 (Key("del")+Pause("5")) * Repeat(extra="n"),
    "true delete line":             Playback([(["delete", "line"], 0.0)])* Repeat(3),
    "clear [<n>]":                  Key("backspace") * Repeat(extra="n"),
    "(cancel | escape)":            Key("escape"),
    "excite mark":                  Text("!"),
    
    # miscellaneous
    "copy clip [<n>]":              Key("c-%(n)d,c-c"),# shortcut for tenclips
    "paste clip [<n>]":             Key("c-%(n)d,c-v"),# shortcut for tenclips
    'auto <mode> <text>':           Function(auto_spell, extra={"mode","text"}),
    
    }
    extras = [
              IntegerRef("n", 1, 500),
              IntegerRef("n2", 1, 1000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("direction",
                    {"up": "up", "down": "down", "left": "left", "right": "right",
                    }),
              Choice("mode",
                    {"spell": "spell", "sent": "sent", "crunch": "crunch", "caps": "caps",
                    }),
             ]
    defaults ={"n": 1,"n2": 1,"text": ""
               }

grammar = Grammar('mouse_and_keyboard')
grammar.add_rule(MainRule())
grammar.load()
