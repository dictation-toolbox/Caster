from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule,
                       Pause, Repeat, Text)
from dragonfly.actions.action_mimic import Mimic

from caster.lib import control, settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
	    "get up":                                
		    R(Key("a-up"), rdescript="RStudio: Navigate up"),
		"get back":                           
		    R(Key("a-left"), rdescript="RStudio: Navigate back"),
		"get forward":                        
		    R(Key("a-right"), rdescript="RStudio: Navigate forward"),
		"file list":                         
		    R(Key("a-d, f6, f6, f6"), rdescript="RStudio: Files list"),
		"navigation pane":                   
		    R(Key("a-d, f6, f6"), rdescript="RStudio: Navigation pane"),
		"filename":                   
		    R(Key("a-d, f6, f6, f6, f6, f6"), rdescript="RStudio: File name"),
	}
    extras = [
    ]
    defaults = {}

context = AppContext(title="save file") | AppContext(title="open file") | AppContext(title="save as")
grammar = Grammar("FileDialogue", context=context)
if settings.SETTINGS["apps"]["filedialogue"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
