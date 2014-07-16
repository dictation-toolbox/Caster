from dragonfly import *
import natlink,os,win32gui,sys
import paths, utilities, config

BASE_PATH = paths.get_base()
NIRCMD_PATH = paths.get_nircmd()

def talk_to_me():
    version_number="0.1.80"
    utilities.report("I am Serena, version "+version_number, speak=True)
       
def repeat_after(text):
    utilities.report(str(text))
#     natlink.execScript ("TTSPlayString \"" +str(text)+ "\"")
#     print "\n\nwe just said:"+str(text)
   
# def get_mouse_point():
#     global BASE_PATH
#     x,y= win32gui.GetCursorPos()
#     natlink.execScript ("TTSPlayString \"" +"mouse coordinates "+str(x) + " by " +str(y)+ "\"")
#     f = open(BASE_PATH+'mouse_points_universal.txt','a')
#     f.write(str(x)+', ' + str(y)+'\n')
#     f.close() 

# def goto_point(n):
#     global BASE_PATH
#     f = open(BASE_PATH+'mouse_points_universal.txt','r')
#     listFile=f.readlines()
#     f.close()
#     if len( listFile )>=n:
#         is_docked=not win32gui.IsIconic(win32gui.FindWindow(None, "DragonBar - Premium"))
#         
#         pieces =listFile[n-1].rstrip('\n').split( ",")
#         x= int(pieces[0])
#         y= int(pieces[1])
#         if is_docked:
#             docking_buffer= 30
#             y=y- docking_buffer
#         Mouse("["+ str(x)+ ", "+str(y)+ "]").execute()
        
    #window_handle=win32gui.WindowFromPoint((2, 2))
    #print win32gui.GetWindowText(window_handle)
            
                  

def volume_control(n, mode):
    global NIRCMD_PATH
    max_volume = 65535
    sign=1
    command="setsysvolume"# default
    mode=str(mode)
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
#         print "Unexpected error:", sys.exc_info()[0]
#         print "Unexpected error:", sys.exc_info()[1]
    utilities.report(message+str(n), speak=config.SPEAK)
#     natlink.execScript ("TTSPlayString \"" +message+str( n )+ "\"")


class MainRule(MappingRule):
    mapping = {
    #speech functions
    'talk to me':       Function(talk_to_me),
    'repeat after me <text>': Function(repeat_after, extra='text'),
    "(<mode> [system] volume [to] <n> | volume <mode> <n>)": Function(volume_control, extra={'n','mode'}),
    }
    extras = [
              IntegerRef("n", 1, 100),
              Dictation("text"),
              Dictation("text2"),
              Choice("mode",
                    {"set": "set", "increase": "up", "decrease": "down",
                     "up":"up","down":"down"}),
             ]
    defaults ={"n": 1,"mode": "setsysvolume"}

grammar = Grammar('Serena')
grammar.add_rule(MainRule())
grammar.load()
#Reload Dragon