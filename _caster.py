'''
main Caster module
Created on Jun 29, 2014
'''

import importlib
from castervoice.lib.ctrl.dependencies import DependencyMan  # requires nothing
DependencyMan().initialize()

from castervoice.lib import settings # requires DependencyMan to be initialized
settings.initialize()

from castervoice.lib.ctrl.updatecheck import UpdateChecker # requires settings/dependencies
UpdateChecker().initialize()

from castervoice.lib.ctrl.configure_engine import EngineConfigEarly, EngineConfigLate
EngineConfigEarly() # requires settings/dependencies

_NEXUS = None

from castervoice.lib import printer
from castervoice.lib import control

if control.nexus() is None: # Initialize Caster State
    from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
    from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
    from castervoice.lib.ctrl.mgr.loading.load.reload_fn_provider import ReloadFunctionProvider
    from castervoice.lib.ctrl.mgr.loading.load.modules_access import SysModulesAccessor
    _crg = ContentRequestGenerator()
    _rp = ReloadFunctionProvider()
    _sma = SysModulesAccessor()
    _content_loader = ContentLoader(_crg, importlib.import_module, _rp.get_reload_fn(), _sma)
    control.init_nexus(_content_loader)
    EngineConfigLate() # Requires grammars to be loaded and nexus
   
if settings.SETTINGS["sikuli"]["enabled"]:
    from castervoice.asynch.sikuli import sikuli_controller
    sikuli_controller.get_instance().bootstrap_start_server_proxy()

printer.out("\n*- Starting " + settings.SOFTWARE_NAME + " -*")
