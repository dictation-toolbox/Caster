# Dragonfly Rules

This page demonstrates how to get started making Dragonfly rules. Let's start with a very simple Dragonfly `MappingRule`. The following is a complete Python file which will work with Dragon. (For WSR, see the WSR page.)

## My First Rule

The following is a very simple Dragonfly rule:

```python
# the following line imports all the dragonfly stuff we'll be using -- obviously you must have Dragonfly installed
from dragonfly import *

# now we make our MappingRule object with only two commands
class MyRule(MappingRule):
  mapping = {
    "some words I speak":         Key("a, b, c"),
    "command number two":         Text("here is a hashtag: #"),
  }

# now let's create our Grammar object and add an instance of our rule to it:
grammar = Grammar("my_new_grammar")
grammar.add_rule(MyRule())
grammar.load()
```

Done. Name this file `_example1.py`, put it in your Natlink `User Directory` folder (configurable in the Natlink configuration GUI `start_configurenatlink.py`) and reboot Dragon. When you do, saying "some words I speak" will trigger the first command, causing the keys A, B, C to be pressed. Same for the second command. (It is a Text action rather than a Key action, but in the example the effects are similar.)

## Using Extras

Okay, now suppose you want to do something more complex than just pressing pre-set key sequences or typing out pre-set text. This is where `extra`s come in. Below is the same rule, but using extras.

```python
from dragonfly import *

class MyRule(MappingRule):
  mapping = {
    "press key <my_key>":               Key("%(a)s"),
    "print these words <my_words>":     Text("words I said: %(my_words)s"),
  }
  extras = [
    Choice("my_key", {
      "arch": "a",
      "brav": "b",
      "char": "c"
    }),
    Dictation("my_words"),
  ]

grammar = Grammar("my_new_grammar")
grammar.add_rule(MyRule())
grammar.load()
```

With this rule, you can say "press key arch" and "a" will be pressed, or "press key brav" and "b" will be pressed. The second command in the rule uses a `Dictation` extra. Any amount of words can be captured by a `Dictation` extra. So, for example, you can say "print these words the short green tree" -- and that will print "words I said: the short green tree". Whatever you said will be slotted into the result in place of "%(my_words)s".

## Optional Words, Optional Extras, and Defaults

Suppose you want to leave words out sometimes. You can use square brackets to make parts of the `spec`, including the extras, optional. However, if you make extras optional, you should set sensible `default`s or you will get errors when you omit said optional extras. Here is a rule with commands with specs with optional parts:

```python
from dragonfly import *

class MyRule(MappingRule):
  mapping = {
    "press [key] <my_key>":               Key("%(a)s"),
    "print these words [<my_words>]":     Text("words I said: %(my_words)s"),
  }
  extras = [
    Choice("my_key", {
      "arch": "a",
      "brav": "b",
      "char": "c"
    }),
    Dictation("my_words"),
  ]
  defaults = {
    "my_words": "said nothing"
  }

grammar = Grammar("my_new_grammar")
grammar.add_rule(MyRule())
grammar.load()
```

It is nearly identical to the rule in the previous section, except that now to trigger the first command, you don't have to speak the word "key". So, you could say "press arch" or "press key arch" and the effect would be the same. The second command has an optional extra now. So, if you only say "print these words", the default for "my_words" will be used and "word I said: said nothing" will be printed.

## The Function Action

The Dragonfly Key, Mouse, and Text actions will get you pretty far, but what if you need to create more complex behavior? For example, suppose you want to make XMLRPC calls or execute conditional logic based on the specifics of your command? This is where Dragonfly's Function action becomes useful.

```python
from dragonfly import *

def my_fn(my_key):
  '''some custom logic here'''

class MyRule(MappingRule):
  mapping = {
    "press <my_key>":     Function(my_fn),
  }
  extras = [
    Choice("my_key", {
      "arch": "a",
      "brav": "b",
      "char": "c"
    })
  ]

grammar = Grammar("my_new_grammar")
grammar.add_rule(MyRule())
grammar.load()
```

In this example, we defined a function called "my_fn". Any extras in the spec of the command will be available to the function which the Function action will call.

## Compound Actions

Actions can be combined with the `+` operator. (They can also be repeated a dynamic number of times via the `*` operator and Dragonfly's Repeat class.) Below, a Key action and a Function action are combined. Both will execute when the spec is spoken.

```python
from dragonfly import *

def my_fn(my_key):
  '''some custom logic here'''

class MyRule(MappingRule):
  mapping = {
    "press <my_key>":     Key("%(my_key)s") + Function(my_fn),
  }
  extras = [
    Choice("my_key", {
      "arch": "a",
      "brav": "b",
      "char": "c"
    })
  ]

grammar = Grammar("my_new_grammar")
grammar.add_rule(MyRule())
grammar.load()
```

Notice that both the Key action and the Function action use the "my_key" extra. It is available to all of the actions in the command.
