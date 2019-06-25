
from dragonfly import (Grammar, MappingRule, Dictation, IntegerRef,
                       Repeat, Pause, Function, Choice)

from castervoice.lib import control, context, utilities, settings
from castervoice.lib.context import AppContext
from castervoice.lib import settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.actions import (Key, Text)

# note that the tab structure of Windows Explorer main window is slightly different than 
# that of Windows Explorer dialogbox (aka child window)
# this file is only for Windows Explorer main window.


# bring me dependencies
CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_PATH"])
if not CONFIG:
    CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
if not CONFIG:
    # logger.warn("Could not load bringme defaults")
    print("Could not load bringme defaults")
    

def explorer_bring_it(folder_path):
    Key("c-l/5").execute()
    Text("{}".format(folder_path)).execute()
    Key("enter/20, a-d/5, tab:3").execute() 

class IERule(MergeRule):
    pronunciation = "explorer"

    mapping = {
        "address bar":
            R(Key("a-d"), rdescript="Explorer: Address Bar"),
        "new folder":
            R(Key("cs-n"), rdescript="Explorer: New Folder"),
        "new file":
            R(Key("a-f, w, t"), rdescript="Explorer: New File"),
        "(show | file | folder) properties":
            R(Key("a-enter"), rdescript="Explorer: Properties Dialog"),
        "get up":                            
            R(Key("a-up"), rdescript="Explorer: Navigate up"),
        "get back":
            R(Key("a-left"), rdescript="Explorer: Navigate back"),
        "get forward":
            R(Key("a-right"), rdescript="Explorer: Navigate forward"),
  
        "search [<text>]":
            R(Key("a-d, tab:1") + Text("%(text)s"), rdescript="Explorer: Search"),
        "(navigation | nav | left) pane":
            R(Key("a-d, tab:2"), rdescript="Explorer: navigation pane"),
        "(center pane | (file | folder) (pane | list))":
            R(Key("a-d, tab:3"), rdescript="Explorer: Center Pane"),
            # for the sort command below,
            # once you've selected the relevant heading for sorting using the arrow keys, press enter
        "sort [headings]":
            R(Key("a-d, tab:4"), rdescript="Explorer: Sort headings e.g. name, date, etc."),
        
            # if you just say "bring me", it will open the folder in a new window.
            # if you say "(explorer|explore|same) bring me", it will open the folder in the same window
            "(explorer|explore|same) bring me <folder_path>":
            R(Function(explorer_bring_it),
            rdescript="Explorer: Go to preconfigured folder within currently open Windows Explorer main window"),
        
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        Choice("folder_path", CONFIG["folder"]),
        ]
    
    defaults = {"n": 1}


#---------------------------------------------------------------------------

context = AppContext(executable="explorer")
grammar = Grammar("Windows Explorer", context=context)

if settings.SETTINGS["apps"]["explorer"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(IERule())
    else:
        rule = IERule(name="explorer")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
