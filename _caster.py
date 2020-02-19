#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import datetime
import logging

logging.basicConfig(format = "%(asctime)s : %(levelname)s : %(funcName)s\n%(msg)s")   

from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()

from castervoice.lib import settings  
settings.initialize()

from castervoice.lib.ctrl.updatecheck import UpdateChecker # requires settings/dependencies
UpdateChecker().initialize()

from dragonfly import get_engine
from dragonfly.windows.window import Window


_NEXUS = None

class LoggingHandler(logging.Handler):
    def emit(self, record):
        # Brings status window to the forefront upon error
        if settings.SETTINGS["miscellaneous"]["status_window_foreground_on_error"]:
            title = None
            # The window title is unique to Natlink
            if get_engine()._name == 'natlink':
                import natlinkstatus  # pylint: disable=import-error
                status = natlinkstatus.NatlinkStatus()
                if status.NatlinkIsEnabled() == 1:
                    title = "Messages from Python Macros V"
            windows = Window.get_matching_windows(title=title)
            if windows and title is not None:
                windows[0].set_foreground()

logger1 = logging.getLogger('action')
logger1.addHandler(LoggingHandler())

logger2 = logging.getLogger('engine')
logger2.addHandler(LoggingHandler())

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
