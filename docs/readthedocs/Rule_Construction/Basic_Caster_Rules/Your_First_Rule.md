# Your First Rule

This page demonstrates how to get started experimenting with voice commands with your first rule.  You should experriment here before moving on to 'Basic Rules' Which gives further explanation to many of the concepts demonstrated in `Example Rule Code`  Rule.

Rules should be placed in [Caster User Directory](https://caster.readthedocs.io/en/latest/readthedocs/User_Dir/Caster_User_Dir/) `rules` directory. See hyperlink for directory file path based on OS. The `rules` folder is where all your created rules should be stored. This folder can be summoned by voice say `bring me caster rules` If Caster is running. 

1. Create a new file called `caster_example_rule.py`
    - Windows OS users may need to [enable viewing file extensions](https://helpdesk.flexradio.com/hc/en-us/articles/204676189-How-to-change-a-File-Extension-in-Windows) like `.py`.

2. Copy and paste the entire contents of `Example Rule Code` into `caster_example_rule.py`

3. Simply start/restart(Say `reboot caster`) Caster for the new rule to be recognized.

4. Say `enable my rule` this will make commands available for recognition. Castor remembers that you've activated the rule between restarts. If you wish to disable the rule say `disable my rule`

5. Now any of the commands below like `hotel`  which print out `hotels are not cheap` are available for recognition.

**Note**
    - Saving the file will cause the rule to reload with your changes allowing you to experiment. If there is an error, the status window will show an error message. Correct what's wrong and save the file. Repeat as needed.
    - Caster goes asleep when it has not recognized words after a period of time. Say `caster on` to wake it up and `caster sleep` to stop recognition.
    - `Example Rule Code` - Some of these commands are Windows OS specific like file paths which could be changed if you're using Linux/Mac OS

## Example Rule Code

```python
# These lines that start with the # are called comments. They don't affect the way the code runs.
# In this tutorial file, I put comments above the relevant lines.

# You can skip down to the next comment, for now this is not important...

from dragonfly import (MappingRule, BringApp, Key, Function, Grammar, Playback, 
                       IntegerRef, Dictation, Choice, WaitWindow)

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.actions import Key, Text, Mouse

def my_function(n, text):
    print("put some Python logic here: " + str(text))

class MyRule(MappingRule):

    mapping = {
    # It is this section that you want to fiddle around with if you're new: mapping, extras, and defaults

    # Here I'm just saying two word to trigger some other words
    "hotel info":                  Text("These types of hospitality industry are not cheap."),

    # In the next line, there are two things to observe:
    # the first is the use of parentheses and the pipe symbol (|)
    # --this lets me use either "motel" or "lodging" to trigger that command.
    # The next is the playback action, which lets me tell speech recognition engine to simulate me speaking some words.
    '(motel | lodging)':           Playback([(["hotel", "info"], 0.0)]),

    # Here I'm using BringApp-- this is the same as typing what goes in between the parentheses
    # Into the command prompt/terminnal, without the quotes and commas, like:
    # Windows OS: explorer C:\NatLink\NatLink\MacroSystem
    # Could be changed changed for Linux/Mac
    # -- (which would open Windows Explorer at the specified location). Anything you can do with the command line can be done this way
    "open natlink folder":         BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

    # Here I'm using the Key action to press some keys -- see the documentation here: https://dragonfly2.readthedocs.io/en/latest/actions.html?#module-dragonfly.actions.action_key
    # "a-" Everything before "-" is a keyboard modifier, "a" is for the "alt" Key.
    # "-space" reprresents the SpaceBar Key. 
    # "/10" After "a-space" Slows down the keypresses by 10 ms" with a seriess of keypresses as demonstrated this may be necessary.
    # The comma "," after "a-space/10" separates keypresses in a series.
    # remax is Windows OS Specific to maximize the current window in the forefront
    "remax":                       Key("a-space/10,r/10,a-space/10,x"),

    # Here I'm chaining a bunch of different actions together to do a complex task
    # This is Windows OS speciffic but the path in BringApp could be changed for Linux/Mac
    "(show | open) documentation": BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

    # If you need to do more complicated tasks, or use external resources, a function might be what you need.
    # Note that here, I'm using extras: "n" and "text"
    # The angle brackets <> meaning I'm using an extra, and the square brackets [] mean that I don't have to speak that word, it's optional.
    # Advice: if you use an optional extra, like I am with "text", you should set a default value  in the defaults section down below.
    # To trigger the following command, you would have to say the word "function" followed by a number between 1 and 1000.
    '[use] function <n> [<text>]': Function(my_function, extra={'n', 'text'}),

     # Sometimes it's easier to have things as a list in a command as a choice that do different things.
     # That's what `<choice>` Is defined in `extras` allows you define that list. If you dictate `i choose custom grid` Then `CustomGrid` will be printed as text.
     # Items in the list are pairs. e.g `{"custom grid": "CustomGrid"}` The first item of a pair is the command "custom grid" and the second "CustomGrid" output text action.   
    "i choose <choice>":           Text("%(choice)s"),

    }
# This stuff is required too -- However you will learn more about how to change the rule types and contexts later.
def get_rule():   
    return MyRule, RuleDetails(name="my rule")
```
