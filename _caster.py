#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import os, time, sys
import logging
logging.basicConfig()

import time, socket, os
from dragonfly import (get_engine, Function, Grammar, Playback, Dictation, Choice, Pause,
                       RunCommand)
from castervoice.lib.ccr.standard import SymbolSpecs


def _wait_for_wsr_activation():
    count = 1
    while True:
        try:
            from castervoice.apps.browser import firefox
            break
        except:
            print(
                "(%d) Attempting to load Caster -- WSR not loaded and listening yet..." %
                count)
            count += 1
            time.sleep(1)


_NEXUS = None
from castervoice.lib import settings  # requires nothing
if settings.SYSTEM_INFORMATION["platform"] != "win32":
    raise SystemError("Your platform is not currently supported by Caster.")
settings.WSR = __name__ == "__main__"
from castervoice.lib import utilities  # requires settings
if settings.WSR:
    _wait_for_wsr_activation()
    SymbolSpecs.set_cancel_word("escape")
from castervoice.lib import control
_NEXUS = control.nexus()
from castervoice.lib import navigation
navigation.initialize_clipboard(_NEXUS)
from castervoice.apps import __init__
import castervoice.lib.dev.dev
from castervoice.asynch.sikuli import sikuli
from castervoice.lib.dfplus.merge.mergepair import MergeInf

if not globals().has_key('profile_switch_occurred'):
    # Load user rules
    _NEXUS.process_user_content()
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)

if globals().has_key('profile_switch_occurred'):
    reload(sikuli)
else:
    profile_switch_occurred = None

print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")

if settings.WSR:
    import pythoncom
    print("Windows Speech Recognition is garbage; it is " \
        +"recommended that you not run Caster this way. ")
    while True:
        get_engine().recognize_forever()
