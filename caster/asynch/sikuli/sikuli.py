import xmlrpclib

from dragonfly import (Grammar, MappingRule, Function, Key)
from subprocess import Popen
from caster.lib import settings, control, utilities


grammar = None
server_proxy = None

def launch_IDE():
    Popen([settings.SETTINGS["paths"]["SIKULI_COMPATIBLE_JAVA_EXE_PATH"],
                "-jar", settings.SETTINGS["paths"]["SIKULI_IDE_JAR_PATH"]])
    
def launch_server():
    Popen([settings.SETTINGS["paths"]["SIKULI_COMPATIBLE_JAVA_EXE_PATH"],
                "-jar", settings.SETTINGS["paths"]["SIKULI_SCRIPTS_JAR_PATH"],
                "-r", settings.SETTINGS["paths"]["SIKULI_SERVER_PATH"]
                ])
#

def execute(fname):
    try:
        global server_proxy
        fn=getattr(server_proxy, fname)
        fn()
    except Exception:
        utilities.simple_log()

def generate_commands(list_of_functions):
    global server_proxy
    global grammar
    mapping = {}
    for fname in list_of_functions:
        spec = " ".join(fname.split("_"))
        mapping[spec] = Function(execute, fname=fname)
    grammar.unload()
    grammar.add_rule(MappingRule(mapping=mapping))
    grammar.load()

def start_server_proxy():
    global server_proxy
    server_proxy = xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.SIKULI_LISTENING_PORT))
    generate_commands(server_proxy.list_functions())
    utilities.report("sikuli server proxy started successfully")
    
def server_proxy_timer_fn():
    utilities.report("attempting server proxy [still loading]")
    try:
        start_server_proxy()
        control.TIMER_MANAGER.remove_callback(server_proxy_timer_fn)
    except Exception:
        pass
    
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

def refresh():
    ''' should be able to add new scripts on the fly and then call this '''
    unload()
    global grammar
    grammar = Grammar("sikuli")
    def refresh_sick_command():
        server_proxy.terminate()
        refresh()
    
    mapping = {
    "launch sick IDE":           Function(launch_IDE),
    "launch sick server":        Function(launch_server),
    "refresh sick you Lee":      Function(refresh_sick_command),
    "sick shot":                 Key("cs-2"),
    }
    grammar.add_rule(MappingRule(name="sik", mapping=mapping))
    grammar.load()
    # start server
    try:
        # if the server is already running, this should go off without a hitch
        start_server_proxy()
    except Exception:
        launch_server()
        seconds5 = 5
        control.TIMER_MANAGER.add_callback(server_proxy_timer_fn, seconds5)


if settings.SETTINGS["miscellaneous"]["sikuli_enabled"]:
    refresh()
        

