from subprocess import Popen
import traceback
import socket

from dragonfly import get_current_engine, Function, Playback

from castervoice.lib import settings, utilities, control, printer


class SikuliController(object):

    _ENABLE_GEN_RULE = Playback([(["enable", "sikuli", "custom"], 0.0)])
    _DISABLE_GEN_RULE = Playback([(["disable", "sikuli", "custom"], 0.0)])

    def __init__(self):
        self._server_proxy = None
        self._timer = None

    def launch_IDE(self):
        """
        Launches the Sikuli IDE. Has no effect on anything else.
        """
        ide_path = settings.SETTINGS["paths"]["SIKULI_IDE"]
        if ide_path == "":
            print("No 'SIKULI_IDE' path is available. Did you configure it in " + settings.get_filename())
        else:
            Popen(["java", "-jar", ide_path])

    def bootstrap_start_server_proxy(self):
        """
        There are two parts to getting Sikuli running: the server and the
        server proxy. The server is an independent process, which needs to
        already be running before the server proxy is started. This method
        attempts to start the server proxy and then if that fails, it starts
        the server and sets a timer to retry the server proxy.
        """
        try:
            # if the server is already running, this should go off without a hitch
            self._start_server_proxy()
        except Exception:
            self._start_server()
            five_seconds = 5
            self._timer = get_current_engine().create_timer(self._retry_server_proxy, five_seconds)

    def _start_server(self):
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

    def _start_server_proxy(self):
        """
        This method will fail if the server isn't started yet.
        """
        # this will never fail:
        self._server_proxy = control.nexus().comm.get_com("sikuli")
        # this will fail if the server isn't started yet:
        self._server_proxy.list_functions()
        # success at this point:
        printer.out("Caster-Sikuli server started successfully.")
        SikuliController._ENABLE_GEN_RULE.execute()

    def _retry_server_proxy(self):
        printer.out("Attempting Caster-Sikuli connection [...]")
        try:
            self._start_server_proxy()
            if self._timer:
                self._timer.stop()
                self._timer = None
        except socket.error:
            pass
        except Exception:
            traceback.print_exc()

    def terminate_server_proxy(self):
        control.nexus().comm.coms.pop('sikuli')
        self._server_proxy.terminate()
        SikuliController._DISABLE_GEN_RULE.execute()

    def _execute(self, fname):
        try:
            fn = getattr(self._server_proxy, fname)
            fn()
        except Exception:
            utilities.simple_log()

    def generate_commands(self):
        list_of_functions = []
        if self._server_proxy is not None:
            list_of_functions = self._server_proxy.list_functions()
        mapping = {}
        for fname in list_of_functions:
            spec = " ".join(fname.split("_"))
            mapping[spec] = Function(self._execute, fname=fname)
        return mapping


_INSTANCE = None


def get_instance():
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = SikuliController()
    return _INSTANCE
