from dragonfly import ( Key, Text , Playback, Function, Repeat,
                        BringApp,IntegerRef, Grammar, Dictation,
                        MappingRule, Mouse, Choice, WaitWindow)
import sys, win32api, time, win32clipboard, natlink
from ctypes import windll
from win32con import MOUSEEVENTF_WHEEL
from win32api import GetSystemMetrics
import paths, utilities, settings

BASE_PATH = paths.get_base()
MMT_PATH = paths.get_mmt()
NIRCMD_PATH = paths.get_nircmd()

def initialize_clipboard():
    utilities.MULTI_CLIPBOARD = utilities.load_json_file(paths.get_saved_clipboard_path())

def clipboard_to_file(n):
    key=str(n)
    time.sleep(0.05)# time for keypress to execute
    win32clipboard.OpenClipboard()
    utilities.MULTI_CLIPBOARD[key]=win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    utilities.save_json_file(utilities.MULTI_CLIPBOARD, paths.get_saved_clipboard_path())

def volume_control(n, volume_mode):
    global NIRCMD_PATH
    max_volume = 65535
    sign=1
    command="setsysvolume"# default
    mode=str(volume_mode)
    message="setting volume to "
    if mode=="up":
        command="changesysvolume"
        message="increasing volume by "
    elif mode=="down":
        command="changesysvolume"
        message="decreasing volume by "
        sign=-1
    chosen_level=str(int(n*sign* 1.0/100*max_volume))
    try:
        BringApp(NIRCMD_PATH, command, chosen_level).execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    utilities.report(message+str(n), speak=settings.SPEAK)
 
    
def drop(n, n2):
    key=str(n)
    times=int(n2)
    if key in utilities.MULTI_CLIPBOARD:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(utilities.MULTI_CLIPBOARD[key])
        win32clipboard.CloseClipboard()
        for i in range(0, times):
            Key("c-v")._execute()
    else:
        natlink.execScript ("TTSPlayString \"slot empty\"")
    
def auto_spell(mode, text):
    # to do: add support for other modes
    format_mode=str(mode)
    if format_mode == "spell":
        base="".join(str(text).split(" ")).lower()
        Text(base)._execute()
    elif format_mode == "crunch":
        Text(str(text).lower())._execute()
    elif format_mode == "caps":
        Text(str(text).upper())._execute()
    elif format_mode == "sent":
        base=str(text).capitalize()
        Text(base)._execute()
        
def scroll(direction, n):
    updown=-100
    if str(direction)== "up":
        updown= 100
    (x, y) = win32api.GetCursorPos()
    win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, updown*n, 0)
    
def kick():
    window_title=utilities.get_active_window_title()
    if window_title=="Custom Grid":
        Playback([(["I", "left"], 0.0)])._execute()
    else:
        Playback([(["mouse", "left", "click"], 0.0)])._execute()

def kick_right():
    window_title=utilities.get_active_window_title()
    if window_title=="Custom Grid":
        Playback([(["I", "right"], 0.0)])._execute()
    else:
        Playback([(["mouse", "right", "click"], 0.0)])._execute()

def kick_middle():
    windll.user32.mouse_event(0x00000020,0,0,0,0)
    windll.user32.mouse_event(0x00000040,0,0,0,0)

def grid_to_window():
    BringApp("pythonw", paths.get_grid(), "--rowheight","20" , "--columnwidth","20" , "--numrows","20" , 
             "--numcolumns","20","--sizeToClient",utilities.get_active_window_hwnd())._execute()
             
def grid_full():# make sure to change both references to pythonw when you upgrade this
    screen_width = GetSystemMetrics (0)
    screen_height =GetSystemMetrics (1)
    BringApp(paths.get_grid(),
        "--width",str((screen_width - 20)),"--height",str((screen_height - 30)),"--locationx","10","--locationy","15", 
        "--rowheight","20" , "--columnwidth","20" , "--numrows","20", "--numcolumns","20")._execute()
    WaitWindow(executable="CustomGrid.exe")._execute()
    Key("h")._execute()
    
def pixel_jump(direction,direction2,n5):
    x,y= 0, 0
    d=str(direction)
    d2=str(direction2)
    if d=="up" or d2=="up":
        y=-n5
    if d=="down" or d2=="down":
        y=n5
    if d=="left" or d2=="left":
        x=-n5
    if d=="right" or d2=="right":
        x=n5
    
    Mouse("<"+ str(x)+ ", "+str(y)+ ">").execute()
    
def color(color_mode, n):
    c=str(color_mode)
    if c=="up":
        Key("shift:down, up/5:"+str(n)+", shift:up").execute()
    elif c=="down":
        Key("shift:down, down/5:"+str(n)+", shift:up").execute()
    elif c=="left" or c=="back":
        Key("cs-left/5:"+str(n)).execute()
    elif c=="right":
        Key("cs-right/5:"+str(n)).execute()
    elif c=="home":
        Key("s-home").execute()
    elif c=="end":
        Key("s-end").execute()

def fly(fly_mode, n):
    f=str(fly_mode)
    if f=="top":
        Key("c-home").execute()
    elif f=="bottom":
        Key("c-end").execute()
    elif f=="left" or f=="back":
        Key("c-left/5:"+str(n)).execute()
    elif f=="right":
        Key("c-right/5:"+str(n)).execute()
    elif f=="home":
        Key("home").execute()
    elif f=="end":
        Key("end").execute()

    
class MainRule(MappingRule):
    mapping = {

	
    #mouse control
    'kick':                         Function(kick),
	'kick mid': 				    Function(kick_middle),
	'kick right': 	                Function(kick_right),
    '(kick double|double kick)':    Playback([(["mouse", "double", "click"], 0.0)]),
    "shift right click":            Key("shift:down")+ Mouse("right")+ Key("shift:up"),
    "scroll [<direction>] <n>":     Function(scroll, extra={'direction', 'n'}),
    'be grid position mode':        BringApp("pythonw", paths.get_grid(), r"--positionMode"),
    'be grid wrap':                 Function(grid_to_window),
    'be grid':                      Function(grid_full),
    "curse <direction> [<direction2>] [<n5>]":Function(pixel_jump, extra={"direction","direction2","n5"}),
    "side left":                    Playback([(["MouseGrid"], 0.1),(["four", "four"], 0.1),(["click"], 0.0)]),
    "side right":                   Playback([(["MouseGrid"], 0.1),(["six", "six"], 0.1),(["click"], 0.0)]),
    "center":                       Playback([(["MouseGrid"], 0.1),(["click"], 0.0)]),
    
    
    
    #keyboard shortcuts
	"username":                     Text("synkarius"),
    'save':                         Key("c-s"),
    'scratch':                      Playback([(["scratch", "that"], 0.0)]),
    'enter [<n>]':                  Key("enter")* Repeat(extra="n"),
    'space [<n>]':                  Key("space")* Repeat(extra="n"),
    "down [<n>]":                   Key("down") * Repeat(extra="n"),
    "up [<n>]":                     Key("up") * Repeat(extra="n"),
    "left [<n>]":                   Key("left") * Repeat(extra="n"),
    "right [<n>]":                  Key("right") * Repeat(extra="n"),
    "fly [<fly_mode>] [<n>]":       Function(fly, extra={"fly_mode", " n"}),
    "(coup | color) [<color_mode>] [<n>]":   Function(color, extra={"color_mode", "n"}),
    "shin [<n>]":                   Key("s-right") * Repeat(extra="n"),
    "shin back [<n>]":              Key("s-left") * Repeat(extra="n"),
    "find":                         Key("c-f"),
    "replace":                      Key("c-h"),
    "copy [<n>]":                   Key("c-c")+Function(clipboard_to_file, extra="n"),
    "cut [<n>]":                    Key("c-x")+Function(clipboard_to_file, extra="n"),
    "select all":                   Key("c-a"),
    "drop [<n>] [times <n2>]":      Function(drop, extra={"n","n2"}),
    "delete [<n>]":                 Key("del/5") * Repeat(extra="n"),
    "clear [<n>]":                  Key("backspace") * Repeat(extra="n"),
    "(cancel | escape)":            Key("escape"),
    "excite mark":                  Text("!"),
     
    # miscellaneous
    'auto <mode> <text>':           Function(auto_spell, extra={"mode","text"}),
    "(<volume_mode> [system] volume [to] <n> | volume <volume_mode> <n>)": Function(volume_control, extra={'n','volume_mode'}),
    }
    extras = [
              IntegerRef("n", 1, 500),
              IntegerRef("n2", 1, 1000),
              IntegerRef("n5", 1, 1000),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("direction",
                    {"up": "up", "down": "down", "left": "left", "right": "right",
                    }),
              Choice("direction2",
                    {"up": "up", "down": "down", "left": "left", "right": "right",
                    }),
              Choice("mode",
                    {"spell": "spell", "sent": "sent", "crunch": "crunch", "caps": "caps",
                    }),
              Choice("color_mode",
                    {"left": "left", "back": "back", "up": "up", "down": "down", 
                     "right": "right", "home": "home", "end": "end",
                    }),
              Choice("volume_mode",
                    {"set": "set", "increase": "up", "decrease": "down",
                     "up":"up","down":"down"}),
              Choice("fly_mode",
                    {"left": "left", "back": "back", "top": "top", "bottom": "bottom", 
                     "right": "right", "home": "home", "end": "end", "away": "end",
                    }),
             ]
    defaults ={"n": 1,"n2": 1,"text": "", "n5":5, "color_mode":"right", "fly_mode":"right",
               "direction2":"", "volume_mode": "setsysvolume"
               }

initialize_clipboard()
grammar = Grammar('mouse_and_keyboard')
grammar.add_rule(MainRule())
grammar.load()
