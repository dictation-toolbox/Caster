# Rule Filters

- **Rule Filters Removed From Caster 1.0.0. Replaced by Transformers.**

## Rule Merging

Before we get into how rule filters work, you need to know a little about the rule-merging process.

When MergeRules are activated, they are merged together with each other into one large CCR rule. If rules are incompatible with each other, the more-recently activated rule will deactivate the less-recently activated rule. For instance, both the Java and Python rules have "if" and "else" commands, so either would deactivate the other. Compatibility is based on specs: rules with even one identical spec are incompatible.

Let's say you have four rules, A, B, C, and D. A is incompatible with D, but B and C are not incompatible with anything. Now suppose you have B, C, and D active and you speak the command to activate A. The current combined rule, composed of B, C, and D, is dropped. A is treated as the new combined rule. It is then merged with B. Now the combined rule consists of A and B. Then C is merged in: still no incompatibilities, so the new combined rule is A, B, and C. Now Caster attempts to merge D in, but discovers the incompatibility and drops D, since A is the more-recently activated of the two incompatible rules.

### Merge Times

There are three times these merges occur: at boot, when you manually activate a rule, and when a `SelfModifyingRule` changes itself. The third is out of the scope of this document, and so will not be discussed. At boot, Caster looks at your CCR config file (caster/bin/data/ccr.toml), and activates whatever rules you had active last time you were using Caster. By default, four CCR rules are active: Alphabet, Numbers, Navigation, and Punctuation.

### How Rule Filters Work

In our example above with A, B, C, and D, the rules were combined (or at least attempted) in pairs. (A and B, C and AB, D and ABC.) At each point at which an incompatibility could occur (each "merge point"), Caster gives you the user the opportunity to examine and change the incoming pair of rules. You can write functions which do anything you want to the two rules, based on any properties of the rules, or the merge. To do this, you need to understand MappingRules and MergeRules, and their properties. That is why this section is last. Let's look at some example rule filters.

```Python
from castervoice.lib import control
from castervoice.lib.merge.mergepair import MergeInf
from castervoice.lib.merge.state.short import R

def handle_incompatibility_by_deletion(mp):
    if mp.time == MergeInf.RUN and mp.rule1 is not None:
        for spec in mp.rule1.mapping_actual().keys():
            if spec in mp.rule2.mapping_actual().keys():
                del mp.rule2.mapping_actual()[spec]

control.nexus().merger.add_filter(handle_incompatibility_by_deletion)
```

This rule filter would ensure that there was never any incompatibility, by deleting conflicting words in the more-recently activated rule. Things worth pointing out here:

- The function receives a parameter called "mp". "mp" is an instance of `caster.lib.dfplus.merge.mergepair.MergePair`. It includes either one or two rules and information about the merge.
- `rule1` is checked for None. `rule1` can be None. `rule2` cannot be None.
- Either of the rules can be modified in any way before the function exits and the attempted merge takes place.
- The rule filter is added to the Caster rule merger via `control.nexus().merger.add_filter`.

Here is another example. Suppose you don't like a particular spec and want to replace or modify it?

```Python
from castervoice.lib import control
from castervoice.lib.merge.mergepair import MergeInf
from castervoice.lib.merge.state.short import R

def replace_spec(rule, target, replacement):
    if target in rule.mapping_actual().keys():
        action = rule.mapping_actual()[target]
        del rule.mapping_actual()[target]
        rule.mapping_actual()[replacement] = action

def replace_spec_filter(mp):
    if mp.time == MergeInf.BOOT:
        target = "[go to] line <n>"
        replacement = "travel to line <n>"

        if mp.rule1 is not None:
            replace_spec(mp.rule1, target, replacement)
        replace_spec(mp.rule2, target, replacement)

control.nexus().merger.add_filter(replace_spec_filter)
```

In this example, "[go to] line <n>" is replaced by "travel to line <n>". This could be configured to replace any number of specs, perhaps reading in from a dictionary file.

Maybe you're fine with a spec, but you want to replace the action?

```Python
from dragonfly.actions.action_text import Text

from castervoice.lib import control
from castervoice.lib.merge.mergepair import MergeInf
from castervoice.lib.merge.state.short import R

def update_python(rule):
    if "shells" in rule.mapping_actual().keys():
        rule.mapping_actual()["shells"] = R(Text("not allowed to use 'else'"), rdescript="Troll Replacement")

def replace_python_else_action(mp):
    if mp.time == MergeInf.RUN and mp.type == MergeInf.GLOBAL:
        if mp.rule1 is not None and mp.rule1.get_pronunciation() == "Python":
            update_python(mp.rule1)
        if mp.rule2.get_pronunciation() == "Python":
            update_python(mp.rule2)

control.nexus().merger.add_filter(replace_python_else_action)
```

Notice here how both `rule1` and `rule2` are being checked. That is because either of them might be the Python rule which is being targeted.

Here is another example. In this one, we add the "identity is" command to the Python rule:

```python
from dragonfly.actions.action_text import Text

from castervoice.lib import control
from castervoice.lib.merge.mergepair import MergeInf
from castervoice.lib.merge.state.short import R

def add_is_to_python(rule):
    if rule.get_pronunciation() == "Python":
        rule.mapping_actual()["identity is"] = R(Text(" is "), rdescript="Python: Is")

def add_is_to_python_filter(mp):
    if mp.time == MergeInf.BOOT:
        if mp.rule1 is not None:
            add_is_to_python(mp.rule1)
        add_is_to_python(mp.rule2)

control.nexus().merger.add_filter(add_is_to_python_filter)
```

### Where Do I Put These?

The designated location which Caster will check for rule filters is the `caster/user/filters` folder. Any Python files you put there with rule filters will be picked up, and, like the rest of the `caster/user` folder, will not be affected by Caster updates.