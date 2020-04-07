#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import six

if six.PY2:
    import logging
    logging.basicConfig()

from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()

from castervoice.lib import settings  
settings.initialize()

from castervoice.lib.ctrl.updatecheck import UpdateChecker # requires settings/dependencies
UpdateChecker().initialize()

from dragonfly import get_engine

_NEXUS = None

# get_engine() is used here as a workaround for running Natlink inprocess
if get_engine().name in ["sapi5shared", "sapi5", "sapi5inproc"]:
    settings.WSR = True
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
