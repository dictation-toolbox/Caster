# NodeRule

**Contents**

- [What and Why](#what-and-why)
- [Integration With the Status Window](#integration-with-the-status-window)
- [How to Create and Register a Node](#how-to-create-and-register-a-node)

---

## What and Why

All speech recognition engines, including Dragon NaturallySpeaking, have an upper complexity limit on Grammars. After the limit is reached, a BadGrammar error will occur. NodeRule is a way to sidestep that limit. By packing specs into nodes in a tree - and only activating part of the tree at a given time - it's possible to include thousands of specs in a single grammar.

So, let's say for example that I want to be able to speak any of the following command chains, where the letters represent specs.

    a         | a f o     | b g p
    a d       | a f o q   | c
    a d m     | a f o r   | c h
    a e       | a f o s   | c i
    a f       | b         |
    a f n     | b g       |

That's sixteen specs getting added. Since a lot of them will only be spoken after others, this command set fits well into a tree structure. (Not all command sets will.) The number of specs in the active CCR grammar from this command set can be reduced by only keeping a certain number of levels of the tree structure open (speakable) at a given time.

<img src="https://raw.githubusercontent.com/dictation-toolbox/Caster/master/docs/img/noderule1.png">

In the above diagram, the first two levels of the tree are active. This means I can speak these specs:

    a
    a d
    a e
    a f
    
    b
    b g
    
    c
    c h
    c i

If I then speak spec (a), it's effect occurs, and the NodeRule updates itself so that the active nodes look like the diagram below.

<img src="https://raw.githubusercontent.com/dictation-toolbox/Caster/master/docs/img/noderule2.png">

If I had spoken (a d) instead, only (m) would have been available next.

The NodeRule will reset itself to its initial state if either any of the final nodes are spoken or, if any unrelated **Context Stack** action is spoken.

## Integration With the Status Window (Not implemented Yet)

If the **status window** is active, the NodeRule will use it to display hints about what the next available nodes are.

## How to Create and Register a Node

### Making Your Own TreeNode

To create a TreeRule, you first have to create a [TreeNode](https://github.com/dictation-toolbox/Caster/blob/master/castervoice/lib/merge/selfmod/tree_rule/tree_node.py) which will be passed into the NodeRule constructor. For examples, look at the [tree directory](https://github.com/dictation-toolbox/Caster/tree/master/castervoice/lib/merge/selfmod/tree_rule/trees). A TreeNode basically looks like this:

```python
HintNode("spec", SomeDragonflyAction(), [<child nodes>], [<extras>], {<defaults>})
```

Some further explanation:

- `spec` - the same sort of spec you would use in a Dragonfly MappingRule
- `SomeDragonflyAction` - Text, Mimic, Key, etc.
- `<child nodes>` - a list of HintNodes, which may themselves have child nodes, etc.
- `<extras>` - a list of Dragonfly extras, the same kind you would use in a MappingRule (IntegerRefST, Dictation, Choice, etc.)
- `<defaults>` - a dict of default values for the extras, again, the same kind you would use in a MappingRule

A few examples:

```python
HintNode("hello node <abc>", Text("hello node %(abc)s"), extras=[Dictation("abc")])
HintNode("goodbye", Mimic("go to sleep"))
HintNode("spell name", Function(some_function), [HintNode("Fred", Text("Fred")), HintNode("Sally", Text("Sally"))])
HintNode("choose [<d>]", Function(print_choice), extras=[Choice("d", {"one":1, "two":})], defaults={"d":1})
```

### Registering Your NodeRule.

- Drop the following rule `YourTree.py` into `.caster\rules`

- You will need to add to `settings.toml` under `[Tree_Node_Path]` in its own line eg. `SM_<YourTreeRule>_TREE_PATH = "C:/Users/.caster/data/sm_<YourTreeRule>_tree_node.toml"`

- Restart Caster

- The pronunciation for enabling and disabling a note rule is the `class name` 

  **Note**: To manually reset the NodeTree say `cancel demo nodes`

### Complete NodeRule Example Rule

```python
from castervoice.lib.actions import Text
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.tree_rule.tree_node import TreeNode
from castervoice.lib.merge.selfmod.tree_rule.tree_rule import TreeRule
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R

H = TreeNode

demo_nodes = H("I say zero", R(Text("LevelZero")), [
            H("I say one", Text("Level One A"), [
                    H("two A one", R(Text("Level Two A1")), [
                            H("three A one", R(Text("Level Three A1"))),
                            H("three A two", R(Text("Level Three A2"))),
                            H("three A three", R(Text("Level Three A3")))
                        ]),
                    H("two A two", R(Text("Level Two A2")))
                ]),
            H("level one be", R(Text("Level One B"))),
            H("level one see", R(Text("Level One C")))
    ])

class DemoTreeRule(TreeRule):
    def __init__(self):
        super(DemoTreeRule, self).__init__("demo nodes", demo_nodes)

def get_rule():
     return [DemoTreeRule, RuleDetails(ccrtype=CCRType.SELFMOD)]
```

### Registering the Complete NodeRule Example

1. Drop the following rule `DemoTreeRule` into `.caster\rules`.

2. You will need to add to `settings.toml` Under `[paths]`  the following on its own line `SM_DEMO_NODES_TREE_PATH = "C:/Users/<Insert username here>/.caster/data/sm_demo_tree_node.toml"` 

3. Restart Caster.

4. To enable the rule say `Enable Demo Tree Rule`

   **Note**: If you forget to add the path above in the settings the following will print out.
   `TreeRuleConfigurationError: Path 'SM_DEMO_NODES_TREE_PATH' was not found in the 'paths' section of settings.toml. Did you add it?`

**NodeRule Example Spec Flowchart**

Once the DemoTreeRule is registered the flowchart below can be used as a reference. The flowchart is to clarify the flow of commands throughout different node levels  To begin transitioning the Nodes say `I say zero` It will perform that action and advance to the next level Node. However if I say `level one be` the NodeTree will reset back all the way to the beginning `I say zero`.

![image](https://user-images.githubusercontent.com/24551569/70587921-eafe5b00-1b90-11ea-8e17-16db4036bf73.png)