#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import datetime
import logging

from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()

from castervoice.lib import settings  
settings.initialize()

from castervoice.lib.ctrl.updatecheck import UpdateChecker # requires settings/dependencies
UpdateChecker().initialize()

from dragonfly import get_engine

_NEXUS = None

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
