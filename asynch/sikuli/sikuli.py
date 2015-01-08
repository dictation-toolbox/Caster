import xmlrpclib

from dragonfly import (Grammar, MappingRule, Function)

from lib import settings, control, utilities
from lib.dragonfree import launch

grammar = None
server_proxy = None


def launch_IDE():
    launch.run([settings.SETTINGS["paths"]["SIKULI_COMPATIBLE_JAVA_EXE_PATH"],
                "-jar", settings.SETTINGS["paths"]["SIKULI_IDE_JAR_PATH"]])
    
def launch_server():
    launch.run([settings.SETTINGS["paths"]["SIKULI_COMPATIBLE_JAVA_EXE_PATH"],
                "-jar", settings.SETTINGS["paths"]["SIKULI_SCRIPTS_JAR_PATH"],
                "-r", settings.SETTINGS["paths"]["SIKULI_SERVER_PATH"]
                ])

def start_server_proxy():
    global server_proxy
    server_proxy = xmlrpclib.ServerProxy("http://localhost:" + str(settings.SIKULI_LISTENING_PORT))
    server_proxy.ping()
    utilities.report("sikuli server proxy started successfully")
#     print dir(server_proxy)
    
def server_proxy_timer_fn():
    utilities.report("attempting server proxy")
    try:
        start_server_proxy()
        control.TIMER_MANAGER.remove_callback(server_proxy_timer_fn)
    except Exception:
        pass
    


def refresh():
    ''' should be able to add new scripts on the fly and then call this '''

class SikuliControlRule(MappingRule):
    mapping = {
    "launch sick IDE":           Function(launch_IDE),
    "Launch sick server":        Function(launch_server),
    }

if settings.SETTINGS["miscellaneous"]["sikuli_enabled"]:
    grammar = Grammar("sikuli")
    grammar.add_rule(SikuliControlRule())
    grammar.load()
    
    # start server
    try:
        # if the server is already running, this should go off without a hitch
        start_server_proxy()
    except Exception:
        launch_server()
        seconds5 = 5
        control.TIMER_MANAGER.add_callback(server_proxy_timer_fn, seconds5)
        

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
