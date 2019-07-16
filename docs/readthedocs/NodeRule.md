# NodeRule

**Contents**

- [What and Why](#what-and-why)
- [Integration With the Status Window](#integration-with-the-status-window)
- [How to Create and Register a Node](#how-to-create-and-register-a-node)

---

## What and Why

Dragon NaturallySpeaking has an upper complexity limit on Grammars. After the limit is reached, a BadGrammar error will occur. NodeRule is a way to sidestep that limit. By packing specs into nodes in a tree, and only activating part of the tree at a given time, it's possible to include thousands of specs in a single grammar.

So, let's say for example that I want to be able to speak any of the following command chains, where the letters represent specs.

    a         | a f o     | b g p
    a d       | a f o q   | c
    a d m     | a f o r   | c h
    a e       | a f o s   | c i
    a f       | b         |
    a f n     | b g       |

That's sixteen specs getting added. Since a lot of them will only be spoken after others, this command set fits well into a tree structure. (Not all command sets will.) The number of specs in the active CCR grammar from this command set can be reduced by only keeping a certain number of levels of the tree structure open (speakable) at a given time.

<img src="https://raw.githubusercontent.com/synkarius/caster/master/caster/doc/img/noderule1.png">

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

<img src="https://raw.githubusercontent.com/synkarius/caster/master/caster/doc/img/noderule2.png">

If I had spoken (a d) instead, only (m) would have been available next.

The NodeRule will reset itself to its initial state if either any of the final nodes are spoken or, if any unrelated **Context Stack** action is spoken.

## Integration With the Status Window

If the **status window** is active, the NodeRule will use it to display hints about what the next available nodes are.

## How to Create and Register a Node

### Making Your Own HintNode

To create a NodeRule, you first have to create a [HintNode](https://github.com/synkarius/caster/blob/master/caster/lib/dfplus/hint/hintnode.py) which will be passed into the NodeRule constructor. For examples, look at the [nodes directory](https://github.com/synkarius/caster/tree/master/caster/lib/dfplus/hint/nodes). A HintNode basically looks like this:

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

### Registering Your NodeRule with CCR (optional)

The topmost node will be treated a little differently than the rest.

- Its text/spec will not be used to create any commands. They will be ignored in this regard. Instead, its text will be used to create the enable/disable commands if you register it with CCR.
- Its immediate children will be treated as top-level nodes, and it is to them that the NodeRule will reset, when it resets.

A NodeRule can be added to a normal Dragonfly grammar. However, if you wish to add one to the global Caster CCR grammar, you must register it by adding its HintNode to the list in [\_nodes.py](https://github.com/synkarius/caster/blob/master/caster/lib/dfplus/hint/_nodes.py). Then, a NodeRule will be generated for that HintNode the next time you reboot Dragon NaturallySpeaking, and you can enable or disable it by saying `enable <topmost node spec>` or `disable <topmost node spec>`.
