from subprocess import Popen
import xmlrpclib

from dragonfly import (Grammar, MappingRule, Function)

from castervoice.lib import control
from castervoice.lib import settings, utilities
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule

grammar = None
custom_rule = None
server_proxy = None

def launch_IDE():
    ide_path = settings.SETTINGS["paths"]["SIKULI_IDE"]
    if ide_path == "":
        print("No 'SIKULI_IDE' path is available. Did you configure it in " + settings.get_filename())
    else:
        Popen(["java", "-jar", ide_path])

def launch_server():
    runner_path = settings.SETTINGS["paths"]["SIKULI_RUNNER"]
    if runner_path == "":
        print("No 'SIKULI_RUNNER' path is available. Did you configure it in " + settings.get_filename())
    else:
        command = [] if settings.SETTINGS["sikuli"]["version"] == "1.1.3" else ["java", "-jar"]
        command.extend([
            settings.SETTINGS["paths"]["SIKULI_RUNNER"], 
            "-r", settings.SETTINGS["paths"]["SIKULI_SERVER_PATH"],
            "--args", settings.SETTINGS["paths"]["SIKULI_SCRIPTS_PATH"]
        ])
        Popen(command)
#     
#     Popen([
#         settings.SETTINGS["paths"]["SIKULI_COMPATIBLE_JAVA_EXE_PATH"], "-jar",
#         settings.SETTINGS["paths"]["SIKULI_SCRIPTS_JAR_PATH"], "-r",
#         settings.SETTINGS["paths"]["SIKULI_SERVER_PATH"]
#     ])

def execute(fname):
    try:
        global server_proxy
        fn = getattr(server_proxy, fname)
        fn()
    except Exception:
        utilities.simple_log()

def terminate_sick_command():
    global server_proxy
    global grammar
    global custom_rule
    grammar.unload()
    grammar.remove_rule(custom_rule)
    grammar.load()
    control.nexus().comm.coms.pop('sikuli')
    server_proxy.terminate()

def start_server_proxy():
    global server_proxy
    global grammar
    server_proxy = control.nexus().comm.get_com("sikuli")
    fns = server_proxy.list_functions()
    # Even though bootstrap_start_server_proxy() didn't load grammar before,
    # you have to unload() here because terminate_sick_command() might have been
    # called before and loaded the grammar.
    grammar.unload()
    populate_grammar(fns)
    grammar.load()
    print("Caster-Sikuli server started successfully.")

def populate_grammar(fns):
    global grammar
    global custom_rule
    if len(fns) > 0:
        mapping_custom_commands = generate_custom_commands(fns)
        custom_rule = MappingRule(mapping=mapping_custom_commands, name="sikuli custom")
        grammar.add_rule(custom_rule)

def generate_custom_commands(list_of_functions):
    mapping = {}
    for fname in list_of_functions:
        spec = " ".join(fname.split("_"))
        mapping[spec] = Function(execute, fname=fname)
    return mapping

def server_proxy_timer_fn():
    print("Attempting Caster-Sikuli connection [...]")
    try:
        start_server_proxy()
        control.nexus().timer.remove_callback(server_proxy_timer_fn)
    except Exception:
        pass

def bootstrap_start_server_proxy():
    try:
        # if the server is already running, this should go off without a hitch
        start_server_proxy()
    except Exception:
        launch_server()
        seconds5 = 5
        control.nexus().timer.add_callback(server_proxy_timer_fn, seconds5)

class SikuliControlCommandsRule(MergeRule):
    pronunciation = "sikuli"

    mapping = {
        "launch sick IDE": Function(launch_IDE),
        "launch sick server": Function(bootstrap_start_server_proxy),
        "terminate sick server": Function(terminate_sick_command),
    }

if settings.SETTINGS["sikuli"]["enabled"]:
    grammar = Grammar("sikuli")
    rule = SikuliControlCommandsRule(name="sikuli control commands")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    bootstrap_start_server_proxy()