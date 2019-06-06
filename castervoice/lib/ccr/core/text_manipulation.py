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
    The wait times should be adjusted depending on the application by changing the numbers in 
    text_manipulation_copy and text_manipulation_paste as well as the functions they call which are
    lib.context.read_selected_without_altering_clipboard and lib.context.paste_string_without_altering_clipboard
    the keypress waittime should probably be made shorter for these commands.
    When these commands are not working in a particular application sometimes the problem is that 
    there is not enough time from when control-c is pressed until the contents of the clipboard are passed into the function
    The solution is to add a longer pause after pressing control see in the supporting functions in text_manipulation_functions.py
    For some applications, pauses in the copy and paste commands are unnecessary and should be removed or shortened by the user.
    and may be removed by the user if they wish to speed up the execution of these commands
    The functions used by the commands copy text into the clipboard and then return whatever you had there before back onto the clipboard.
    If you are using the multi clipboard, thins might be annoying because you will have some
    extra junk put on the second slot on your multi clipboard. If you get the wait times exactly right, in principle this problem can be avoided
    if you are using the functions lib.context.read_selected_without_altering_clipboard and lib.context.paste_string_without_altering_clipboard
    Even though those functions use pyperclip, somehow they can sometimes avoid this problem if you get the 
    right pause time (I think shorter is better), whereas using pure pyperclip 
    does not seem to avoid this problem.
"""

class TextManipulation(MergeRule):
    pronunciation = "text manipulation"


    

        
    mapping = {

    # Todo: Find way to to better consolidate these context actions. 
    # Todo: Put context actions for different apps based on pause time requirements
    # Todo: Consolidate command definitions for left character versus right character; handle defaults in the functions, rather than choice objects.
                
        # PROBLEM: sometimes Dragon thinks the variables are part of dictation.           
        
        "replace <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation> with <dictation2>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", direction="left_right"), 
                       application="standard"), actions=[
                        # Use different cursor method for texstudio
                        (AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", direction="left_right"), 
                       application="texstudio"))]),
              rdescript="Text Manipulation: replace text to the left or right of the cursor"),
        
        "replace <direction>  [<number_of_lines_to_search>] [<occurrence_number>] <character> with <character2>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase", direction="left_right"), 
                       application="standard"), actions=[
                        # Use different cursor method for texstudio
                        (AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase", direction="left_right"), 
                       application="texstudio"))]),
              rdescript="Text Manipulation: replace character to the left of the cursor"),
        
        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", direction="left_right"), application="standard"),
                       actions=[(AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", direction="left_right"), application="texstudio"))]),
              rdescript="Text Manipulation: remove chosen phrase to the left or right of the cursor"),
        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(character="phrase", direction="left_right"),
                       application="standard"), actions=[(AppContext(executable="texstudio"), 
                       Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(character="phrase", direction="left_right"),
                       application="texstudio"))]),
              rdescript="Text Manipulation: remove chosen character to the left of the cursor"),
        
        "go <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default = Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", direction="left_right"), application="standard"), 
                       # Use different method for texstudio
                       actions=[             
                (AppContext(executable="texstudio"), Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", direction="left_right"), application="texstudio")),
                ]), rdescript="Text Manipulation: move to chosen phrase to the left or right of the cursor"),
        "go <direction> [<before_after>] [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.move_until_phrase,
                       dict(character="phrase", direction="left_right"),
                       application="standard"), actions=[(AppContext("texstudio"),
                       Function(text_manipulation_functions.move_until_phrase,
                       dict(character="phrase", direction="left_right"),
                       application="texstudio"))]),
              rdescript="Text Manipulation: move to chosen character to the left of the cursor"),
        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase, 
            dict(dictation="phrase", direction="left_right"), 
            application="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase,
                       dict(dictation="phrase", direction="left_right"),
                       application="texstudio"))]),
                 rdescript="Text Manipulation: select chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase,
            dict(character="phrase", direction="left_right"),
            application="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase, dict(character="phrase", direction="left_right"),
            application="texstudio"))]),
            rdescript="Text Manipulation: select chosen character"),
        
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation> ":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase, 
            dict(dictation="phrase", direction="left_right"), 
            application="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, dict(dictation="phrase", direction="left_right"), 
            application="texstudio"))]),
                 rdescript="Text Manipulation: select until chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase,
            dict(character="phrase", direction="left_right"), 
            application="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, 
            dict(character="phrase", direction="left_right"), 
            application="texstudio"))]),
            rdescript="Text Manipulation: select until chosen character"),
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", direction="left_right"), application="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", direction="left_right"), application="texstudio"))]),
              rdescript="Text Manipulation: delete until chosen phrase"),
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(character="phrase", direction="left_right"),
                       application="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(character="phrase", direction="left_right"),
                       application="texstudio"))]),
              rdescript="Text Manipulation: delete until chosen character"),
        


        
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
            "sauce": "left",
            "dunce": "right",
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
        "number_of_lines_to_search": 0,
        "occurrence_number": 1,}

control.nexus().merger.add_global_rule(TextManipulation())



