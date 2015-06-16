import re
import time

from dragonfly import *

from caster.lib import utilities, control
from caster.lib.dfplus import state


def get_filter():
    from natlinkutils import GrammarBase
    class Filter(GrammarBase):
    
        # this spec will catch everything
        gramSpec = """
            <start> exported = {emptyList};
        """
    
        def initialize(self):
            self.load(self.gramSpec, allResults=1)
            self.activateAll()
    
        def gotResultsObject(self, recogType, resObj):
            for x in range(0, 100):
                try:
                    possible_interpretation = resObj.getWords(x)
                    # do whatever sort of filtering you want here
                except Exception:
                    break
    return Filter()

def navigate_to_character(direction3, target):
    # to do: possibly speed up the keypresses by figuring out how many lines up or down to go first
    try:
        left_or_right = str(direction3)
        look_left = left_or_right == "left"
        is_character = False
        for s in target.split("~"):
            if s in ".,()[]{}<>":
                is_character=True
                break
        
        # make sure nothing is highlighted to boot
        Key("right, left" if look_left else "left, right")._execute()
        if look_left:
            Key("cs-left")._execute()
        else:
            Key("cs-right")._execute()
#         max_highlights = 100
        index = -1
#         last_copy_was_successful = True
        context = None
        tries=0
        while context==None:
            tries+=1
            results = read_selected_without_altering_clipboard()
            error_code = results[0]
            if error_code==0:
                context = results[1]
                break
            if tries>5:
                return False
        
        # if we got to this point, we have a copy result, 
#         print "have copy result: "+context
        index = find_index_in_context(target, context, look_left)
        
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
#             print "success"
            return True
        else:
            # reset cursor
            Key("left" if look_left else "right")._execute()
            return False
            
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
    
    if prior_content == temporary and not same_is_okay:
        return (1, None)
    return (0, temporary)


def fill_within_line(target):
    result = navigate_to_character("left", str(target))
    if result:
        control.nexus().state.halt_asynchronous(True)  # @UndefinedVariable
    return result
        
def nav(parameters):
    result = navigate_to_character(str(parameters[0]), str(parameters[1]))
    if result:
        Key(str(parameters[0]))._execute()
    return result