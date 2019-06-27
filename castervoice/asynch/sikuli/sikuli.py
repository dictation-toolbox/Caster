from castervoice.lib.imports import *
from subprocess import Popen
import traceback
import socket


class SikuliController():
    grammar = Grammar("sikuli")
    custom_rule = None
    server_proxy = None
    timer = None

    def launch_IDE(self):
        ide_path = settings.SETTINGS["paths"]["SIKULI_IDE"]
        if ide_path == "":
            print("No 'SIKULI_IDE' path is available. Did you configure it in " + settings.get_filename())
        else:
            Popen(["java", "-jar", ide_path])

    def launch_server(self):
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

    def execute(self, fname):
        try:
            fn = getattr(self.server_proxy, fname)
            fn()
        except Exception:
            utilities.simple_log()

    def terminate_sick_command(self):
        if self.custom_rule:
            self.grammar.unload()
            self.grammar.remove_rule(self.custom_rule)
            self.grammar.load()
        control.nexus().comm.coms.pop('sikuli')
        self.server_proxy.terminate()

    def start_server_proxy(self):
        self.server_proxy = control.nexus().comm.get_com("sikuli")
        fns = self.server_proxy.list_functions()
        # Even though bootstrap_start_server_proxy() didn't load grammar before,
        # you have to unload() here because terminate_sick_command() might have been
        # called before and loaded the grammar.
        self.grammar.unload()
        self.populate_grammar(fns)
        self.grammar.load()
        print("Caster-Sikuli server started successfully.")

    def populate_grammar(self, fns):
        if len(fns) > 0:
            mapping_custom_commands = self.generate_custom_commands(fns)
            self.custom_rule = MappingRule(mapping=mapping_custom_commands, name="sikuli custom")
            self.grammar.add_rule(self.custom_rule)

    def generate_custom_commands(self, list_of_functions):
        mapping = {}
        for fname in list_of_functions:
            spec = " ".join(fname.split("_"))
            mapping[spec] = Function(self.execute, fname=fname)
        return mapping

    def server_proxy_timer_fn(self):
        print("Attempting Caster-Sikuli connection [...]")
        try:
            self.start_server_proxy()
            if self.timer:
                self.timer.stop()
                self.timer = None
        except socket.error:
            pass
        except Exception:
            traceback.print_exc()

    def bootstrap_start_server_proxy(self):
        try:
            # if the server is already running, this should go off without a hitch
            self.start_server_proxy()
        except Exception:
            self.launch_server()
            seconds5 = 5
            self.timer = get_engine().create_timer(self.server_proxy_timer_fn, seconds5)

sikuli = SikuliController()

class SikuliControlCommandsRule(MergeRule):
    pronunciation = "sikuli"

    mapping = {
        "launch sick IDE":       R(Function(sikuli.launch_IDE)),
        "launch sick server":    R(Function(sikuli.bootstrap_start_server_proxy)),
        "terminate sick server": R(Function(sikuli.terminate_sick_command)),
    }

if settings.SETTINGS["sikuli"]["enabled"]:
    rule = SikuliControlCommandsRule()
    sikuli.grammar.add_rule(rule)
    control.non_ccr_app_rule(rule, context=None, rdp=False)
    sikuli.bootstrap_start_server_proxy()
