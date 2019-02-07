#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''

import logging
logging.basicConfig()

import time
from dragonfly import (Function, Grammar, Playback, Dictation, Choice, Pause)
from castervoice.lib.ccr.standard import SymbolSpecs

def _wait_for_wsr_activation():
    count = 1
    while True:
        try:
            from castervoice.apps import firefox
            break
        except:
            print("(%d) Attempting to load Caster -- WSR not loaded and listening yet..."
                  % count)
            count += 1
            time.sleep(1)

_NEXUS = None
from castervoice.lib import settings  # requires nothing
settings.WSR = __name__ == "__main__"
from castervoice.lib import utilities  # requires settings
if settings.WSR:
    _wait_for_wsr_activation()
    SymbolSpecs.set_cancel_word("escape")
from castervoice.lib import control
_NEXUS = control.nexus()

from castervoice.apps import *
from castervoice.asynch import *
from castervoice.lib import context
from castervoice.lib.actions import Key
import castervoice.lib.dev.dev
from castervoice.asynch.sikuli import sikuli
from castervoice.lib import navigation
navigation.initialize_clipboard(_NEXUS)
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.dfplus.additions import IntegerRefST

from castervoice.lib.dfplus.merge.mergepair import MergeInf
from castervoice.lib.ccr import *
from castervoice.lib.ccr.recording.again import Again
from castervoice.lib.ccr.recording.bringme import bring_rule
from castervoice.lib.ccr.recording.alias import Alias
from castervoice.lib.ccr.recording import history
from castervoice.lib.dev import dev
from castervoice.lib.dfplus.hint.nodes import css
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.merge import gfilter


def change_monitor():
    if settings.SETTINGS["sikuli"]["enabled"]:
        Playback([(["monitor", "select"], 0.0)]).execute()
    else:
        print("This command requires SikuliX to be enabled in the settings file")


class MainRule(MergeRule):
    @staticmethod
    def generate_ccr_choices(nexus):
        choices = {}
        for ccr_choice in nexus.merger.global_rule_names():
            choices[ccr_choice] = ccr_choice
        return Choice("name", choices)

    @staticmethod
    def generate_sm_ccr_choices(nexus):
        choices = {}
        for ccr_choice in nexus.merger.selfmod_rule_names():
            choices[ccr_choice] = ccr_choice
        return Choice("name2", choices)

    mapping = {
        # Dragon NaturallySpeaking commands moved to dragon.py

        # hardware management
        "volume <volume_mode> [<n>]":
            R(Function(navigation.volume_control, extra={'n', 'volume_mode'}),
              rdescript="Volume Control"),
        "change monitor":
            R(Key("w-p") + Pause("100") + Function(change_monitor),
              rdescript="Change Monitor"),

        # window management
        'minimize':
            Playback([(["minimize", "window"], 0.0)]),
        'maximize':
            Playback([(["maximize", "window"], 0.0)]),
        "remax":
            R(Key("a-space/10,r/10,a-space/10,x"), rdescript="Force Maximize"),

        # passwords

        # mouse alternatives
        "legion [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="legion", nexus=_NEXUS),
              rdescript="Activate Legion"),
        "rainbow [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="rainbow", nexus=_NEXUS),
              rdescript="Activate Rainbow Grid"),
        "douglas [<monitor>]":
            R(Function(navigation.mouse_alternates, mode="douglas", nexus=_NEXUS),
              rdescript="Activate Douglas Grid"),

        # ccr de/activation
        "<enable> <name>":
            R(Function(_NEXUS.merger.global_rule_changer(), save=True),
              rdescript="Toggle CCR Module"),
        "<enable> <name2>":
            R(Function(_NEXUS.merger.selfmod_rule_changer(), save=True),
              rdescript="Toggle sm-CCR Module"),
    }
    extras = [
        IntegerRefST("n", 1, 50),
        Dictation("text"),
        Dictation("text2"),
        Dictation("text3"),
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
        Choice("volume_mode", {
            "mute": "mute",
            "up": "up",
            "down": "down"
        }),
        generate_ccr_choices.__func__(_NEXUS),
        generate_sm_ccr_choices.__func__(_NEXUS),
        IntegerRefST("monitor", 1, 10)
    ]
    defaults = {"n": 1, "nnv": 1, "text": "", "volume_mode": "setsysvolume", "enable": -1}


grammar = Grammar('general')
main_rule = MainRule()
gfilter.run_on(main_rule)
grammar.add_rule(main_rule)

gfilter.run_on(bring_rule)
grammar.add_rule(bring_rule)

if settings.SETTINGS["feature_rules"]["again"]:
    again_rule = Again(_NEXUS)
    gfilter.run_on(again_rule)
    grammar.add_rule(again_rule)

if settings.SETTINGS["feature_rules"]["alias"]:
    alias_rule = Alias(_NEXUS)
    gfilter.run_on(alias_rule)
    grammar.add_rule(alias_rule)

grammar.load()

_NEXUS.process_user_content()
_NEXUS.merger.update_config()
_NEXUS.merger.merge(MergeInf.BOOT)


print("*- Starting " + settings.SOFTWARE_NAME + " -*")

if settings.WSR:
    import pythoncom
    print("Windows Speech Recognition is garbage; it is " \
        +"recommended that you not run Caster this way. ")
    while True:
        pythoncom.PumpWaitingMessages()  # @UndefinedVariable
        time.sleep(.1)
