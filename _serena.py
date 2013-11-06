from dragonfly import *
import natlink,os

def foo():
   natlink.execScript ("TTSPlayString \"" +"I don't really know what to say"+ "\"")
   
def repeat_after(text):
   natlink.execScript ("TTSPlayString \"" +str(text)+ "\"")
   print "\n\nwe just said:"+str(text)
   
def clear_pyc():
    path = "C:\NatLink\NatLink\MacroSystem"
    os.chdir(path)
    for files in os.listdir("."):
        if files.endswith(".pyc"):
            filepath=path+"\\"+files
            os.remove(filepath)
            print "Deleted: "+filepath

class MainRule(MappingRule):
    mapping = {
               
    '(reload|restart|reboot) (dragon|dragonfly)':         Function(clear_pyc)+
                                                        Playback([(["stop", "listening"], 0.5), (["wake", 'up'], 0.0)]),           
               
               
    #speech functions
    'talk to me':       Function(foo),
    'repeat after me <text>': Function(repeat_after, extra='text'),
    
    }
    extras = [
              IntegerRef("xtimes", 1, 100),
              Dictation("text"),
              Dictation("text2")
             ]
    defaults ={"xtimes": 1}

grammar = Grammar('Serena')
grammar.add_rule(MainRule())
grammar.load()
#Reload Dragon