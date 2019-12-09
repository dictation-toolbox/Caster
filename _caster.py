#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import datetime
import logging
from dragonfly import get_engine
from dragonfly.windows.window import Window

logging.basicConfig(format = "%(asctime)s")  

from castervoice.lib import settings  # requires toml
settings.initialize()

from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()
_NEXUS = None

class LoggingHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        print("\n")
        # Brings status window to the forefront upon error
        if (settings.SETTINGS["miscellaneous"]["status_window_forefront_on_error"]):
             # The window title is unique to Natlink
            if (get_engine()._name == 'natlink'):
                windows = Window.get_matching_windows(None, "Messages from Python Macros V")
            if windows:
                windows[0].set_foreground()

logger1 = logging.getLogger('action')
logger1.addHandler(LoggingHandler())

logger2 = logging.getLogger('engine')
logger2.addHandler(LoggingHandler())

# Natlink with DNS requires 32-bit Python and Windows OS
# ToDo: create then move to castervoice.lib.ctrl.engines
if (get_engine()._name == 'natlink'):
    import struct
    if settings.SYSTEM_INFORMATION["platform"] not in ["win32", "win-amd64"]:
        msg = "Your platform ({}) is not currently supported by Caster."
        raise SystemError(msg.format(settings.SYSTEM_INFORMATION["platform"]))
    if struct.calcsize("P") == 8:  # 64-bit
        msg = "Caster is using a 64-bit python environment with Natlink. Natlink requires a 32-bit python environment"
        raise SystemError(msg)

settings.WSR = __name__ == "__main__"

if settings.WSR:
    from castervoice.rules.ccr.standard import SymbolSpecs
    SymbolSpecs.set_cancel_word("escape")
from castervoice.lib import control

if control.nexus() is None:
    from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
    from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
    _crg = ContentRequestGenerator()
    _content_loader = ContentLoader(_crg)
    control.init_nexus(_content_loader)

if settings.SETTINGS["sikuli"]["enabled"]:
    from castervoice.asynch.sikuli import sikuli_controller
    sikuli_controller.get_instance().bootstrap_start_server_proxy()
print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")
if settings.WSR:
    get_engine().recognize_forever()
