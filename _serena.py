from dragonfly import *
import natlink,os,win32gui,sys
import paths

BASE_PATH = paths.get_base()
NIRCMD_PATH = paths.get_nircmd()

def talk_to_me():
    natlink.execScript ("TTSPlayString \"" +"I am Serena, version 0.1.67"+ "\"")
   
def repeat_after(text):
    natlink.execScript ("TTSPlayString \"" +str(text)+ "\"")
    print "\n\nwe just said:"+str(text)
   
def get_mouse_point():
    global BASE_PATH
    x,y= win32gui.GetCursorPos()
    natlink.execScript ("TTSPlayString \"" +"mouse coordinates "+str(x) + " by " +str(y)+ "\"")
    f = open(BASE_PATH+'mouse_points_universal.txt','a')
    f.write(str(x)+', ' + str(y)+'\n')
    f.close() 

def goto_point(quantity):
    global BASE_PATH
    f = open(BASE_PATH+'mouse_points_universal.txt','r')
    listFile=f.readlines()
    f.close()
    if len( listFile )>=quantity:
        is_docked=not win32gui.IsIconic(win32gui.FindWindow(None, "DragonBar - Premium"))
        
        pieces =listFile[quantity-1].rstrip('\n').split( ",")
        x= int(pieces[0])
        y= int(pieces[1])
        if is_docked:
            docking_buffer= 30
            y=y- docking_buffer
        Mouse("["+ str(x)+ ", "+str(y)+ "]").execute()
        
    #window_handle=win32gui.WindowFromPoint((2, 2))
    #print win32gui.GetWindowText(window_handle)
            
                  

def volume_control(quantity):
    global NIRCMD_PATH
    max_volume = 65535
    chosen_level=str(int(quantity* 1.0/100*max_volume))
    try:
        BringApp(NIRCMD_PATH, r"setsysvolume",chosen_level).execute()
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
    BringApp(NIRCMD_PATH, r"setsysvolume",chosen_level).execute()
    natlink.execScript ("TTSPlayString \"" +"setting volume to "+str( quantity )+ "\"")


class MainRule(MappingRule):
    mapping = {
               
               
               
               
    #speech functions
    'talk to me':       Function(talk_to_me),
    'repeat after me <text>': Function(repeat_after, extra='text'),
    "point save":   Function(get_mouse_point),
    "fly go [to] <quantity>": Function(goto_point, extra='quantity'),
    "set [system] volume [to] <quantity>": Function(volume_control, extra='quantity'),
    }
    extras = [
              IntegerRef("quantity", 1, 100),
              Dictation("text"),
              Dictation("text2")
             ]
    defaults ={"quantity": 1}

grammar = Grammar('Serena')
grammar.add_rule(MainRule())
grammar.load()
#Reload Dragon