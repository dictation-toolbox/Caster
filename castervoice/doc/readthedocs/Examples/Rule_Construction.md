# Rule Construction

This section discusses how to get started making Dragonfly and Caster rules.

# Standard imports
Using the `from library import *` construction to import everything from a particular module is generally frowned upon in Python because it does not make explicit what you are importing, and this can make it difficult to work out where particular names are coming from at a glance.

When constructing caster rules however, there are a fairly well-defined group of objects which are regularly required and which most people reading the rule will be familiar with. These include dragonfly objects, caster utility modules, caster rule types (MergeRule and SelfModifyingRule), etc.

This means that it makes sense to place all of these standard imports into one file, so that they can be imported into a new file with a single line of code. This file can be found at `castervoice/lib/imports.py` and the standard imports can be accessed with:
```python
from castervoice.lib.imports import *
```

# Loading rules
Once you have created a rule class with your desired mappings inside, you need to load it so that the commands are recognised. Wrapper functions for this are provided in `lib/control.py`, taking as parameters your rule (usually a subclass of MergeRule), and if appropriate the context in which it should be active. The types of rule which can be added are detailed further in `doc/readtedocs/CCR.md`. The functions for loading them are as follows, and should be placed at the bottom of the grammar file.

### Global rules
These rules are available in any context, can be chained together with other commands in a single utterance using CCR, and are enabled using the `enable python` command (for example). All of the programming language grammars and core navigation commands are added as global rules.
```python
control.global_rule(MyRule())
```

### Non-CCR app rules
These rules are context specific and do not allow multiple commands in sequence. While this may seem like a limitation, for most app commands (e.g. "page back" in a browser) it is rare to want to do multiple things in a single utterance. Using CCR only when necessary improves start-up time and reduces grammar complexity, so most app grammars are implemented this way.
```python
context = AppContext(title="application title")
control.non_ccr_app_rule(MyRule(), context=context)
```

### CCR app rules
If desired though, it is possible to create contextual commands with CCR, using the following formulation. By default this will allow app commands to be chained with any core commands, but this can be changed by setting the `mwith` property of the rule to a list of rule pronunciations.
```python
context = AppContext(title="application title")
control.ccr_app_rule(MyRule(), context=context)
```

### Self modifying rules
These rules are available globally and modify themselves on the fly. Examples of this in caster include the "bring me" and "alias" commands.
```python
control.selfmod_rule(MyRule())
```