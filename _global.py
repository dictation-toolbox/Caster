from dragonfly import *
import os, natlink, sys
import string

def clear_pyc():
    path = "C:\NatLink\NatLink\MacroSystem"
    os.chdir(path)
    for files in os.listdir("."):
        if files.endswith(".pyc"):
            filepath=path+"\\"+files
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
    
def copy_clip(xtimes):
    base=str(xtimes)
    Key( "c-"+base)._execute()
    Key( "c-c")._execute()
    
def paste_clip(xtimes):
    base=str(xtimes)
    Key( "c-"+base)._execute()
    Key( "c-v")._execute()
    
def program_to_other_monitor(text):
    try:
        process_name= ""+ text.format()
        capitalized_process_names=["Hearthstone","iTunes"]
        if process_name not in capitalized_process_names:
            process_name=process_name.lower()
        if process_name== "google chrome":
            process_name= "chrome"
        process_name="\""+process_name+ ".exe\""
        print "cmd  attempting to toggle "+process_name
        BringApp(r"C:\NatLink\NatLink\MacroSystem\MultiMonitorTool\MultiMonitorTool.exe", r"/MoveWindow", "Next", "Process", process_name)._execute()
        Key("a-f2")._execute()
        Pause("50").execute()
        Key("c,m,d,tab")._execute()
        
        commands_text=r"C:\NatLink\NatLink\MacroSystem\MultiMonitorTool\MultiMonitorTool.exe /MoveWindow Next Process "+process_name
        
        Text(commands_text)._execute()
        Pause("50").execute()
        Key("enter")._execute()
        Pause("50").execute()
        Key("e,x,i,t,enter")._execute()
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]

def suicide():
    BringApp(r"C:\NatLink\NatLink\MacroSystem\suicide.bat")._execute()

class MainRule(MappingRule):
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
	'drag':				Mouse("left:down"),
	'release':			Mouse("left:up"),
    'right drag':                Mouse("right:down"),
    'right release':            Mouse("right:up"),
    
    
    #keyboard shortcuts
	"username":                    Text("synkarius"),
    'email one':			        Text("synkarius@gmail.com"),
	'email two':			        Text("dconway1985@gmail.com"),
    'email three':                    Text("kyran36@hotmail.com"),
    'save [work]':                  Key("c-s"),
    'enter':                        Key("enter"),
    "down <xtimes>":                Key("down") * Repeat(extra="xtimes"),
    "up <xtimes>":                  Key("up") * Repeat(extra="xtimes"),
    "left <xtimes>":                Key("left") * Repeat(extra="xtimes"),
    "right <xtimes>":               Key("right") * Repeat(extra="xtimes"),
    "fly left [<xtimes>]":                Key("c-left") * Repeat(extra="xtimes"),
    "fly right [<xtimes>]":               Key("c-right") * Repeat(extra="xtimes"),
    "color left [<xtimes>]":                Key("cs-left") * Repeat(extra="xtimes"),
    "color right [<xtimes>]":               Key("cs-right") * Repeat(extra="xtimes"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy":                             Key("c-c"),
    "cut":                              Key("c-x"),
    "select all":                       Key("c-a"),
    "paste":                            Key("c-v"),
    
    "copy clip [<xtimes>]":         Key("c-%(xtimes)d,c-c"),
    "paste clip [<xtimes>]":         Key("c-%(xtimes)d,c-v"),
    
    'auto spell <text>': Function(auto_spell, extra='text'),
    "alt tab":          Key( "w-backtick"),#activates Switcher
    
    '(open|launch) eclipse':        BringApp(r"D:\PROGRAMS\NON_install\eclipse\eclipse.exe"),
    '(open|launch) everything':        BringApp(r"D:\PROGRAMS\NON_install\Everything"),
    '(open|launch) chrome':        BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    '(open|launch) process explorer':        BringApp(r"D:\PROGRAMS\NON_install\procexp.exe"),
    '(put on|play) Pandora':        Playback([(["open", "chrome"], 0.5), (["new", 'tab'], 0.5)])+ Key( "f6")+ Text( "Pandora.com")+ Key( "enter"),
    '(open|launch) (grep|homegroup)':        BringApp(r"D:\PROGRAMS\NON_install\AstroGrep\AstroGrep.exe"),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    'toggle monitor one':               BringApp(r"C:\NatLink\NatLink\MacroSystem\MultiMonitorTool\MultiMonitorTool.exe", r"/switch",r"\\.\DISPLAY1"),
    'toggle monitor two':               BringApp(r"C:\NatLink\NatLink\MacroSystem\MultiMonitorTool\MultiMonitorTool.exe", r"/switch",r"\\.\DISPLAY2"),
    'toggle program <text>': Function(program_to_other_monitor, extra='text'),
    
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
    
    #'(put on|play) [some] music':   BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    #                                +WaitWindow("Chrome", "chrome.exe", 2000)+Key("f6,w,w,w,dot,p,a,n,d,o,r,a,dot,c,o,m,enter"),
    }
    extras = [
              IntegerRef("xtimes", 1, 100),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
             ]
    defaults ={"xtimes": 1}

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
#Reload Dragon