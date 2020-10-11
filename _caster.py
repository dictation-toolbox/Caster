#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import imp
import logging
import six
from dragonfly import get_engine
from dragonfly import RecognitionObserver
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.ctrl.configure_engine import EngineConfigEarly, EngineConfigLate
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.updatecheck import UpdateChecker
from castervoice.lib.utilities import start_hud


class LoggingHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.hud = control.nexus().comm.get_com("hud")

    def emit(self, record):
        try:
            self.hud.send("# {}".format(record.msg))
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("# {}".format(record.msg))


class Observer(RecognitionObserver):
    def __init__(self):
        self.hud = control.nexus().comm.get_com("hud")

    def on_begin(self):
        pass

    def on_recognition(self, words):
        try:
            self.hud.send("$ {}".format(" ".join(words)))
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("$ {}".format(" ".join(words)))

    def on_failure(self):
        try:
            self.hud.send("?!")
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("?!")


if six.PY2:
    logging.basicConfig()
DependencyMan().initialize()  # requires nothing
settings.initialize()
UpdateChecker().initialize()  # requires settings/dependencies
EngineConfigEarly() # requires settings/dependencies

# get_engine() is used here as a workaround for running Natlink inprocess
if get_engine().name in ["sapi5shared", "sapi5", "sapi5inproc"]:
    settings.WSR = True
    from castervoice.rules.ccr.standard import SymbolSpecs
    SymbolSpecs.set_cancel_word("escape")

if control.nexus() is None:
    from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
    from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
    _crg = ContentRequestGenerator()
    _content_loader = ContentLoader(_crg)
    control.init_nexus(_content_loader)
    EngineConfigLate() # Requires grammars to be loaded and nexus

if settings.SETTINGS["sikuli"]["enabled"]:
    from castervoice.asynch.sikuli import sikuli_controller
    sikuli_controller.get_instance().bootstrap_start_server_proxy()

print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")

try:
    imp.find_module('PySide2')
    start_hud()
    _logger = logging.getLogger('caster')
    _logger.addHandler(LoggingHandler())  # must be after nexus initialization
    _logger.setLevel(logging.DEBUG)
    Observer().register()  # must be after HUD process has started
except ImportError:
    pass  # HUD is not available
