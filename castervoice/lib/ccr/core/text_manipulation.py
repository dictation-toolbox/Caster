from dragonfly import Function, Key, Text, Mouse, Pause, Dictation, Choice, Grammar , ContextAction


from castervoice.lib import control, settings, text_manipulation_functions

from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.ccr.core.punctuation import text_punc_dict,  double_text_punc_dict
from castervoice.lib.alphanumeric import caster_alphabet

# Advertisement
print("""Check out the new experimental text manipulation commands in castervoice\lib\ccr\core\\text_manipulation.py 
    where you can disable this message. Enable them by saying "enable text manipulation". You may want to reduce the pause or sleep time
    in the functions text_manipulation_copy and text_manipulation_paste in castervoice\lib\\text_manipulation_functions.py
    These are WIP, Please give feedback and report bugs""")




""" requires a recent version of dragonfly because of recent modification of the Function action
    # I think dragonfly2-0.13.0
    The wait times should be adjusted depending on the application by changing the numbers in copy_pause_time_dict
    and paste_pause_time_dict which are called by the functions text_manipulation_copy and text_manipulation_paste 
    in text_manipulation_functions.py. The wait times can be further adjusted by adjusting the sleep times in the 
    functions that those functions call: lib.context.read_selected_without_altering_clipboard 
    and lib.context.paste_string_without_altering_clipboard
    the keypress waittime should possibly be made shorter for these commands, though note that the keypress wait time is
    used by the aforementioned functions and lib.context.
    When these commands are not working in a particular application sometimes the problem is that 
    there is not enough time from when control-c is pressed until the contents of the clipboard are passed into the function
    In that case you need to increase the pause time in that application in copy_pause_time_dict
    
    The functions in text_manipulation_functions.py copy text into the clipboard and then return whatever
    you had there before back onto the clipboard. If you are using the multi clipboard (windows-x on Windows 10),
    this might be annoying because you will have some extra junk put on the second (and sometimes third) 
    slot on your multi clipboard. If you get the wait times exactly right, in principle
    this problem can be avoided using the functions lib.context.read_selected_without_altering_clipboard 
    and lib.context.paste_string_without_altering_clipboard
    In my experience, often times the paste part doesn't add
    any junk to the multi-clipboard although the copy (a.k.a. read) part does.

"""

class TextManipulation(MergeRule):
    pronunciation = "text manipulation"


    

        
    mapping = {

    # Todo: Find way to to better consolidate these context actions. 
    # Todo: Put context actions for different apps based on pause time requirements
    # Todo: Consolidate command definitions for left character versus right character; handle defaults in the functions, rather than choice objects.
                
        # PROBLEM: sometimes Dragon thinks the variables are part of dictation.           
        
        # replace text or character
        "replace <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation> with <dictation2>":
            R(Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase")), 
              rdescript="Text Manipulation: replace text to the left or right of the cursor"),
        "replace <direction>  [<number_of_lines_to_search>] [<occurrence_number>] <character> with <character2>":
            R(Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase")), 
              rdescript="Text Manipulation: replace character to the left of the cursor"),
        
        # remove text or character 
        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase")),
                        rdescript="Text Manipulation: remove chosen phrase to the left or right of the cursor"),
        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(character="phrase")), 
              rdescript="Text Manipulation: remove chosen character to the left of the cursor"),
        
        # remove until text or character
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase")), 
              rdescript="Text Manipulation: delete until chosen phrase"),
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(character="phrase")),
              rdescript="Text Manipulation: delete until chosen character"),
        
        # move cursor
        "(go | move) <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase")), 
               rdescript="Text Manipulation: move to chosen phrase to the left or right of the cursor"),
        "(go | move) <direction> [<before_after>] [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_functions.move_until_phrase,
                       dict(character="phrase")),
              rdescript="Text Manipulation: move to chosen character to the left of the cursor"),

        # select text or character
        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_functions.select_phrase, 
            dict(dictation="phrase")), 
                 rdescript="Text Manipulation: select chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_functions.select_phrase,
            dict(character="phrase")),
            rdescript="Text Manipulation: select chosen character"),
        
        # select until text or character
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation> ":
            R(Function(text_manipulation_functions.select_until_phrase, 
            dict(dictation="phrase")), 
                 rdescript="Text Manipulation: select until chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_functions.select_until_phrase,
            dict(character="phrase")), 
            rdescript="Text Manipulation: select until chosen character"),
        
        


        
    }
    text_punc_dict.update(caster_alphabet)
    character_dict = text_punc_dict
    
    extras = [
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("dictation2"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        IntegerRefST("number_of_lines_to_search", 1, 50),
        
    
        Choice("character", character_dict),         
        Choice("character2", character_dict),
    
    
        Choice("direction", {
            "lease": "left",
            "ross": "right",
            "sauce": "up",
            "dunce": "down",
            # note: "sauce" (i.e. "up") will be treated the same as "lease" (i.e. "left") except that
            # the default number_of_lines_to_search will be set to 3
            # in the same way, "dunce" (i.e. "down") will be treated the same as
            # "ross" (i.e. "right")
        }),
        Choice("before_after", {
            "before": "before",
            "after": "after",
        }),
        Choice("occurrence_number", {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "ninth": 9,
            "tenth": 10,
        }),
        
        
    ]
    defaults = {

        "before_after": None,
        "number_of_lines_to_search": 0, # before changing this default, please read the function deal_with_up_down_directions
        "occurrence_number": 1,} # if direction is up or down, the default number_of_lines_to_search 
        # will be 3 instead of zero. 
        # This can be changed in the function deal_with_up_down_directions 
        # 'number_of_lines_to_search = zero' means you are searching only on the current line

control.nexus().merger.add_global_rule(TextManipulation())



