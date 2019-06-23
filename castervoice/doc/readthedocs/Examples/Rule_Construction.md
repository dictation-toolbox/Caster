# Rule Construction

This section discusses how to get started making Dragonfly and Caster rules.

# Standard imports
Using the `from library import *` construction to import everything from a particular module is generally frowned upon in Python because it does not make explicit what you are importing, and this can make it difficult to work out where particular names are coming from at a glance.

When constructing caster rules however, there are a fairly well-defined group of objects which are regularly required and which most people reading the rule will be familiar with. These include dragonfly objects, caster utility modules, caster rule types (MergeRule and SelfModifyingRule), etc.

This means that it makes sense to place all of these standard imports into one file, so that they can be imported into a new file with a single line of code. This file can be found at `castervoice/lib/imports.py` and the standard imports can be accessed with:
```python
from castervoice.lib.imports import *
```