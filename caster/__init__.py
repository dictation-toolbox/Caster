try:
    from caster.lib import settings# requires nothing
    settings.WSR = __name__ == "__main__"
    from caster.lib import utilities# requires settings
    from caster.lib import control# requires settings
    from caster.lib.dfplus.state.stack import CasterState# requires control
    control.nexus().inform_state(CasterState())
    
    from caster.apps import *
    from caster.asynch import *
    from caster.lib import context
    import caster.lib.dev.dev
    try:
        import caster.w
    except Exception:
        pass
    from caster.asynch.hmc import h_launch
    from caster.asynch.hmc import vocabulary_processing
    from caster.asynch.sikuli import sikuli
    from caster.lib import navigation, password
    from caster.lib.pita import scanner
    from caster.lib.dfplus.state.short import R
    from caster.lib.dfplus.additions import IntegerRefST
    
    from caster.lib.dfplus.merge.ccrmerger import Inf
    from caster.lib.ccr import *
    from caster.lib.ccr.recording.again import Again
    from caster.lib.ccr.recording.alias import VanillaAlias
    from caster.lib.ccr.recording import history
    from caster.lib.dev import dev
    from caster.lib.dfplus.hint.nodes import css
    from caster.user.filters.examples import scen4, modkeysup
    from caster import user
    
except:
    print "\nAttempting to load CCR anyway..."
    from caster.lib import utilities
    from caster.lib import control# requires settings
    from caster.lib.dfplus.state.stack import CasterState# requires control
    control.nexus().inform_state(CasterState())
    
    utilities.simple_log()

def boot_message():
    if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
        utilities.report("\nWARNING: Status Window is an experimental feature, and there is a known freezing glitch with it.\n")
    utilities.report("*- Starting " + settings.SOFTWARE_NAME + " -*")

boot_message()