# Sample.py

There's been a lot of documentation on how to construct Dragonfly rules. However people learn in different ways, and the following is a complete example called `sample.py`. The comments explain a lot of things which beginners might struggle with.

```python
# These lines that start with the # are called comments. They don't affect the way the code runs.
# In this tutorial file, I put comments above the relevant lines.

# Before we begin, it's worth noting that the name of this file, sample.py, will cause it to never run.
# You will have to rename it to "_sample.py".
# Putting an underscore as the first character of a grammar Python file will tell Dragonfly
# that you want this file to run all the time. Grammars that run all the time are a good way to start.
# The alternative is making grammars for specific programs that only trigger when the programs are active.

# You can skip down to the next comment, for now this is not important...

from dragonfly import (BringApp, Key, Function, Grammar, Playback, 
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule, Text, Mouse,)

def my_function(n, text):
    print("put some Python logic here: " + str(text))

class MainRule(MappingRule):

    mapping = {
    # It is this section that you want to fiddle around with if you're new: mapping, extras, and defaults


    # In the next line, there are two things to observe:
    # the first is the use of parentheses and the pipe symbol (|)
    # --this lets me use either "lock dragon" or "deactivate" to trigger that command.
    # The next is the playback action, which lets me tell speech recognition engine to simulate me speaking some words.
	'(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),

    # Here I'm using BringApp-- this is the same as typing what goes in between the parentheses
    # into the Windows command prompt, without the quotes and commas, like:
    # explorer C:\NatLink\NatLink\MacroSystem
    # -- (which would open Windows Explorer at the specified location). Anything you can do with the command line can be done this way
    "open natlink folder":          BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

    # Here I'm using the Key action to press some keys -- see the documentation here: https://dragonfly2.readthedocs.io/en/latest/actions.html?highlight=key#module-dragonfly.actions.action_key
    "remax":                        Key("a-space/10,r/10,a-space/10,x"),

    # Here I'm chaining a bunch of different actions together to do a complex task
    "(show | open) documentation":  BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

    # Here I'm just saying one word to trigger some other words
    "hotel":                        Text("hotels are not cheap"),

    # If you need to do more complicated tasks or use external resources, a function might be what you need.
    # Note that here, I'm using extras: "n" and "text"
    # The angle brackets <> meaning I'm using an extra, and the square brackets [] mean that I don't have to speak that word, it's optional.
    # Advice: if you use an optional extra, like I am with "text", you should set a default value in the defaults section down below.
    # To trigger the following command, you would have to say the word "function" followed by a number between 1 and 1000.
    '[use] function <n> [<text>]':    Function(my_function, extra={'n', 'text'}),
	
     # Sometimes it's easier to have things as a list in a command as a choice that do different things.
     # The `<choice>` defined in `extras` allows you define that list. If you dictate `I choose custom grid` Then `CustomGrid` will be printed as text.
     # Items in the list are pairs. e.g `{"custom grid": "CustomGrid"}` The first item of a pair is the command "custom grid" and the second "CustomGrid" output text action.   
    "i choose <choice>":              Text("%(choice)s"),
        
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

# This stuff is required too -- where I have the word "sample" below, each grammar file should have a unique name.
grammar = Grammar('sample')
grammar.add_rule(MainRule())
grammar.load()
```
