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
        
def scroll(text, xnumber):
    direction=str(text)
    updown=-100
    if direction== "up" or direction == "north":
        updown= 100
    (x, y) = win32api.GetCursorPos()
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, updown*xnumber, 0)

    
def copy_clip(xnumber):
    base=str(xnumber)
    Key( "c-"+base)._execute()
    Key( "c-c")._execute()
    
def paste_clip(xnumber):
    base=str(xnumber)
    Key( "c-"+base)._execute()
    Key( "c-v")._execute()
    
def suicide():
    BringApp(BASE_PATH + r"\suicide.bat")._execute()
    
def open_and(text,text2):
    print text
    print text2

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
    "scroll [<text>] <xnumber>":     Function(scroll, extra={'text', 'xnumber'}),
    
    #keyboard shortcuts
	"username":                    Text("synkarius"),
    "nat link":                     Text( "natlink" ),
    'save [work]':                  Key("c-s"),
    'enter':                        Key("enter"),
    "(down | south) [<xnumber>]":                Key("down") * Repeat(extra="xnumber"),
    "(up | north) [<xnumber>]":                  Key("up") * Repeat(extra="xnumber"),
    "(left | west) [<xnumber>]":               Key("left") * Repeat(extra="xnumber"),
    "(right | east) [<xnumber>]":               Key("right") * Repeat(extra="xnumber"),
    "fly (left | west | back) [<xnumber>]":                Key("c-left") * Repeat(extra="xnumber"),
    "fly [(right | east)] [<xnumber>]":               Key("c-right") * Repeat(extra="xnumber"),
    "color (left | west | back) [<xnumber>]":                Key("cs-left") * Repeat(extra="xnumber"),
    "color [(right | east)] [<xnumber>]":               Key("cs-right") * Repeat(extra="xnumber"),
    "color (up | north) [<xnumber>]":               Key("shift:down, up, shift:up") * Repeat(extra="xnumber"),
    "color (down | south) [<xnumber>]":               Key("shift:down, down, shift:up") * Repeat(extra="xnumber"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy":                             Key("c-c"),
    "cut":                              Key("c-x"),
    "select all":                       Key("c-a"),
    "drop":                            Key("c-v"),
    "delete [<xnumber>]":                (Key("del")+Pause("5")) * Repeat(extra="xnumber"),
    "clear [<xnumber>]":                Key("backspace") * Repeat(extra="xnumber"),
    "(cancel | escape)":                Key("escape"),
    
    # miscellaneous
    "copy clip [<xnumber>]":         Key("c-%(xnumber)d,c-c"),# shortcut for tenclips
    "paste clip [<xnumber>]":         Key("c-%(xnumber)d,c-v"),# shortcut for tenclips
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
              IntegerRef("xnumber", 1, 10000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
             ]
    defaults ={"xnumber": 1,
               "text": ""
               }

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
