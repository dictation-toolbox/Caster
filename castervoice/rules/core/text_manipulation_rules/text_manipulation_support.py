import re
from dragonfly import Window
from castervoice.lib.context import AppContext
from castervoice.lib import context
from castervoice.lib.actions import Key

contexts = {
    "texstudio": AppContext(executable="texstudio"),
    "lyx": AppContext(executable="lyx"),
    "winword": AppContext(executable="winword")
}


def get_application():
    window = Window.get_foreground()
    # Check all contexts. Return the name of the first one that matches or
    # "standard" if none matched.
    for name, context in contexts.items():
        if context.matches(window.executable, window.title, window.handle):
            return name
    return "standard"


def get_start_end_position(text, phrase, direction, occurrence_number, dictation_versus_character):
    # def get_start_end_position(text, phrase, direction):
    if dictation_versus_character == "character":
        pattern = re.escape(phrase)
    if dictation_versus_character == "dictation":
        # avoid e.g. matching 'and' in 'land' but allow e.g. matching 'and' in 'hello.and'
        # for matching purposes use lowercase
        # PROBLEM: this will not match words in class names like "Class" in "ClassName"
        # PROBLEM: it's not matching the right one when you have two occurrences of the same word in a row
        pattern = r'(?:[^A-Za-z]|\A)({})(?:[^A-Za-z]|\Z)'.format(phrase.lower()) # must get group 1

    if not re.search(pattern, text.lower()):
        # replaced phase not found
        print("'{}' not found".format(phrase))
        return
    match_iter = re.finditer(pattern, text.lower())
    if dictation_versus_character == "character":
        match_index_list = [(m.start(), m.end()) for m in match_iter] 
    if dictation_versus_character == "dictation":
        match_index_list = [(m.start(1), m.end(1)) for m in match_iter] # first group
    
    if direction == "left":
        try:
            match = match_index_list[-1*occurrence_number] # count from the right
        except IndexError:
            print("There aren't that many occurrences of '{}'".format(phrase))
            return
    if direction == "right":
        try:
            match = match_index_list[occurrence_number - 1] # count from the left
        except IndexError:
            print("There aren't that many occurrences of '{}'".format(phrase))
            return 
    left_index, right_index = match
    return (left_index, right_index)


copy_pause_time_dict = {"standard": "10", "texstudio": "70", "lyx": "60", "winword": "90"}
paste_pause_time_dict = {"standard": "0", "texstudio": "100", "lyx": "20", "winword": "20"} 
# winword (a.k.a. Microsoft Word) pause times may need some tweaking, 
# people are probably better off just using the native Dragon commands in winword.


def text_manipulation_copy(application):
    """ the wait time can also be modified up or down further by going into context.read_selected_without_altering_clipboard 
    and changing the sleep time which is apparently slightly different than the pause time.
    the sleep time is set to a positive number, so can be reduced
    here I am using "wait time" to mean the sum of the sleep and pause time right after pressing control c """
    # double hashmarks below indicate an alternative to using the functions in lib.context
    ## previous_item_on_the_clipboard = pyperclip.paste()
    ## Key("c-c").execute()
    ## Pause(copy_pause_time_dict[application]).execute()
    ## selected_text = pyperclip.paste()
    
    err, selected_text = context.read_selected_without_altering_clipboard(same_is_okay=True, pause_time=copy_pause_time_dict[application])
    if err != 0:
        # I'm not discriminating between err = 1 and err = 2
        print("failed to copy text")
        return
    return selected_text
    ## pyperclip.copy(previous_item_on_the_clipboard) 


def text_manipulation_paste(text, application):
    context.paste_string_without_altering_clipboard(text, pause_time=copy_pause_time_dict[application])


def select_text_and_return_it(direction, number_of_lines_to_search, application):
    if direction == "left":
        if number_of_lines_to_search > 0:
            Key("s-up:%d" %number_of_lines_to_search).execute()
        Key("s-home").execute()
    if direction == "right":    
        if number_of_lines_to_search > 0:
            Key("s-down:%d" %number_of_lines_to_search).execute()
        Key("s-end").execute()
        
    selected_text = text_manipulation_copy(application)
    if selected_text == None:
        # failed to copy
        return 
    if selected_text == "":
        print("no text to select")
        return 
    
    return selected_text


def deal_with_phrase_not_found(selected_text, application, direction):
        # Approach 1: unselect text by pressing left and then right, works in Tex studio
        if application == "texstudio":
            Key("left, right").execute() # unselect text
            if direction == "right":
                Key("left:%d" %len(selected_text)).execute()
        # Approach 2: unselect text by pressing opposite arrow key, does not work in Tex studio
        else:
            if direction == "left":
                Key("right").execute()
            if direction == "right":
                Key("left").execute()


def deal_with_up_down_directions(direction, number_of_lines_to_search):
    # note that zero is the default number of lines to search, so if you change that you will may want to change this
    if number_of_lines_to_search == 0 and (direction == "up" or direction == "down"):
        # if the user says sauce (meeting up) or dunce (meaning down), set default number of lines to 3
        number_of_lines_to_search = 3
    if direction == "up":
        direction = "left"
    if direction == "down":    
        direction = "right"
    return (number_of_lines_to_search, direction)


def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, direction, occurrence_number, dictation_versus_character):
    match_index = get_start_end_position(text, replaced_phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        return
    return text[: left_index] + replacement_phrase + text[right_index:] 
    

def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, direction, number_of_lines_to_search, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        # "up" and "down" get treated just as the "left" and "right" 
        # except that the default number of lines to search get set to three instead of zero
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    replaced_phrase = str(replaced_phrase)
    replacement_phrase = str(replacement_phrase) 
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, direction, occurrence_number, dictation_versus_character)
    if not new_text:
        # replaced_phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return
    
    text_manipulation_paste(new_text, application)
    if number_of_lines_to_search < 20: 
        # only put the cursor back in the right spot if the number of lines to search is fairly small
        if direction == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()


def copypaste_change_phrase_capitalization(phrase, direction, number_of_lines_to_search, occurrence_number, letter_size, dictation_versus_character):
    if direction == "up" or direction == "down":
        # "up" and "down" get treated just as the "left" and "right" 
        # except that the default number of lines to search get set to three instead of zero
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    replaced_phrase = phrase
    if letter_size == "lower":
        replacement_phrase = phrase[0].lower()
    else:
        replacement_phrase = phrase[0].upper()
    replacement_phrase += phrase[1:]
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, direction, occurrence_number, dictation_versus_character)
    if not new_text:
        # replaced_phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return
    
    text_manipulation_paste(new_text, application)
    if number_of_lines_to_search < 20: 
        # only put the cursor back in the right spot if the number of lines to search is fairly small
        if direction == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()



def remove_phrase_from_text(text, phrase, direction, occurrence_number, dictation_versus_character):
    match_index = get_start_end_position(text, phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        return
        
    # if the "phrase" is punctuation, just remove it, but otherwise remove an extra space adjacent to the phrase
    if dictation_versus_character == "character":
        return text[: left_index] + text[right_index:] 
    else:
        if left_index == 0:
            # the phrase is at the beginning of the line
            return text[right_index:]  # todo: consider removing extra space
        elif text[left_index - 1] == " ":
            return text[: left_index - 1] + text[right_index:]
        else:
            return text[: left_index] + text[right_index:]


def copypaste_remove_phrase_from_text(phrase, direction, number_of_lines_to_search, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    phrase = str(phrase)
    new_text = remove_phrase_from_text(selected_text, phrase, direction, occurrence_number, dictation_versus_character)
    if not new_text:
        # phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return 
    
    text_manipulation_paste(new_text, application)

    if direction == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()


def delete_until_phrase(text, phrase, direction, before_after, occurrence_number, dictation_versus_character):
    match_index = get_start_end_position(text, phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        return
    # the spacing below may need to be tweaked
    if direction == "left":
        if before_after == "before":
            # if text[-1] == " ":
            #     return text[: left_index] + " "
                return text[: left_index]

        else: # TODO: handle before-and-after defaults better
            if text[-1] == " ":
                return text[: right_index] + " "
            else:
                return text[: right_index]
    if direction == "right":
        if before_after == "after":
            return text[right_index :]
        else:
            if text[0] == " ":
                return " " + text[left_index :]
            else:
                return text[left_index :]


def copypaste_delete_until_phrase(direction, phrase, number_of_lines_to_search, before_after, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()  
    if not before_after:
        # default to delete all the way through the phrase not just up until it
        if direction == "left":
            before_after = "before"
        if direction == "right":
            before_after = "after"

    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    phrase = str(phrase)
    new_text = delete_until_phrase(selected_text, phrase, direction, before_after, occurrence_number, dictation_versus_character)
        
    if new_text is None: 
        # do NOT use `if not new_text` because that will pick up the case where new_text="" which
        # occurs if the phrase is at the beginning of the line
        # phrase not found
        # deal_with_phrase_not_found(selected_text, temp_for_previous_clipboard_item, application, direction)
        deal_with_phrase_not_found(selected_text, application, direction)
        return

    if new_text == "":
        # phrase is at the beginning of the line
        Key("del").execute()
        return
    else:
        text_manipulation_paste(new_text, application)

        if direction == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()


def move_until_phrase(direction, before_after, phrase, number_of_lines_to_search, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()
    if not before_after:
          # default to whatever is closest to the cursor
        if direction  == "left":
            before_after = "after"
        if direction == "right":
            before_after = "before"
    
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return
              
    if application == "texstudio":
    # Approach 1: Unselect text by pressing left and then right. A little slower but works in Texstudio
        Key("left, right").execute() # unselect text
        if direction == "left":
            # cursor is at the left side of the previously selected text
            if before_after == "before":
                selected_text_to_the_left_of_phrase = selected_text[:left_index]
                multiline_offset_correction = selected_text_to_the_left_of_phrase.count("\r\n")
                offset = left_index - multiline_offset_correction
            if before_after == "after":
                selected_text_to_the_left_of_phrase = selected_text[:right_index]
                multiline_offset_correction = selected_text_to_the_left_of_phrase.count("\r\n")
                offset = right_index - multiline_offset_correction
            Key("right:%d" %offset).execute()

        if direction == "right":
            # cursor is at the left side of the previously selected text
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
    else:
        # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
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
    

def select_phrase(phrase, direction, number_of_lines_to_search, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return
    
        
    # Approach 1: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # TODO: change this so that it unselects by pressing left and then right rather than pasting over the top
    if application == "texstudio":
        text_manipulation_paste(selected_text, application) # yes, this is kind of redundant but it gets the proper pause time
        multiline_movement_correction = selected_text[right_index :].count("\r\n")
        movement_offset = len(selected_text) - right_index - multiline_movement_correction
        Key("left:%d" %movement_offset).execute()
        multiline_selection_correction = selected_text[left_index : right_index].count("\r\n")
        selection_offset = len(selected_text[left_index : right_index]) - multiline_selection_correction
        Key("s-left:%d" %selection_offset).execute()

    # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    else:
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
    

def select_until_phrase(direction, phrase, before_after, number_of_lines_to_search, occurrence_number, dictation_versus_character):
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = deal_with_up_down_directions(direction, number_of_lines_to_search)
    application = get_application()  
    if not before_after:
    # default to select all the way through the phrase not just up until it
        if direction == "left":
            before_after = "before"
        if direction == "right":
            before_after = "after"
    
    selected_text = select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not selected_text:
        return 
    phrase = str(phrase)
    match_index = get_start_end_position(selected_text, phrase, direction, occurrence_number, dictation_versus_character)
    if match_index:
        left_index, right_index = match_index
    else:
        # phrase not found
        deal_with_phrase_not_found(selected_text, application, direction)
        return
    
    # Approach 1: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # TODO: change this so that it unselects by pressing left and then right rather than pasting over the top
    if application == "texstudio":
        text_manipulation_paste(selected_text, application) # yes, this is kind of redundant but it gets the proper pause time
        if direction == "left":
            if before_after == "before": 
                selected_text_to_the_right_of_phrase = selected_text[left_index :]    
                multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
                offset = len(selected_text) - left_index - multiline_offset_correction
                
            if before_after == "after":
                selected_text_to_the_right_of_phrase = selected_text[right_index :]
                multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
                offset = len(selected_text) - right_index - multiline_offset_correction
            
            Key("s-left:%d" %offset).execute()
        if direction == "right":
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
    
    # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    else:
        if direction == "left":
            Key("right").execute() # unselect text and move to left side of selection
            if before_after == "before":
                multiline_correction = selected_text[left_index :].count("\r\n")
                offset = len(selected_text) - left_index - multiline_correction
            if before_after == "after":
                multiline_correction = selected_text[right_index :].count("\r\n")
                offset = len(selected_text) - right_index - multiline_correction
            Key("s-left:%d" %offset).execute()
        if direction == "right": 
            Key("left").execute() # unselect text and move to the right side of selection
            if before_after == "before":
                multiline_correction = selected_text[: left_index].count("\r\n")
                offset = left_index - multiline_correction
            if before_after == "after":
                multiline_correction = selected_text[: right_index].count("\r\n")
                offset = right_index - multiline_correction
            Key("s-right:%d" %offset).execute()

