# These lines that start with the '#' are called comments. They don't affect the way the code runs.
# In this tutorial file, I put comments above the relevant lines.

# Before we begin, it's worth noting that the function 'get_rule()' that loads this rule is commented out. Therefore will cause it to never run.
# 1. You will need to scroll to the very end of the file and uncomment the following:

# def get_rule():
#     return MyRule, RuleDetails(name="my rule")

# 2. Now that it's uncommented simply start/restart Caster. 
# 3. To enable the rule, say "enable my rule" 

# You can skip down to the next comment, for now this is not important...

from dragonfly import (BringApp, Key, Function, Grammar, Playback, 
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule)

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.actions import Key, Text, Mouse


def my_function(n, text):
    print("put some Python logic here: " + str(text))

class MyRule(MappingRule):

    # It is this section that you want to edit if you're new. The mapping, extras, and defaults
    mapping = {

    # Here I'm just saying two words to trigger some other words
    "hotel info":                   Text("These types of hospitality services are not cheap."),

    # In the next line, there are two things to observe:
    # the first is the use of parentheses and the pipe symbol (|)
    # --this lets me use either "motel" or "lodging" to trigger that command.
    # The next is the playback action, which lets me tell the speech recognition engine to simulate me speaking some words.
    "(motel | lodging)":            Playback([(["hotel", "info"], 0.0)]),

    # Here I'm using BringApp -- this is the same as typing what goes in between the parentheses
    # into the command prompt/terminal, without the quotes and commas, like:
    # Windows OS: explorer C:\NatLink\NatLink\MacroSystem
    # Could be changed changed for Linux/Mac
    # -- (which would open Windows Explorer at the specified location). Anything you can do with the command line can be done this way
    "open natlink folder":          BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

    # Here I'm using the Key action to press some keys -- see the documentation here: https://dragonfly2.readthedocs.io/en/latest/actions.html?#module-dragonfly.actions.action_key
    # "a-" Everything before "-" is a keyboard modifier, "a" is for the "alt" Key.
    # "-space" reprresents the SpaceBar Key. 
    # "/10" After "a-space" Slows down the keypresses by 10 ms" with a seriess of keypresses as demonstrated this may be necessary.
    # The comma "," after "a-space/10" separates keypresses in a series.
    "remax":                        Key("a-space/10,r/10,a-space/10,x"),

    # Here I'm chaining a bunch of different actions together to do a complex task
    # This is Windows OS speciffic but the path in BringApp could be changed for Linux/Mac
    "(show | open) documentation":  BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

    # If you need to do more complicated tasks, or use external resources, a function might be what you need.
    # Note that here, I'm using extras: "n" and "text"
    # The angle brackets <> meaning I'm using an extra, and the square brackets [] mean that I don't have to speak that word, it's optional.
    # Advice: if you use an optional extra, like I am with "text", you should set a default value  in the defaults section down below.
    # To trigger the following command, you would have to say the word "function" followed by a number between 1 and 1000.
    '[use] function <n> [<text>]':   Function(my_function, extra={'n', 'text'}),
	
     # Sometimes it's easier to have things as a list in a command as a choice that do different things.
     # That's what `<choice>` Is defined in `extras` allows you define that list. If you dictate `i choose custom grid` Then `CustomGrid` will be printed as text.
     # Items in the list are pairs. e.g `{"custom grid": "CustomGrid"}` The first item of a pair is the command "custom grid" and the second "CustomGrid" output text action.   
    "i choose <choice>":             Text("%(choice)s"),
        
    }

    extras = [
              IntegerRef("n", 1, 1000),
              Dictation("text"),
              Choice("choice",
                    {
                    "alarm": "alarm",
                    "custom grid": "CustomGrid", 
                    "element": "e"
                    }),
                ]
    defaults = {
                "n": 1,
                "text": "",
            }

# This stuff below is required too -- 
# However you will learn more about how to change the rule types and contexts later in the documentation.

# Uncomment the next two lines.
#def get_rule():
#    return MyRule, RuleDetails(name="my rule")
