from dragonfly import *
import os, natlink, sys, win32api
import string
from win32con import *
import paths

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()

def clear_pyc():
    global BASE_PATH
    os.chdir(BASE_PATH)
    for files in os.listdir("."):
        if files.endswith(".pyc"):
            filepath=BASE_PATH+files
            os.remove(filepath)
            print "Deleted: "+filepath
    
def auto_spell(text):
    #To do: add capitalization, support for military alphabet
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
    
def suicide():
    BringApp(BASE_PATH + r"\suicide.bat")._execute()
    
def open_and(text,text2):
    print text
    print text2
    
def test():
    import pydevd;pydevd.settrace()
    BringApp("pythonw", paths.get_grid(), r" --width 364" , r" --height 182" , r" --locationx 93" , r" --locationy 120" , r" --rowheight 20" , r" --columnwidth 20" , r" --numrows 20" , r" --numcolumns 20")._execute()

class MainRule(MappingRule):
    global MMT_PATH
    mapping = {
    # Dragon NaturallySpeaking management
    '(reload|restart|reboot) (dragon|dragonfly)':         Function(clear_pyc)+Playback([(["stop", "listening"], 0.5), (["wake", 'up'], 0.0)]),
	'deactivate': 			Playback([(["go", "to", "sleep"], 0.0)]),
	'scratch': 			Playback([(["scratch", "that"], 0.0)]),
    '(number|numbers) mode':             Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':             Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':             Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':             Playback([(["normal", "mode", "on"], 0.0)]),
    "dragon (death | suicide) and rebirth":   Function( suicide ),
	
    #mouse control
    '(kick left|kick)': 			Playback([(["mouse", "left", "click"], 0.0)]),
	'kick mid': 				    Playback([(["mouse", "middle", "click"], 0.0)]),
	'kick right': 	                Playback([(["mouse", "right", "click"], 0.0)]),
    '(kick double|double kick)':    Playback([(["mouse", "double", "click"], 0.0)]),
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
    
    # monitor management
    'toggle monitor one':               BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':               BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY2"),
    
    # window management
    "open <text> and <text2>":      Function(open_and, extra={'text','text2'}),
    "alt tab":          Key( "w-backtick"),#activates Switcher
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    #military alphabet
    "alpha": Key("a"),
    "bravo": Key("b"),
    "charlie": Key("c"),
    "delta": Key("d"),
    "echo": Key("e"),
    "foxtrot": Key("f"),
    "golf": Key("g"),
    "hotel": Key("h"),
    "India": Key("i"),
    "Juliet": Key("j"),
    "kilo": Key("k"),
    "Lima": Key("l"),
    "Mike": Key("m"),
    "November": Key("n"),
    "oscar": Key("o"),
    "papa": Key("p"),
    "Quebec": Key("q"),
    "Romeo": Key("r"),
    "Sierra": Key("s"),
    "tango": Key("t"),
    "uniform": Key("u"),
    "victor": Key("v"),
    "whiskey": Key("w"),
    "x-ray": Key("x"),
    "yankee": Key("y"),
    "Zulu": Key("z"),
    
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

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
