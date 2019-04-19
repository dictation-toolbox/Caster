import pyperclip
from dragonfly import (Grammar, MappingRule, Dictation, IntegerRef,
                       Repeat, Pause, Function, Choice, AppContext)

from castervoice.lib import control, context, utilities, settings
from castervoice.lib.context import paste_string_without_altering_clipboard
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
if not CONFIG:import pyperclip

# note that the tab structure of Windows Explorer window is slightly different than 
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
    Key("c-l/20").execute()
    # Attempt to paste enclosed text without altering clipboard
    if not paste_string_without_altering_clipboard(folder_path):
        print("failed to paste {}".format(folder_path))
    # the paste without altering the clipboard seems a bit inconsistent for me though it's working now
    # if it's not working properly, here's an alternative method that does alter the clipboard
        # pyperclip.copy(folder_path)
        # Pause("5").execute()
        # Key("c-v/30").execute()
    Pause("10").execute()
    # note that the tab structure of of Windows Explorer window is slightly different than 
    # that of Windows Explorer dialogbox (aka child window)
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
        "bring me <folder_path>":
            R(Function(explorer_bring_it),
            rdescript="go to preconfigured folder within currently open Windows Explorer main window"),
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
