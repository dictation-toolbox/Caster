from subprocess import Popen
from dragonfly import Choice, MappingRule, Grammar, Function
from lib import settings

def deactivate_natlink():
    import natlink
    natlink.setMicState("sleeping")
    
def activate_wsr():
    Popen([settings.SETTINGS["paths"]["WSR_PATH"], "-SpeechUX"])

def kill_wsr():
    ''''''
#         launch.kill_process("sapisvr.exe")
    
class WSR_Rule(MappingRule):

    
    mapping = {
        "start listening":                      Function(deactivate_natlink),
        "(W S R | W S are)":                    Function(activate_wsr)
    
    }
    extras = []
    defaults = {}

          
wsra_rule = WSR_Rule()
grammar = Grammar('wsr hijack rule')
grammar.add_rule(wsra_rule)
grammar.load()