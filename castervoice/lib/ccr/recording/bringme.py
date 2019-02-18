import os
import threading
import subprocess
import time
import shlex
# import dragonfly
from dragonfly import Choice, Function, Dictation

from castervoice.lib import control, context, utilities, settings
from castervoice.lib.actions import Text, Key
from castervoice.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from castervoice.lib.dfplus.state.short import R

CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_PATH"])
if not CONFIG:
    CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
if not CONFIG:
    # logger.warn("Could not load bringme defaults")
    print("Could not load bringme defaults")
    
def refresh():
    bring_rule.refresh()

#module functions
def bring_it(desired_item):
    '''
    Currently simply invoke os.startfile. New thread keeps Dragon from crashing. 
    '''
    item, item_type = desired_item
    if item_type == "website":
        browser = utilities.default_browser_command()
        subprocess.Popen(shlex.split(browser.replace('%1', item)))
    elif item_type == 'folder':
        subprocess.Popen([r'C:\Windows\explorer.exe', item])
    elif item_type == 'program':
        subprocess.Popen(item)
    else:    
        threading.Thread(target=os.startfile, args=(item,)).start()

def bring_add(launch, key):
    '''
    Add current program or highlighted text to bring me
    '''
    key = str(key)
    if launch == "program":
        path = utilities.get_active_window_path()
        if not path:
            # dragonfly.get_engine().speak("program not detected")
            print("Program path for bring me not found ")
    # elif launch == 'file':
    # no way to add file via pyperclip
    else:
        Key("a-d/5").execute()
        fail, path = context.read_selected_without_altering_clipboard()
        if fail == 2:
            #FIXME
            time.sleep(0.1)
            _, path = context.read_selected_without_altering_clipboard()
            if not path:
                # dragonfly.get_engine().speak("nothing selected")
                print("Selection for bring me not found ")
        Key("escape").execute()
    if not path:
        #logger.warn('Cannot add %s as %s to bringme: cannot get path', launch, key)
        return
    CONFIG[launch][key] = path
    utilities.save_toml_file(CONFIG, settings.SETTINGS["paths"]["BRINGME_PATH"])
    refresh()

def bring_remove(key):
    '''
    Remove item from bring me
    '''
    key = str(key)
    for section in CONFIG.keys():
        if key in CONFIG[section]:
            del CONFIG[section][key]
            utilities.save_toml_file(CONFIG, settings.SETTINGS["paths"]["BRINGME_PATH"])
            refresh()
            return
        
def bring_restore():
    '''
    Restore bring me list to defaults
    '''
    global CONFIG
    CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
    refresh()

def _rebuild_items():
    #logger.debug('Bring me rebuilding extras')
    return {key: (os.path.expandvars(value), header) for header, section in CONFIG.iteritems() 
        for key, value in section.iteritems()}

class BringRule(SelfModifyingRule):

    pronunciation = "bring me"
    
    def refresh(self, *args):
        #logger.debug('Bring me refresh')
        self.extras[0] = Choice('desired_item', _rebuild_items())
        self.reset(self.mapping)

    mapping = {
       "bring me <desired_item>":
            R(Function(bring_it), rdescript="Launch preconfigured program, folder or website"),
       "<launch> to bring me as <key>":
            R(Function(bring_add, extra={"launch", "key"}), rdescript="Add program, folder or website to the bring me list"),
       "remove <key> from bring me":
            R(Function(bring_remove, extra="key"), rdescript="Remove program, folder or website from the bring me list"),
       "restore bring me defaults":
            R(Function(bring_restore), rdescript="Delete bring me list and put defaults in its place"),
    }
    
    extras = [
        Choice("desired_item", _rebuild_items()),
        Choice("launch", {
            "[current] program": "program",
            "website": "website",
            "folder": "folder",
            "file": "file",
        }),
        Dictation("key"),
    ]

    defaults = { 'desired_item': ('', ""), 'launch': 'program', 'key': ''}

bring_rule = BringRule()
#Does not work
#control.nexus().merger.add_selfmodrule(bring_rule)

