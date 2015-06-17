'''
--Caster WSR module--
Can be run by itself to use Caster with Windows Speech Recognition or 
to activate WSR after Dragon is already running. 

If you're interested in running Dragonfly, but not Caster, use a similar
pattern to the
if __name__ == "__main__":
section.

'''

from subprocess import Popen
import time, pythoncom


if __name__ == "__main__":
    print "WSR Speech Recognition is garbage; it is recommended that you not run Caster this way."
    import __init__
    import _caster
    while True:
        pythoncom.PumpWaitingMessages()  # @UndefinedVariable
        time.sleep(.1)
else:
    
    from dragonfly import Choice, MappingRule, Grammar, Function
    import natlink
    from lib import settings
    
    def deactivate_natlink():
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