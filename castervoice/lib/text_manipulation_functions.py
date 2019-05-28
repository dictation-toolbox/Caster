from dragonfly import Key, Pause
import pyperclip
import re 
from castervoice.lib import context
# from castervoice.lib.ccr.core.text_manipulation import character_dict

# character_list = [text_manipulation.character_dict.values()]
character_list = [".", ",", "'", '"', "(", ")", "[", "]", "<", ">", "{", "}", "?", "!", "-", ";", ":", "|", "=", "/", 
"`", "~", "&", "%", "@", "\\", "$", "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", 
    "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"] 

def get_start_end_position(text, phrase, left_right, occurrence_number):
# def get_start_end_position(text, phrase, left_right):
    if phrase in character_list:
        pattern = re.escape(phrase)
    else:
        # avoid e.g. matching 'and' in 'land' but allow e.g. matching 'and' in 'hello.and'
        # for matching purposes use lowercase
        # PROBLEM: this will not match words in class names like "Class" in "ClassName"
        # PROBLEM: it's not matching the right one when you have two occurrences of the same word in a row
        pattern = '(?:[^A-Za-z]|\A)({})(?:[^A-Za-z]|\Z)'.format(phrase.lower()) # must get group 1

    if not re.search(pattern, text.lower()):
        # replaced phase not found
        print("'{}' not found".format(phrase))
        return
    match_iter = re.finditer(pattern, text.lower())
    if phrase in character_list: # consider changing this to if len(phrase) == 1 or something
        match_index_list = [(m.start(), m.end()) for m in match_iter] 
    else:
        match_index_list = [(m.start(1), m.end(1)) for m in match_iter] # first group
    
    if left_right == "left":
        try:
            match = match_index_list[-1*occurrence_number] # count from the right
        except IndexError:
            print("There aren't that many occurrences of '{}'".format(phrase))
            return
    if left_right == "right":
        try:
            match = match_index_list[occurrence_number - 1] # count from the left
        except IndexError:
            print("There aren't that many occurrences of '{}'".format(phrase))
            return 
    left_index, right_index = match


    return (left_index, right_index)
    # return 

def select_text_and_return_it(left_right, number_of_lines_to_search):
    # temporarily store previous clipboard item
    # temp_for_previous_clipboard_item = pyperclip.paste()
    # Pause("20").execute()
    if left_right == "left":
        # Key("s-home, s-up:%d, s-home, c-c" %number_of_lines_to_search).execute()
        Key("s-home, s-up:%d, s-home" %number_of_lines_to_search).execute()
        err, selected_text = context.read_selected_without_altering_clipboard()
        if err != 0:
            # I'm not discriminating between err = 1 and err = 2
            print("failed to copy text")
            return
    if left_right == "right":
        Key("s-end, s-down:%d, s-end" %number_of_lines_to_search).execute()
    err, selected_text = context.read_selected_without_altering_clipboard()
    if err != 0:
            # I'm not discriminating between err = 1 and err = 2
            print("failed to copy text")
            return

    Pause("70").execute()
    # return (selected_text, temp_for_previous_clipboard_item)
    return selected_text

# def deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right):
def deal_with_phrase_not_found(selected_text, cursor_behavior, left_right):
        # Approach 1: unselect text by using the arrow keys, a little faster but does not work in texstudio
        if cursor_behavior == "standard":
            if left_right == "left":
                Key("right").execute()
            if left_right == "right":
                Key("left").execute()
        # Approach 2: paste selected text over itself, sometimes a little slower but works in texstudio
        if cursor_behavior == "texstudio":
            # move cursor to the right side of selection by pasting, 
            # another way to do this in tex studio is to press left then right or vice versa
            # depending on whether you're selecting from left to right or right to left
            # Key("c-v").execute() # move cursor to the right side of selection by pasting, 
            context.paste_string_without_altering_clipboard(selected_text)
            if left_right == "right":
                Key("left:%d" %len(selected_text)).execute()
    
        # put previous clipboard item back in the clipboard
        # Pause("20").execute()
        # pyperclip.copy(temp_for_previous_clipboard_item)


def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right, occurrence_number):
# def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right):
    match_index = get_start_end_position(text, replaced_phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        return
    return text[: left_index] + replacement_phrase + text[right_index:] 
    


def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, left_right, number_of_lines_to_search, cursor_behavior, occurrence_number):
# def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, left_right, number_of_lines_to_search, cursor_behavior):
    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    replaced_phrase = str(replaced_phrase)
    replacement_phrase = str(replacement_phrase) 
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, left_right, occurrence_number)
    if not new_text:
        # replaced_phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)
        return
    
    pyperclip.copy(new_text)
    # Key("c-v").execute()
    context.paste_string_without_altering_clipboard(new_text)
    if number_of_lines_to_search < 20: 
        # only put the cursor back in the right spot if the number of lines to search is fairly small
        if left_right == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)

def remove_phrase_from_text(text, phrase, left_right, occurrence_number):
    match_index = get_start_end_position(text, phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        return
        
    # if the "phrase" is punctuation, just remove it, but otherwise remove an extra space adjacent to the phrase
    if phrase in character_list:
        return text[: left_index] + text[right_index:] 
    else:
        if left_index == 0:
            # the phrase is at the beginning of the line
            return text[right_index:]  # todo: consider removing extra space
        else:
            return text[: left_index - 1] + text[right_index:] 


def copypaste_remove_phrase_from_text(phrase, left_right, number_of_lines_to_search, cursor_behavior, occurrence_number):
    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    phrase = str(phrase)
    new_text = remove_phrase_from_text(selected_text, phrase, left_right, occurrence_number)
    if not new_text:
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)
        return 
    pyperclip.copy(new_text)
    # Key("c-v").execute()
    context.paste_string_without_altering_clipboard(new_text)

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)


def move_until_phrase(left_right, before_after, phrase, number_of_lines_to_search, cursor_behavior, occurrence_number):
    if not before_after:
          # default to whatever is closest to the cursor
        if left_right  == "left":
            before_after = "after"
        if left_right == "right":
            before_after = "before"

    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)

        return

    
    if cursor_behavior == "standard":
        # Approach 1: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
        if right_index < round(len(selected_text))/2:
            # it's faster to approach phrase from the left
            Key("left").execute() # unselect text and place cursor on the left side of selection 
            if before_after  == "before":
                offset_correction = selected_text[: left_index].count("\r\n")
                offset = left_index - offset_correction
            if before_after  == "after":
                offset_correction = selected_text[: right_index].count("\r\n")
                offset = right_index - offset_correction
            Key("right:%d" %offset).execute()
        else:
            # it's faster to approach phrase from the right
            Key("right").execute() # unselect text and place cursor on the right side of selection
            if before_after  == "before":
                offset_correction = selected_text[left_index :].count("\r\n")
                offset = len(selected_text) - left_index - offset_correction
            if before_after  == "after":
                offset_correction = selected_text[right_index :].count("\r\n")
                offset = len(selected_text) - right_index - offset_correction
            Key("left:%d" %offset).execute()
            
    if cursor_behavior == "texstudio":
    # Approach 2: paste the selected text over itself rather than simply unselecting. A little slower but works in Texstudio
    # comments below indicate the other approach
        # Key("c-v").execute()
        context.paste_string_without_altering_clipboard(selected_text)
        if before_after == "before":
            selected_text_to_the_right_of_phrase = selected_text[left_index :]    
        if before_after == "after":
            selected_text_to_the_right_of_phrase = selected_text[right_index :]
        multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
        if before_after  == "before":
            offset = len(selected_text) - left_index - multiline_offset_correction
        if before_after == "after":
            offset = len(selected_text) - right_index - multiline_offset_correction
        Key("left:%d" %offset).execute()

    # put previous clipboard item back in the clipboard (Todo: consider factoring this out)
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)

def select_phrase(phrase, left_right, number_of_lines_to_search, cursor_behavior, occurrence_number):
    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)
        return
    


    # Approach 1: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    if cursor_behavior == "standard":
        if right_index < round(len(selected_text))/2:
            # it's faster to approach phrase from the left
            Key("left").execute() # unselect text and place cursor on the left side of selection 
            multiline_movement_offset_correction = selected_text[: left_index].count("\r\n")
            movement_offset = left_index - multiline_movement_offset_correction
            # move to the left side of the phrase
            Key("right:%d" %movement_offset).execute()
            # select phrase
            multiline_selection_offset_correction = selected_text[left_index : right_index].count("\r\n")
            selection_offset = len(phrase) - multiline_selection_offset_correction
            Key("s-right:%d" %selection_offset).execute()
        else:
            # it's faster to approach phrase from the right
            Key("right").execute() # unselect text and place cursor on the right side of selection
            multiline_movement_offset_correction = selected_text[left_index :].count("\r\n")
            movement_offset = len(selected_text) -  left_index - multiline_movement_offset_correction
            # move to the left side of the phrase
            Key("left:%d" %movement_offset).execute()
            # select phrase
            multiline_selection_offset_correction = selected_text[left_index : right_index].count("\r\n")
            selection_offset = len(phrase) - multiline_selection_offset_correction
            Key("s-right:%d" %selection_offset).execute()
        
    # Approach 2: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # comments below indicate the other approach
    if cursor_behavior == "texstudio":
        # Key("c-v").execute()
        context.paste_string_without_altering_clipboard(selected_text)
        multiline_movement_correction = selected_text[right_index :].count("\r\n")
        movement_offset = len(selected_text) - right_index - multiline_movement_correction
        Key("left:%d" %movement_offset).execute()
        multiline_selection_correction = selected_text[left_index : right_index].count("\r\n")
        selection_offset = len(selected_text[left_index : right_index]) - multiline_selection_correction
        Key("s-left:%d" %selection_offset).execute()


    # put previous clipboard item back in the clipboard
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)


def select_until_phrase(left_right, phrase, before_after, number_of_lines_to_search, cursor_behavior, occurrence_number):
    
    if not before_after:
    # default to select all the way through the phrase not just up until it
        if left_right == "left":
            before_after = "before"
        if left_right == "right":
            before_after = "after"
    
    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)
        return
    
    # Approach 1: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    if cursor_behavior == "standard":
        if left_right == "left":
            Key("right").execute() # unselect text and move to left side of selection
            if before_after == "before":
                multiline_correction = selected_text[left_index :].count("\r\n")
                offset = len(selected_text) - left_index - multiline_correction
            if before_after == "after":
                multiline_correction = selected_text[right_index :].count("\r\n")
                offset = len(selected_text) - right_index - multiline_correction
            Key("s-left:%d" %offset).execute()
        if left_right == "right": 
            Key("left").execute() # unselect text and move to the right side of selection
            if before_after == "before":
                multiline_correction = selected_text[: left_index].count("\r\n")
                offset = left_index - multiline_correction
            if before_after == "after":
                multiline_correction = selected_text[: right_index].count("\r\n")
                offset = right_index - multiline_correction
            Key("s-right:%d" %offset).execute()


    # Approach 2: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    if cursor_behavior == "texstudio":
        # Key("c-v").execute()  
        context.paste_string_without_altering_clipboard(selected_text)
        if left_right == "left":
            if before_after == "before": 
                selected_text_to_the_right_of_phrase = selected_text[left_index :]    
                multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
                offset = len(selected_text) - left_index - multiline_offset_correction
                
            if before_after == "after":
                selected_text_to_the_right_of_phrase = selected_text[right_index :]
                multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
                offset = len(selected_text) - right_index - multiline_offset_correction
            
            Key("s-left:%d" %offset).execute()
        if left_right == "right":
            multiline_movement_correction = selected_text.count("\r\n")
            movement_offset = len(selected_text) - multiline_movement_correction
            
            if before_after == "before":
                multiline_selection_correction = selected_text[: left_index].count("\r\n")
                selection_offset = left_index - multiline_movement_correction
            if before_after == "after":
                multiline_selection_correction = selected_text[: right_index].count("\r\n")
                selection_offset = right_index

            # move cursor to original position
            Key("left:%d" %movement_offset).execute()
            # select text
            Key("s-right:%d" %selection_offset).execute()
        
    
    # put previous clipboard item back in the clipboard (consider factoring this out)
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)


# seems a little inconsistent
def delete_until_phrase(text, phrase, left_right, before_after, occurrence_number):
    print("selected_text {} \n").format(text)
    match_index = get_start_end_position(text, phrase, left_right, occurrence_number)
    if match_index:
        left_index, right_index = match_index
    else:
        return
    # the spacing below may need to be tweaked
    if left_right == "left":
        if before_after == "before":
            # if text[-1] == " ":
            #     return text[: left_index] + " "
                return text[: left_index]

        else: # todo: handle before-and-after defaults better
            if text[-1] == " ":
                return text[: right_index] + " "
            else:
                return text[: right_index]
    if left_right == "right":
        if before_after == "after":
            return text[right_index :]
        else:
            if text[0] == " ":
                return " " + text[left_index :]
            else:
                return text[left_index :]

def copypaste_delete_until_phrase(left_right, phrase, number_of_lines_to_search, before_after, cursor_behavior, occurrence_number):
    if not before_after:
        # default to delete all the way through the phrase not just up until it
        if left_right == "left":
            before_after = "before"
        if left_right == "right":
            before_after = "after"

    # clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    # selected_text = clip[0]
    # temp_for_previous_clipboard_item = clip[1]
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)
    phrase = str(phrase)
    new_text = delete_until_phrase(selected_text, phrase, left_right, before_after, occurrence_number)
        
    if new_text is None: 
        # do not use `if not new_text` because that will pick up the case where new_text="" which
        # occurs if the phrase is at the beginning of the line
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, cursor_behavior, left_right)
        deal_with_phrase_not_found(selected_text, cursor_behavior, left_right)
        return

    if new_text == "":
        # phrase is at the beginning of the line
        Key("del").execute()
        return
    else:
        # put modified text on the clipboard
        # pyperclip.copy(new_text)
        # Key("c-v").execute()
        context.paste_string_without_altering_clipboard(new_text)

        if left_right == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    # Pause("20").execute()
    # pyperclip.copy(temp_for_previous_clipboard_item)

