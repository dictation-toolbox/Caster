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
        
def scroll(text, xtimes):
    direction=str(text)
    updown=-100
    if direction== "up" or direction == "north":
        updown= 100
    (x, y) = win32api.GetCursorPos()
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, updown*xtimes, 0)

    
def copy_clip(xtimes):
    base=str(xtimes)
    Key( "c-"+base)._execute()
    Key( "c-c")._execute()
    
def paste_clip(xtimes):
    base=str(xtimes)
    Key( "c-"+base)._execute()
    Key( "c-v")._execute()
    
def suicide():
    BringApp(BASE_PATH + "suicide.bat")._execute()

class MainRule(MappingRule):
    global MMT_PATH
    mapping = {
    '(reload|restart|reboot) (dragon|dragonfly)':         Function(clear_pyc)+
                                                        Playback([(["stop", "listening"], 0.5), (["wake", 'up'], 0.0)]),
	'deactivate': 			Playback([(["go", "to", "sleep"], 0.0)]),
	'scratch': 			Playback([(["scratch", "that"], 0.0)]),
    '(number|numbers) mode':             Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':             Playback([(["spell", "mode", "on"], 0.0)]),
    'dictation mode':             Playback([(["dictation", "mode", "on"], 0.0)]),
    'normal mode':             Playback([(["normal", "mode", "on"], 0.0)]),
    "dragon (death | suicide) and rebirth":   Function( suicide ),
	
    #mouse control
    '(kick left|kick)': 			Mouse("left:1"),#Playback([(["mouse", "left", "click"], 0.0)]),something
	'kick mid': 				Mouse("middle:1"),#Playback([(["mouse", "middle", "click"], 0.0)]),
	'kick right': 			Mouse("right:1"),#Playback([(["mouse", "right", "click"], 0.0)]),
    '(kick double|double kick)':           Mouse("left:2"),
    "scroll [<text>] <xtimes>":     Function(scroll, extra={'text', 'xtimes'}),
    
    #keyboard shortcuts
	"username":                    Text("synkarius"),
    'email one':			        Text("synkarius@gmail.com"),
	'email two':			        Text("dconway1985@gmail.com"),
    'email three':                    Text("kyran36@hotmail.com"),
    'save [work]':                  Key("c-s"),
    'enter':                        Key("enter"),
    "(down | south) [<xtimes>]":                Key("down") * Repeat(extra="xtimes"),
    "(up | north) [<xtimes>]":                  Key("up") * Repeat(extra="xtimes"),
    "(left | west) [<xtimes>]":               Key("left") * Repeat(extra="xtimes"),
    "(right | east) [<xtimes>]":               Key("right") * Repeat(extra="xtimes"),
    "fly (left | west | back) [<xtimes>]":                Key("c-left") * Repeat(extra="xtimes"),
    "fly [(right | east)] [<xtimes>]":               Key("c-right") * Repeat(extra="xtimes"),
    "color (left | west | back) [<xtimes>]":                Key("cs-left") * Repeat(extra="xtimes"),
    "color [(right | east)] [<xtimes>]":               Key("cs-right") * Repeat(extra="xtimes"),
    "color (up | north) [<xtimes>]":               Key("shift:down, up, shift:up") * Repeat(extra="xtimes"),
    "color (down | south) [<xtimes>]":               Key("shift:down, down, shift:up") * Repeat(extra="xtimes"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy":                             Key("c-c"),
    "cut":                              Key("c-x"),
    "select all":                       Key("c-a"),
    "paste":                            Key("c-v"),
    "delete [<xtimes>]":                (Key("del")+Pause("5")) * Repeat(extra="xtimes"),
    "clear [<xtimes>]":                Key("backspace") * Repeat(extra="xtimes"),
    "(cancel | escape)":                Key("escape"),
    
    "copy clip [<xtimes>]":         Key("c-%(xtimes)d,c-c"),
    "paste clip [<xtimes>]":         Key("c-%(xtimes)d,c-v"),
    
    'auto spell <text>': Function(auto_spell, extra='text'),
    "alt tab":          Key( "w-backtick"),#activates Switcher
    
    '(open|launch) eclipse':        BringApp(r"D:\PROGRAMS\NON_install\eclipse\eclipse.exe"),
    '(open|launch) everything':        BringApp(r"D:\PROGRAMS\NON_install\Everything"),
    '(open|launch) chrome':        BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    '(open|launch) process explorer':        BringApp(r"D:\PROGRAMS\NON_install\procexp.exe"),
    '(put on|play) Pandora':        BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")+Pause("100")+Key("c-t")+Pause("100")+ Text( "Pandora.com")+Pause("50")+ Key( "enter"),
    '(open|launch) (grep|homegroup)':        BringApp(r"D:\PROGRAMS\NON_install\AstroGrep\AstroGrep.exe"),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    'toggle monitor one':               BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':               BringApp(MMT_PATH, r"/switch",r"\\.\DISPLAY2"),
    
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
              IntegerRef("xtimes", 1, 10000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
             ]
    defaults ={"xtimes": 1,
               "text": ""
               }

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
