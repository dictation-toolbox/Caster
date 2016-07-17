#Caster Rules

Dragonfly is a powerful framework for mapping voice commands to actions. Caster gives the user:
* the ability to dynamically combine CCR rules at run time,
* a pre-made set of rules to start with as a base, 
* tools with which to modify the pre-made rules,
* the Context Stack, a way of tracking state between commands.

##MergeRules VS MappingRules

A Caster MergeRule is very similar to a Dragonfly MappingRule, but it has a few extra properties and can do things that MappingRules can't easily do. The following is an example of a full Python file containing two MergeRules *and* a MappingRule.
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class MyMappingRule(MappingRule):
  mapping = {
    "some command":         Key("a"),
    "some other command":   Key("b"),
  }

class MyMergeRule(MergeRule):
  pronunciation = "key rule"
  
  mapping = {
    "press keys <key_one> [<key_two>]":   Key("%(key_one)s, %(key_two)s"),
  }
  extras = [
    Choice("key_one", { "arch": "a", "brav": "b", "char": "c" } ),
    Choice("key_two", { "arch": "a", "brav": "b", "char": "c" } ),
  ]
  defaults = { "key_two": "a" }

class OtherRule(MergeRule):
  pronunciation = "other rule"
  non = MyMappingRule
  auto = [".js"]
  
  mapping = {
    "hello":    Text("hello"),
  }

control.nexus().merger.add_global_rule(MyMergeRule())
control.nexus().merger.add_global_rule(OtherRule())

```


##Pre-made Rules

Out-of-the-box, Caster gives the user new mouse navigation commands (see the Mouse page), text formatting and navigation commands, and programming-language specific rules. (See the Quick Reference for more details.) Unlike Dragonfly, Caster is targeted at programmers specifically, and so more technical knowledge is assumed of its user base.

##Modifying the Pre-made Rules

If you want to modify the pre-made ruleset, there are a few ways to go about it. Of course, you could just edit the source, but then you'd have to deal with merge conflicts when updating to newer versions of Caster. There are two ways to get around this:
* **Make a copy in the safe zone.** (1) Copy the file you'd like to change into your `caster/user` folder. (2) Disable the original rule in your `settings.json` file. (3) Give the new MergeRule a `pronunciation` which is distinct from that of the original. For example, if you're modifying java.py, give the new JavaCCRRule a `pronunciation` of "my java" rather than "java". 
* **Use rule filters.** This is the recommended way. Rule filters allow you to change any part of any rule, either at boot time or when the rule is activated ("merge time"). See the Rule Filters section of the CCR page for more details.
