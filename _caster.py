#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import datetime

from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator

import logging
logging.basicConfig()
from dragonfly import get_engine
from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()
_NEXUS = None
from castervoice.lib import settings  # requires toml
if settings.SYSTEM_INFORMATION["platform"] != "win32":
    raise SystemError("Your platform is not currently supported by Caster.")
settings.WSR = __name__ == "__main__"

if settings.WSR:
    from castervoice.lib.ccr.standard import SymbolSpecs
    SymbolSpecs.set_cancel_word("escape")
from castervoice.lib import control

if control.nexus() is None:
    _crg = ContentRequestGenerator()
    _content_loader = ContentLoader(_crg)
    control.init_nexus(_content_loader)

# TODO: whatever this was intended to do probably needs to be re-done:
# if globals().has_key('profile_switch_occurred'):
#     reload(sikulixx)
# else:
#     profile_switch_occurred = None

if settings.SETTINGS["sikuli"]["enabled"]:
    from castervoice.asynch.sikuli import sikuli_controller
    sikuli_controller.get_instance().bootstrap_start_server_proxy()
print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")
if settings.WSR:
    get_engine().recognize_forever()
