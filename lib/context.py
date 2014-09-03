import time
from dragonfly import *
import win32clipboard, sys, win32con
from lib import utilities, paths

def navigate_to_character(direction3, target):
    # to do: possibly speed up the keypresses by figuring out how many lines up or down to go first
    try:
        left_or_right = str(direction3)
        look_left = left_or_right == "left"
        up_or_down="up" if look_left else "down" 
        home_or_end="end, home, home" if look_left==False else "end"
        #if looking/going right and down, get number of presses right from beginning of line?
        # yes, that's what we want 
        
        c, n = characters_until(look_left, str(target))
        keystring=""
        if n>0:
            keystring+=up_or_down+"/5:"+str(n)+", "+home_or_end+", "
        keystring += left_or_right + "/5:" + str(c) + ", s-" + left_or_right
        Key(keystring)._execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))

def characters_until(look_left, target, max_lines=30):
    characters = 0
    index = 0  # the index in the context of the desired character or word
    new_lines = 0  # the number of new lines between the index and the cursor
#     utilities.remote_debug()
    for i in range(0, max_lines):
        if look_left:
            if i==0:#debugging point
                Key("s-home")._execute()
            else:
                Key("s-up, s-home")._execute()
        else:
            if i==0:
                Key("s-end")._execute()
            else:
                Key("s-down, s-end")._execute()
        context = read_selected_without_altering_clipboard()
        
        if context==None:
            continue# if copying the line was unsuccessful, skip it; the one in case where this can happen is if this macro is called at the end of the line
        
        if "\r\n" in context:# it has trouble with line breaks, counts them as two characters, so:
            context = context.replace("\r\n", "\n")
        
        if context.endswith("\n"):# this is so that the string.split below works
            context=context.rstrip("\n")
        
        new_lines = i#context.count("\n")
        # new way of thinking: using the arrow keys for every value of i is a default
        # therefore, the characters that get returned are only the characters for the relevant line
        # again, remember  you have to press home or end before starting to press left and right
        
        relevant_context=context.split("\n")[0 if look_left else -1]
        index = find_index_in_context(target, relevant_context, look_left)
        
        if look_left and index != -1:
            characters = len(relevant_context) - index - 1
            break
        elif look_left == False and index != -1:
            characters = index
            break
        else:
            continue
    if look_left:  # reset cursor position
        Key("right")._execute()
    else:
        Key("left")._execute()

    return (characters, new_lines)

#
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

def read_selected_without_altering_clipboard():
    # first, get whatever was in the clipboard
#     utilities.remote_debug()()()
    time.sleep(0.05)  # time for previous keypress to execute
    win32clipboard.OpenClipboard()
    prior_content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

    Key("c-c")._execute()
    time.sleep(0.05)  # time for keypress to execute

    win32clipboard.OpenClipboard()
    highlighted = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(prior_content)
    win32clipboard.CloseClipboard()
    
    if prior_content==highlighted:
        return None
    return highlighted

def jump_out(direction3, levels):
    print ""
    d = str(direction3)
    

    









        
    
