# Rule Construction

This section discusses how to get started making Dragonfly and Caster rules. 

## Dragonfly Rules

These are some basic examples of how Dragonfly loads rules. Dragon rules can be converted to Caster equivalents by replacing the loading functions and with the proper Caster imports. The following are types of dragonfly rules.

**Dragonfly App Rule**

```python
context = AppContext(executable="devenv", title="microsoft visual studio")
grammar = Grammar("visual studio", context=context)
grammar.add_rule(MicrosoftVisualStudioRule())
grammar.load()
```

**Dragonfly Global Rule**

```python
grammar = Grammar("my new grammar")
grammar.add_rule(MyRule())
grammar.load()
```

## Caster Loading Rules

Caster differs from Dragonfly on how it manages loading rules. The primary purpose for this difference is so that Caster can manages the CCR merger and makes rules reloadable on save. 

Once you have created a rule class with your desired mappings inside, you need to load it so that the commands are recognised. RuleDetails are provided in `lib\ctrl\mgr\rule_details.py`, that has parameters your rule, and if appropriate the context in which it should be active.  The `get_rule()` function returns `RuleDetails` parameters and the rule class. Here is a breakdown of the RuleDetails parameters.

**RuleDetails Parameters Summary** 

- `name`:  Dragonfly rule name needs to be unique

- `executable`:  Dragonfly AppContext executable
  - For Windows users the `.exe` is not needed. For example `firefox.exe`  would be `firefox`.

- `title`:  AppContext title can be a partial or exact match

- `grammar_name`:  Dragonfly grammar name Needs to be unique

- `ccrtype`:  global, app, selfmod, or none

 The types of rule which can be added are detailed further in `doc/readtedocs/CCR.md` with complete examples.  However here is a summary.

**Global CCR Rules**

These rules are available in any context, can be chained together with other commands in a single utterance using CCR, and are enabled using the `enable python` command (for example). All of the programming language grammars and core navigation commands are added as global rules.

```python
def get_rule():
    return MyRule, RuleDetails(ccrtype=CCRType.GLOBAL)
```

### Non-CCR App Rules
These rules are context specific and do not allow multiple commands in sequence. While this may seem like a limitation, for most app commands (e.g. "page back" in a browser) it is rare to want to do multiple things in a single utterance. Using CCR only when necessary improves start-up time and reduces grammar complexity, so most app grammars are implemented this way.

```python
def get_rule():
    details = RuleDetails(executable="exe name", 
                          title="application title")
    return MyRule, details
```

### CCR App Rules
App specific commands with CCR, using the following formulation. By default this will allow app commands to be chained with any core commands.
```python
def get_rule():
    details = RuleDetails(executable="exe name", 
                          title="application title",
                          ccrtype=CCRType.APP)
    return MyRule, details
```

### Self Modifying CCR Rules
These rules are available globally and modify themselves on the fly. Examples of this in Caster include the "bring me" and "alias" commands.
```python
def get_rule():
    return MyRule, RuleDetails(ccrtype=CCRType.SELFMOD)
```



## Required Caster Imports by Rule Category

Based on the type of rule category as described in the above section require important. The imports go at the very top of the file.

**CCR App Rules / Global CCR Rules**

```python
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType
```

**Non-CCR App Rules**

```python
from dragonfly import MappingRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
```

**Self Modifying CCR Rules**

```python
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.const import CCRType
```





