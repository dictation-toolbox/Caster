import os
import threading
import logging
import time
from dragonfly import Grammar, Choice, Function, Dictation, Text

from caster.lib import control, context, utilities, settings
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.short import R

config = utilities.load_json_file(settings.SETTINGS["paths"]["BRINGME_PATH"])

def reload():
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
        #logger.warn('Cannot add %s to bringme: cannot read selected' % launch)
        return
    config[str(key)] = path
    utilities.save_json_file(config, settings.SETTINGS["paths"]["BRINGME_PATH"])
    reload()

def bring_remove(key):
    '''
    Remove item from bring me
    '''
    key = str(key)
    if key in config:
        del config[key]
        utilities.save_json_file(config, settings.SETTINGS["paths"]["BRINGME_PATH"])
        reload()
    else:
        #logger.debug('No item %s in bringme' % key)
        return

def _rebuild_items():
    #logger.debug('Bring me rebuilding extras')
    return {key: os.path.expandvars(value) for key, value in config.iteritems()}

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
            R(Function(bring_add), rdescript="Launch preconfigured program, folder or website"),
       "remove <key> from bring me":
            R(Function(bring_remove), rdescript="Launch preconfigured program, folder or website"),
       "Bring me test":
            R(Text("Test works"), rdescript="Bring me test"),
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
control.nexus().merger.add_selfmodrule(bring_rule)

