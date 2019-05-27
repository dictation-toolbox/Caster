from dragonfly import Function, Key, Text, Mouse, Pause, Dictation, Choice, Grammar , ContextAction


from castervoice.lib import control, settings, text_manipulation_functions

from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.short import R

# Advertisement
print("""Check out the new experimental text manipulation commands in castervoice\lib\ccr\core\\text_manipulation.py 
    Enable them by saying "enable text manipulation". You may want to reduce the pause time in the function select_text_and_return_it in castervoice\lib\\text_manipulation_functions.py
    These are WIP, Please give feedback and report bugs""")




""" requires a recent version of dragonfly because of recent modification of the Function action
    # I think dragonfly2-0.13.0
    The PAUSE TIMES in these functions should be reduced (possibly depending on the application, eventually can use a context action ).
    I have them cranked up very high right now just to make sure everything works.
    the keypress waittime should probably be made shorter for these commands.
    When these commands are not working in a particular application sometimes the problem is that 
    there is not enough time from when control-c is pressed until the contents of the clipboard are passed into the function
    The solution is to add a longer pause after pressing control see in the supporting functions in text_manipulation_functions.py
    For some applications this pause ( and other pauses in the functions for that matter ) is not necessary
    and may be removed by the user if they wish to speed up the execution of these commands
    These functions copy text into the clipboard and then return whatever you had there before backing onto the clipboardcenter.
    If you are using the multi clipboard, thins might be annoying because you will have some
    extra junk put on the second slot on your multi clipboard. To combat this problem you
    could use castervoice.lib.context.read_selected_without_altering_clipboard() instead of pyperclip
"""

class TextManipulation(MergeRule):
    pronunciation = "text manipulation"


    

        
    mapping = {

    # Todo: Find way to to better consolidate these context actions. 
    # Todo: Put context actions for different apps based on pause time requirements
    # Todo: Consolidate command definitions for left character versus right character; handle defaults in the functions, rather than choice objects.
                
        # PROBLEM: sometimes Dragon thinks the variables are part of dictation.           
        
        "replace <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation> with <dictation2>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="standard"), actions=[
                        # Use different cursor method for texstudio
                        (AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: replace text to the left or right of the cursor"),
        
        "replace <lease_ross>  [<number_of_lines_to_search>] [<occurrence_number>] <character> with <character2>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="standard"), actions=[
                        # Use different cursor method for texstudio
                        (AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase", lease_ross="left_right"), 
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: replace character to the left of the cursor"),
        
        "remove <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"),
                       actions=[(AppContext(executable="texstudio"), Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: remove chosen phrase to the left or right of the cursor"),
        "remove <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="standard"), actions=[(AppContext(executable="texstudio"), 
                       Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: remove chosen character to the left of the cursor"),
        
        "go <lease_ross> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default = Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"), 
                       # Use different method for texstudio
                       actions=[             
                (AppContext(executable="texstudio"), Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio")),
                ]), rdescript="Text Manipulation: move to chosen phrase to the left or right of the cursor"),
        "go <lease_ross> [<before_after>] [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.move_until_phrase,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="standard"), actions=[(AppContext("texstudio"),
                       Function(text_manipulation_functions.move_until_phrase,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: move to chosen character to the left of the cursor"),
        "grab <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase, 
            dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase,
                       dict(dictation="phrase", lease_ross="left_right"),
                       cursor_behavior="texstudio"))]),
                 rdescript="Text Manipulation: select chosen phrase"),
        "grab <lease_ross> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_phrase,
            dict(character="phrase", lease_ross="left_right"),
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_phrase, dict(character="phrase", lease_ross="left_right"),
            cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select chosen character"),
        
        "grab <lease_ross> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation> ":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase, 
            dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, dict(dictation="phrase", lease_ross="left_right"), 
            cursor_behavior="texstudio"))]),
                 rdescript="Text Manipulation: select until chosen phrase"),
        "grab <lease_ross> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.select_until_phrase,
            dict(character="phrase", lease_ross="left_right"), 
            cursor_behavior="standard"), actions=[(AppContext("texstudio"),
            Function(text_manipulation_functions.select_until_phrase, 
            dict(character="phrase", lease_ross="left_right"), 
            cursor_behavior="texstudio"))]),
            rdescript="Text Manipulation: select until chosen character"),
        "remove <lease_ross> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right"), cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: delete until chosen phrase"),
        "remove <lease_ross> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(ContextAction(default=Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="standard"),
                       actions=[(AppContext("texstudio"), Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(character="phrase", lease_ross="left_right"),
                       cursor_behavior="texstudio"))]),
              rdescript="Text Manipulation: delete until chosen character"),
        


        
    }
    character_dict = {
                "(left prekris | lay)": "(",
                "(right prekris | ray)": ")",
                "(left brax | lack)": "[",
                "(right brax | rack)": "]",
                "(left angle | lang)": "<",
                "(right angle | rang)": ">",
                "(left curly | lace)": "{",
                "(right curly | race)": "}",
                "quotes": '"',
                "(single quote | thin quote)": "'",
                "comma": ",",
                "(dot | period)": ".",
                "questo": "?",
                "deckle": ":",
                "semper": ";",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "clamor": "!",
                "ampersand": "&",
                "modulo": "%",
                "atty": "@",
                "arch"    : "a",
                "brov"    : "b",
                "char"    : "c",
                "delta"   : "d",
                "echo"    : "e",
                "foxy"    : "f",
                "goof"    : "g",
                "hotel"   : "h",
                "India"   : "i",
                "julia"   : "j",
                "kilo"    : "k",
                "Lima"    : "l",
                "Mike"    : "m",
                "Novakeen": "n",
                "oscar"   : "o",
                "prime"   : "p",
                "Quebec"  : "q",
                "Romeo"   : "r",
                "Sierra"  : "s",
                "tango"   : "t",
                "uniform" : "u",
                "victor"  : "v",
                "whiskey" : "w",
                "x-ray"   : "x",
                "yankee"  : "y",
                "Zulu"    : "z",
    }

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
    
    
        Choice("lease_ross", {
            "lease": "left",
            "ross": "right",
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
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", 
        "horizontal_distance": 0, "vertical_distance": 0, 
        "lease_ross": "left",
        "before_after": None,
        "number_of_lines_to_search": 0,
        "occurrence_number": 1,}

control.nexus().merger.add_global_rule(TextManipulation())



