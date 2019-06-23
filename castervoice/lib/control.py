from dragonfly import Grammar

from castervoice.lib.ctrl.nexus import Nexus
from castervoice.lib import settings
from castervoice.lib.dfplus.merge import gfilter

_NEXUS = None

def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS


'''
Commands for easily loading different types of rules, e.g.:
control.non_ccr_app_rule(FirefoxRule(), AppContext("firefox"))
'''
def non_ccr_app_rule(rule, context=None):
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        nexus().merger.add_global_rule(rule)
    else:
        grammar = Grammar(str(rule), context=context)
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()

def ccr_app_rule(rule, context=None):
    nexus().merger.add_app_rule(rule, context=context)

def global_rule(rule):
    nexus().merger.add_global_rule(rule)

def selfmod_rule(rule):
    nexus().merger.add_selfmodrule(rule)