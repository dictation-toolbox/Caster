import time
import sys

from dragonfly import AppContext, Pause

from castervoice.lib import utilities, settings
from castervoice.lib.actions import Key
from castervoice.lib.clipboard import Clipboard

# Override dragonfly.AppContext with aenea.ProxyAppContext if the 'use_aenea'
# setting is set to true.
if settings.settings(["miscellaneous", "use_aenea"]):
    try:
        from aenea import ProxyAppContext as AppContext
    except ImportError:
        print("Unable to import aenea.ProxyAppContext. dragonfly.AppContext "
              "will be used instead.")


def _target_is_character(target):
    '''determines if the target is a single character'''
    if len(target) == 1:
        return True
    '''if the character is in the character group:'''
    for s in target.split("~"):
        if s in ".,()[]{}<>":
            return True
    return False


def _find_index_in_context(target, context, look_left):
    '''attempts to find index of target in clipboard content'''
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


def navigate_to_character(direction3, target, fill=False):
    try:
        look_left = str(direction3) == "left"

        # make sure nothing is highlighted to boot
        if not fill:  # (except when doing "fill" -- if at end of line, there is no space for this )
            Key("right, left" if look_left else "left, right").execute()
        if look_left:
            Key("cs-left").execute()
        else:
            Key("cs-right").execute()

        context = read_nmax_tries(5, .01)
        if context is None:
            return False

        # if we got to this point, we have a copy result
        index = _find_index_in_context(target, context, look_left)

        if index != -1:  # target found
            '''move the cursor to the left of the target if looking left,
            to the right of the target if looking right:'''
            Key("left" if look_left else "right").execute()
            '''number of times to press left or right before the highlight
            (the target may be a part of a fully highlighted word): '''
            nt = index if look_left else len(context) - index - 1 # pylint: disable=no-member
            if nt != 0:
                Key("right/5:" + str(nt) if look_left else "left/5:" + str(nt)).execute()
            '''highlight only the target'''
            if _target_is_character(target):
                Key("s-right" if look_left else "s-left").execute()
            else:
                Key("cs-right" if look_left else "cs-left").execute()
            return True
        else:
            # reset cursor
            Key("left" if look_left else "right").execute()
            return False

    except Exception:
        utilities.simple_log()


def read_nmax_tries(n, slp=0.1):
    tries = 0
    while True:
        tries += 1
        results = read_selected_without_altering_clipboard()
        error_code = results[0]
        if error_code == 0:
            return results[1]
        if tries > n:
            return None
        time.sleep(slp)


def read_selected_without_altering_clipboard(same_is_okay=False, cb_timeout=0.200, pause_time="0", key_override=None):
    '''Returns selected item from temporary clipboard buffer.

    Args:
        same_is_okay (bool, optional): Initial clipboard contents is same as copied contents. Defaults to False.
        cb_timeout (int, optional): Timeout monitoring for clipboard change.
            - Windows OS increments clipboard contents, other OS's comparing clipboard contents
        pause_time (str, optional): Keypress delay. Defaults to 0 ms.
            - Allows foreground window to process key events
        key_override (str, optional): Override platform copy key spec. Defaults to None.
            - Allows non-standard key specs to invoke copy action

    Returns tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''
    if key_override is None:
        _default_copy_spec = "w-c/20" if sys.platform == "darwin" else "c-c/20"
    else:
        _default_copy_spec = key_override

    original_cb = Clipboard(from_system=True)
    new_cb = Clipboard(from_system=True)
    try:
        with Clipboard.synchronized_changes(cb_timeout, initial_clipboard=original_cb):
            Key(_default_copy_spec, use_hardware=True).execute()
        Pause(pause_time).execute()
        new_cb.copy_from_system()
    except Exception as e:
        print(e)
        return (2, None)
    original_cb.copy_to_system()
    if original_cb == new_cb and not same_is_okay:
        return (1, None)
    else:
        return(0, new_cb.get_text())


def paste_string_without_altering_clipboard(content, cb_timeout=0.200, pause_time="1", key_override=None):
    '''Paste content from temporary clipboard buffer.
    Args:
        content (str): content to insert into clipboard buffer.
        cb_timeout (int, optional): timeout monitoring for clipboard change
            - Windows OS increments clipboard contents, other OS's comparing clipboard contents
        pause_time (str, optional): Keypress delay. Defaults to 1.
            - Allows foreground window to process key events
        key_override (str, optional): Override platform paste key spec. Defaults to None.
            - Allows non-standard key specs to invoke paste action

    Returns bool:
    True - indicates success
    False - indicates clipboard error
    '''
    
    if key_override is None:
        _default_paste_spec = "w-v/20" if sys.platform == "darwin" else "c-v/20"
    else:
        _default_paste_spec = key_override
        

    cb = Clipboard(from_system=True)
    try:
        with cb.synchronized_changes(cb_timeout):
            Clipboard.set_system_text(content)
        Key(_default_paste_spec, use_hardware=True).execute()
        Pause(pause_time).execute()
    except Exception as e:
        print(e)
        return False    
    cb.copy_to_system()
    return True

def fill_within_line(target):
    result = navigate_to_character("left", str(target), True)
    if result:
        from castervoice.lib import control
        control.nexus().state.terminate_asynchronous(success=True)
    return result


def nav(parameters):
    result = navigate_to_character(str(parameters[0]), str(parameters[1]))
    if result:
        Key(str(parameters[0])).execute()
    return result
