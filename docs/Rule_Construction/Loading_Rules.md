# Loading Rules

Up until this point we talk a lot about of how to create your own commands but not  the context of when they become active.  This is managed through `get_rule` where Caster registers rules to create grammars.

A few things to note as your thinking of loading rule.

- User Caster Rules are loaded from [Caster User Directory](https://caster.readthedocs.io/en/latest/readthedocs/User_Dir/Caster_User_Dir/) `Rules` folder including subfolders and/or the Caster source code directly typically `Documents\Caster\Rules`.

- Up until this point we've used rule class as `MyRule` eg `class MyRule(MappingRule):` in the documentation. This is been done to save time and to reuse the same rule and file. When creating your own rule in a new file create your own unique rule class.

- Caster needs to restart to pick up new rules and the new rule load suuccessfully

- New rules need to  be enabled at least once say 

**Explanation of get_rule**

Once you have created a unique rule class  with your desired mappings inside, you need to load it so that the commands are recognized.  You can customize your rule by defining RuleDetail parameters, which includes the appropriate the context in which it should be active.  The `get_rule()` function returns `RuleDetails`  parameters and the rule class get_rule at the very bottom of your file. Here is a breakdown of the RuleDetails parameters:

**RuleDetails Parameters Summary** 

- `name`:  Rule name needs to be unique

- `executable`:  executable
  
  - For Windows users the `.exe` is not needed. For example `firefox.exe`  would be `firefox`.

- `title`:  Title can be a partial or exact match to the window title of the appllication

- `grammar_name`:  Grammar name needs to be unique

- `ccrtype`:  global, app, selfmod, or none

- `function_context`: Dragonfly FuncContext bool variable
  
  The types of rule which can be added are detailed further in `doc/readtedocs/CCR.md` with complete examples. One rule can only be contained per file. However here is a summary:

## **CCR Global Rules**

`MergeRule`

These rules are available in any context, can be chained together with other commands in a single utterance using CCR, and are enabled using the `enable python` command (for example). All of the programming language grammars and core navigation commands are added as global rules.

```python
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

def get_rule():
    return HomonymsRule, RuleDetails(ccrtype=CCRType.GLOBAL)
```

### **Non-CCR Global Rules**

`MappingRule`

These rules are available in any context and are enabled  e.g. `enable my rule` command. Non-CCR do not allow multiple commands in sequence. While this may seem like a limitation, for most commands (e.g. "page back" in a browser) it is rare to want to do multiple things in a single utterance. Using CCR only when necessary improves start-up time and reduces grammar complexity, so most app grammars are implemented this way.

```python
def get_rule():   
    return MyUniqueRule, RuleDetails(name="my unique rule")
```

### **CCR App Rules**

`MergeRule`

App CCR rules can be made with the following `get_rule` example. By default this will allow app commands to be chained with any CCR commands . Note: It is possible to have a CCR and multiple non-CCR rules for one application in separate files. 

```python
from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def get_rule():
    details = RuleDetails(executable="exe name", 
                          title="application title",
                          ccrtype=CCRType.APP)
    return ExcelRule, details
```

### Non-CCR App Rules

`MappingRule`

App Rules are context specific to a specific application. These can be limited by the application executable and optionally the application window title. The advantage of the window title is you can have multiple grammars for the same application what change based on title that is window displayed

```python
from castervoice.lib.actions import Key, Text, Mouse

from dragonfly import MappingRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

def get_rule():
    details = RuleDetails(executable="exe name", 
                          title="application title")
    return MyRule, details
```

#### Self Modifying CCR Rules

These rules are available globally and modify themselves on the fly. 

```python
from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.const import CCRType
from castervoice.lib.merge.state.short import R

def get_rule():
    return MySelfModRule, RuleDetails(ccrtype=CCRType.SELFMOD)
```

### FuncContext

`MergeRule` or `MappingRule` use their respectiive imports above.

Parameter allows a function to be evaluated if it returns `true` and `false` to  determine context. When the function returns true the context becomes active. Can be used everything above with the exception of`MergeRule`  types `CCRType.SELFMOD` and `ccrtype=CCRType.GLOBAL`.

```python
def get_rule():
    details = RuleDetails(executable="exe name", 
                          title="application title",
                          function_context=myfunction,
                          ccrtype=CCRType.APP)
    return MyFunctionContext, details
```

Based on the type of rule category as described in the above section, these are the required imports. The imports go at the very top of the file.
