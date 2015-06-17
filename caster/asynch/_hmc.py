from dragonfly import (Function, Grammar, IntegerRef, Dictation, MappingRule, AppContext, Choice)

from caster.lib import  settings, control
from caster.lib.dfplus.state.short import R


def kill():
    control.nexus().comm.get_com("hmc").kill()

def complete():
    control.nexus().comm.get_com("hmc").complete()

def hmc_checkbox(n):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    control.nexus().comm.get_com("hmc").do_action("check", [int(n)])

def hmc_focus(field):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    control.nexus().comm.get_com("hmc").do_action("focus", str(field))

def hmc_recording_check_range(n, n2):
    control.nexus().comm.get_com("hmc").do_action("check_range", [int(n), int(n2)])

def hmc_recording_exclude(n):
    control.nexus().comm.get_com("hmc").do_action("exclude", int(n))
    
def hmc_recording_repeatable():
    control.nexus().comm.get_com("hmc").do_action("repeatable")

def hmc_directory_browse():
    control.nexus().comm.get_com("hmc").do_action("dir")

class HMCRule(MappingRule):
    mapping = {
        "kill homunculus":              R(Function(kill), rdescript="Kill Helper Window"),
        "complete":                     R(Function(complete), rdescript="Complete Input"),
        "check <n>":                    R(Function(hmc_checkbox, extra="n"), rdescript="Check Checkbox"),
        "focus <field> [box]":          R(Function(hmc_focus, extra="field"), rdescript="Focus Field"),
        # specific to macro recorder
        "check from <n> to <n2>":       R(Function(hmc_recording_check_range, extra={"n", "n2"}), rdescript="Check Range"),
        "exclude <n>":                  R(Function(hmc_recording_exclude, extra="n"), rdescript="Uncheck Checkbox"),
        "[make] repeatable":            R(Function(hmc_recording_repeatable), rdescript="Make Macro Repeatable"),
        # specific to your directory browser
        "browse":                       R(Function(hmc_directory_browse), rdescript="Browse Computer"),
    }   
    extras = [
              IntegerRef("n", 1, 25),
              IntegerRef("n2", 1, 25),
              Choice("field",
                    {"vocabulary": "vocabulary", "word": "word"
                    }),
             ]
    defaults = {
               
               }


c = AppContext(title=settings.HOMUNCULUS_VERSION)
grammar = Grammar("hmc", context=c)
grammar.add_rule(HMCRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
