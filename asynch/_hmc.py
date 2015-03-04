import xmlrpclib

from dragonfly import (Function, Grammar, IntegerRef, Dictation, MappingRule, AppContext, Choice)

from lib import  settings


def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.HMC_LISTENING_PORT))

def kill():
    communicate().kill()

def complete():
    communicate().complete()

def hmc_checkbox(n):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    communicate().do_action("check", [int(n)])

def hmc_focus(field):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    communicate().do_action("focus", str(field))

def hmc_recording_check_range(n, n2):
    communicate().do_action("check_range", [int(n), int(n2)])

def hmc_recording_exclude(n):
    communicate().do_action("exclude", int(n))
    
def hmc_recording_repeatable():
    communicate().do_action("repeatable")

def hmc_directory_browse():
    communicate().do_action("dir")

class HMCRule(MappingRule):
    mapping = {
        "kill homunculus":              Function(kill),
        "complete":                     Function(complete),
        "check <n>":                    Function(hmc_checkbox, extra="n"),
        "focus <field> [box]":          Function(hmc_focus, extra="field"),
        # specific to macro recorder
        "check from <n> to <n2>":       Function(hmc_recording_check_range, extra={"n", "n2"}),
        "exclude <n>":                  Function(hmc_recording_exclude, extra="n"),
        "[make] repeatable":            Function(hmc_recording_repeatable),
        # specific to your directory browser
        "browse":                       Function(hmc_directory_browse),
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
