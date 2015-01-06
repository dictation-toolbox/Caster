import time

from dragonfly import *

from asynch import squeue
from asynch.hmc import h_launch, homunculus
from lib import utilities, settings, control
from __builtin__ import True


def navigate_to_character(direction3, target):
    # to do: possibly speed up the keypresses by figuring out how many lines up or down to go first
    try:
        left_or_right = str(direction3)
        look_left = left_or_right == "left"
        is_character = str(target) in [".", ",", "(~)", "[~]", "{~}", "(", ")", "(~[~{", "}~]~)"]
        
        # make sure nothing is highlighted to boot
        Key("right, left" if look_left else "left, right")._execute()
        
        max_highlights = 100
        index = -1
        last_copy_was_successful = True
        context = None
        for i in range(0, max_highlights):
            if last_copy_was_successful:
                if look_left:
                    Key("cs-left")._execute()
                else:
                    Key("cs-right")._execute()
                # reset success indicator
                last_copy_was_successful = True
            results = read_selected_without_altering_clipboard()
            error_code = results[0] 
            if error_code == 1:
                continue
            if error_code == 2:
                last_copy_was_successful = False
                continue
            context = results[1]
            
            index = find_index_in_context(target, context, look_left)
            if index != -1:
                break
        
        # highlight only the target
        if index != -1:
            Key("left" if look_left else "right")._execute()
            nt = index if look_left else len(context) - index - 1  # number of times to press left or right before the highlight
            if nt != 0:
                Key("right/5:" + str(nt) if look_left else "left/5:" + str(nt))._execute()
            if is_character:
                Key("s-right" if look_left else "s-left")._execute()
            else:
                Key("cs-right" if look_left else "cs-left")._execute()
        else:
            # reset cursor
            Key("left" if not look_left else "right")._execute()
            
    except Exception:
        utilities.simple_log(False)

def find_index_in_context(target, context, look_left):
    tlist = target.split("~")
    index = -1
    if look_left:
        index = -99999
        for t in tlist:
            tmpindex = context.rfind(t)  #
            if tmpindex != -1 and tmpindex > index:  # when looking left, we want the largest index
                index = tmpindex
    else:
        index = 99999  # arbitrarily large number
        for t in tlist:
            tmpindex = context.find(t)
            if tmpindex != -1 and tmpindex < index:  # conversely, when looking right, we want the smallest index
                index = tmpindex
    if index == 99999 or index == -99999:
        return -1
    return index

def read_selected_without_altering_clipboard(same_is_okay=False):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error, should not advance cursor before trying again
    '''
    time.sleep(0.05)  # time for previous keypress to execute
    cb = Clipboard(from_system=True)
    temporary = None
    prior_content = None
    try: 

        prior_content = Clipboard.get_system_text()
        Clipboard.set_system_text("")
    
        Key("c-c")._execute()
        time.sleep(0.05)  # time for keypress to execute
        temporary = Clipboard.get_system_text()
        cb.copy_to_system()

        
    except Exception:
        utilities.simple_log(False)
        return (2, None)
#     if temporary:
    if prior_content == temporary and not same_is_okay:
        return (1, None)
    return (0, temporary)

    
def fill_blanks(target):
    sequence = ["gopher", "previous", str(target).lower()]
    Playback([(sequence, 0.0)])._execute()


#--------------------------------- macro recording section =================================



class RecordedRule(CompoundRule):
    def __init__(self, commands, name=None, spec=None, extras=None,
        defaults=None, exported=None, context=None):
        CompoundRule.__init__(self, name=name, spec=spec, extras=extras, defaults=defaults, exported=exported, context=context)
        self.playback_array = []
        for command in commands:
            self.playback_array.append((command, 0.05))
            
    def _process_recognition(self, node, extras):
        Playback(self.playback_array)._execute()

def get_macro_spec():
    ''''''
    h_launch.launch(settings.QTYPE_DEFAULT)
    WaitWindow(title=settings.HOMUNCULUS_VERSION, timeout=5)._execute()
    FocusWindow(title=settings.HOMUNCULUS_VERSION)._execute()
    Key("tab")._execute()
    squeue.add_query(add_recorded_macro)

def add_recorded_macro(data):
    ''''''
    # use a response window to get a spec for the new macro: handled by calling function
    
    # search through dictation cache for "begin recording macro"
    beginning_found = False
    commands = []
    
    for i in range(0, len(control.DICTATION_CACHE)):
        d = control.DICTATION_CACHE[i]
        if not beginning_found:
            if d[0] == "begin" and d[1] == "recording":
                beginning_found = True
            continue
        
        if d[0] == "end" and d[1] == "recording":
            break
        # take every tuple after that  and turn it into a comma separated list
        commands.append(list(d))
    
    spec = data["response"]
    # clean the results
    for l in commands:
        for w in l:
            if "\\" in w:
                w = w.split("\\")[0]
    spec = spec.replace("\n", "") 
    
    # store the list in the macros section of the settings file
    recorded_macros = None
    if spec != "" and len(commands) > 0:
        recorded_macros = settings.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        recorded_macros[spec] = commands
        settings.save_json_file(recorded_macros, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    
    # immediately make a new compound rule  and add to a set grammar
    control.RECORDED_MACROS_GRAMMAR.unload()
    rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec)
    control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
    control.RECORDED_MACROS_GRAMMAR.load()
    
    # clear the dictation cache
    while len(control.DICTATION_CACHE) > 0:
        control.DICTATION_CACHE.pop()


def null_func():
    '''this function intentionally does nothing, is for use with macro recording'''

def load_recorded_rules():
    recorded_macros = settings.load_json_file(settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    for spec in recorded_macros:
        commands = recorded_macros[spec]
        rule = RecordedRule(commands=commands, spec=spec, name="recorded_rule_" + spec)
        control.RECORDED_MACROS_GRAMMAR.add_rule(rule)
    if len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        control.RECORDED_MACROS_GRAMMAR.load()

def delete_recorded_rules():
    settings.save_json_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
    control.RECORDED_MACROS_GRAMMAR.unload()
    while len(control.RECORDED_MACROS_GRAMMAR.rules) > 0:
        rule = control.RECORDED_MACROS_GRAMMAR.rules[0]
        control.RECORDED_MACROS_GRAMMAR.remove_rule(rule)


        
    
#--------------------------------- context action section =================================

class SelectiveAction(ActionBase):
    def __init__(self, action, executables, negate=True):
        '''
        action: another Dragonfly action
        executables: an array of strings, each of which is the name of an executable
        negate: if True, the action should not occur during any of the listed executables, if false the opposite
        '''
        ActionBase.__init__(self)
        self.action = action
        self.executables = executables
        self.negate = negate
        
    def _execute(self, data=None):
        executable = utilities.get_active_window_path().split("\\")[-1]
        is_executable=executable in self.executables
        if (is_executable and not self.negate) or (self.negate and not is_executable):
            self.action._execute()
        
        
        
        
        
