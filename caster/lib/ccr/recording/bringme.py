import os
import threading
import logging
import time
from dragonfly import Choice, Function, Dictation, Text

from caster.lib import control, context, utilities, settings
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.short import R

CONFIG = utilities.load_json_file(settings.SETTINGS["paths"]["BRINGME_PATH"])
if not CONFIG:
    CONFIG = utilities.load_json_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
    
def refresh():
    bring_rule.refresh()

#module functions
def bring_it(item):
    '''
    Currently simply invoke os.startfile. New thread keeps Dragon from crashing. 
    '''
    threading.Thread(target=os.startfile, args=(item,)).start()

def bring_add(launch, key):
    '''
    Add current program or highlighted text to bring me
    '''
    if launch=="program":
        path = utilities.get_active_window_path()
    else:
        fail, path = context.read_selected_without_altering_clipboard()
        if fail == 2:
            #FIXME
            time.sleep(0.1)
            _, path = context.read_selected_without_altering_clipboard()
    if not path:
        #logger.warn('Cannot add %s to bringme: cannot read selected', launch)
        return
    CONFIG[str(key)] = path
    utilities.save_json_file(CONFIG, settings.SETTINGS["paths"]["BRINGME_PATH"])
    refresh()

def bring_remove(key):
    '''
    Remove item from bring me
    '''
    key = str(key)
    if key in CONFIG:
        del CONFIG[key]
        utilities.save_json_file(CONFIG, settings.SETTINGS["paths"]["BRINGME_PATH"])
        refresh()
    else:
        #logger.debug('No item %s in bringme', key)
        return
        
def bring_restore():
    '''
    Restore bring me list to defaults
    '''
    global CONFIG
    CONFIG = utilities.load_json_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
    refresh()

def _rebuild_items():
    #logger.debug('Bring me rebuilding extras')
    return {key: os.path.expandvars(value) for key, value in CONFIG.iteritems()}

class BringRule(SelfModifyingRule):

    pronunciation = "bring me"
    
    def refresh(self, *args):
        #logger.debug('Bring me refresh')
        self.extras[0] = Choice('item', _rebuild_items())
        self.reset(self.mapping)

    mapping = {
       "bring me <item>":
            R(Function(bring_it), rdescript="Launch preconfigured program, folder or website"),
       "<launch> to bring me as <key>":
            R(Function(bring_add), rdescript="Add program, folder or website to the bring me list"),
       "remove <key> from bring me":
            R(Function(bring_remove), rdescript="Remove program, folder or website from the bring me list"),
       "restore bring me defaults":
            R(Function(bring_restore), rdescript="Delete bring me list and put defaults in its place"),
    }
    
    extras = [
        Choice("item", _rebuild_items()),
        Choice("launch", {
            "[current] program": "program",
            "website": "website",
            "folder": "folder",
        }),
        Dictation("key"),
    ]

    defaults = { 'item': '', 'launch': 'program', 'key': ''}

bring_rule = BringRule()
#Does not work
#control.nexus().merger.add_selfmodrule(bring_rule)

