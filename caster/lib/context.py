import time

from dragonfly import *

from caster.lib import utilities, settings


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
            nt = index if look_left else len(context) - index - 1
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


def read_selected_without_altering_clipboard(same_is_okay=False):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''
    time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/
               1000.)  # time for previous keypress to execute
    cb = Clipboard(from_system=True)
    temporary = None
    prior_content = None
    try:

        prior_content = Clipboard.get_system_text()
        Clipboard.set_system_text("")

        Key("c-c").execute()
        time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/
                   1000.)  # time for keypress to execute
        temporary = Clipboard.get_system_text()
        cb.copy_to_system()

    except Exception:
        utilities.simple_log(False)
        return 2, None
    if prior_content == temporary and not same_is_okay:
        return 1, None
    return 0, temporary


def paste_string_without_altering_clipboard(content):
    '''
    True - indicates success
    False - indicates clipboard error
    '''
    time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/
               1000.)  # time for previous keypress to execute
    cb = Clipboard(from_system=True)

    try:
        Clipboard.set_system_text(str(content))

        Key("c-v").execute()
        time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/
                   1000.)  # time for keypress to execute
        cb.copy_to_system()

    except Exception:
        utilities.simple_log(False)
        return False
    return True


def fill_within_line(target, nexus):
    result = navigate_to_character("left", str(target), True)
    if result:
        nexus.state.terminate_asynchronous(True)
    return result


def nav(parameters):
    result = navigate_to_character(str(parameters[0]), str(parameters[1]))
    if result:
        Key(str(parameters[0])).execute()
    return result