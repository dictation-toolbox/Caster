from dragonfly import *
import natlink,os,win32gui

MACRO_PATH='C:\NatLink\NatLink\MacroSystem\\'

def foo():
   natlink.execScript ("TTSPlayString \"" +"I am Serena, version 0.1.59"+ "\"")
   
def repeat_after(text):
   natlink.execScript ("TTSPlayString \"" +str(text)+ "\"")
   print "\n\nwe just said:"+str(text)
   
def get_mouse_point():
    global MACRO_PATH
    x,y= win32gui.GetCursorPos()
    natlink.execScript ("TTSPlayString \"" +"mouse coordinates "+str(x) + " by " +str(y)+ "\"")
    f = open(MACRO_PATH+'mouse_points_universal.txt','a')
    f.write(str(x)+', ' + str(y)+'\n')
    f.close() 

def goto_point(quantity):
    global MACRO_PATH
    f = open(MACRO_PATH+'mouse_points_universal.txt','r')
    list=f.readlines()
    f.close()
    if len( list )>=quantity:
        is_docked=not win32gui.IsIconic(win32gui.FindWindow(None, "DragonBar - Premium"))
        
        pieces =list[quantity-1].rstrip('\n').split( ",")
        x= int(pieces[0])
        y= int(pieces[1])
        if is_docked:
            docking_buffer= 30
            y=y- docking_buffer
        Mouse("["+ str(x)+ ", "+str(y)+ "]").execute()
        
    #window_handle=win32gui.WindowFromPoint((2, 2))
    #print win32gui.GetWindowText(window_handle)
            
                  

def volume_control(quantity):
    max_volume = 65535
    chosen_level=str(int(quantity* 1.0/100*max_volume))
    BringApp(r"C:\NatLink\NatLink\MacroSystem\nircmd\nircmd.exe", r"setsysvolume",chosen_level).execute()
    natlink.execScript ("TTSPlayString \"" +"setting volume to "+str( quantity )+ "\"")
          


class MainRule(MappingRule):
    mapping = {
               
               
               
               
    #speech functions
    'talk to me':       Function(foo),
    'repeat after me <text>': Function(repeat_after, extra='text'),
    "point save":   Function(get_mouse_point),
    'point show':        BringApp(r"pythonw",r"C:\Users\dave\Dropbox\backup\dragonfly\_screenGrid.py"),
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