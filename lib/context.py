import time
from dragonfly import *
import win32clipboard,sys,win32con
from lib import utilities, paths


def read_selected_without_altering_clipboard():
    # first, get whatever was in the clipboard
#     utilities.remote_debug()
    time.sleep(0.05) # time for previous keypress to execute
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
    
    return highlighted

def characters_until(look_left, target, max_lines=30):
    characters = 0
    for i in range(0, max_lines):
        if look_left:
            Key("s-up")._execute()
        else:
            Key("s-down")._execute()
        context = read_selected_without_altering_clipboard()
        # it has trouble with line breaks, counts them as two characters, so:
        if "\r\n" in context:
            context = context.replace("\r\n", "\n")
        index=find_index_in_context(target, context, look_left)
        print " index: "+str(index) +" context:\n"+context+"\nlen(context): "+str(len(context))+" characters: "+ str(len(context) - index - 1)
        if look_left and index!=-1:
            characters = len(context) - index - 1
            break
        elif look_left==False and index!=-1:
            characters = index
            break
        else:
            continue
    if look_left:  # reset cursor position
        Key("right")._execute()
    else:
        Key("left")._execute()

    return characters

#
def find_index_in_context(target, context, look_left):
    tlist=list(target)
    index=-1
    if look_left:
        index=0
        #tlist=tlist[::-1]# reverse the list, useful in case we are looking at brackets or parentheses# commented out because we don't care about preference
        for t in tlist:
            tmpindex=context.rfind(t)#
            if tmpindex!=-1 and tmpindex>index:# when looking left, we want the largest index
                index=tmpindex
    else:
        index=99999# arbitrarily large number
        for t in tlist:
            tmpindex=context.find(t)
            if tmpindex!=-1 and tmpindex<index:# conversely, when looking right, we want the smallest index
                index=tmpindex
    if index==99999 or index==0:
        return -1
    return index
    
def jump_out(direction3, levels):
    print ""
    d = str(direction3)
    
def navigate_to_character(direction3, target):
    # to do: possibly speed up the keypresses by figuring out how many lines up or down to go first
    try:
        key_to_press = str(direction3)
        look_left = key_to_press == "left"
        c = characters_until(look_left, str(target))
        keystring=key_to_press + "/5:" + str(c) + ", s-" + key_to_press
        Key(keystring)._execute()
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    









        
    
