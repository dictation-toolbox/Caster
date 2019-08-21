#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''

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
from castervoice.lib.ccr.standard import SymbolSpecs
if settings.WSR:
    from castervoice.lib.ccr.standard import SymbolSpecs
    SymbolSpecs.set_cancel_word("escape")
from castervoice.lib import control
_NEXUS = control.nexus()

from castervoice.asynch.sikuli import sikuli_controller

if not globals().has_key('profile_switch_occurred'):
    # Load user rules
    _NEXUS.process_user_content()
    # _NEXUS.merger.update_config()
    # _NEXUS.merger.merge(MergeInf.BOOT)

if globals().has_key('profile_switch_occurred'):
    reload(sikulixx)
else:
    profile_switch_occurred = None

if settings.SETTINGS["sikuli"]["enabled"]:
    sikuli_controller.get_instance().bootstrap_start_server_proxy()

print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")

if settings.WSR:
    get_engine().recognize_forever()
