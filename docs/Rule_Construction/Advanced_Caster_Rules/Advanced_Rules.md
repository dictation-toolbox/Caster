# Caster Rules

Up until this point most of the grammars have been based on Dragonfly MappingRules and loaded through Caster's `get_rule`  function. Caster provides is a powerful framework to merge multiple rules together. This allows you to say multiple commands in a single utterance that are defined in different grammars. This is substantially different with MappingRules which requires a pause between each command.

## MergeRules VS MappingRules

A Caster MergeRule is very similar to a MappingRule, but it has a few extra properties and can do things that MappingRules can't easily do. The following is an examples containing two complete MergeRules _and_ a MappingRule.

```python
from dragonfly import MappingRule, Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

class MyRule(MappingRule):
  mapping = {
    "some command":         Key("a"),
    "some other command":   Key("b"),
  }

def get_rule():
    details = RuleDetails(name="Rule Name")
    return MyMappingRule, details
```

```python
from dragonfly import Key, Choice

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

class MyRule(MergeRule):
    pronunciation = "my rule"

    mapping = {
        "press keys <key_one> [<key_two>]": Key("%(key_one)s, %(key_two)s"),
    }
    extras = [
        Choice("key_one", {"arch": "a", "brav": "b", "char": "c"}),
        Choice("key_two", {"arch": "a", "brav": "b", "char": "c"}),
    ]
    defaults = {"key_two": "a"}

def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

Differences you should notice here:

- The `pronunciation` property: this is what you say in order to enable or disable the rule. If it is not specified, the pronunciation will be the name of the class. So, to enable the first MergeRule, you'd say, "enable key rule". To disable it, you'd say, "disable key rule".
  
  - MappingRule Use `name="Rule Name"`  for enable/disable instead of `pronunciation` 

- The `non` property: this is a reference to a MappingRule. This MappingRule will be activated alongside the MergeRule when it is activated through companion rules. MergeRules will be added to the CCR pool, whereas MappingRules are not. All of its commands will remain as singular, uncombinable. This is often desirable because either (1) certain specs don't blend well, or (2) certain commands are not usually combined with others and so keeping them out of the CCR pool reduces combinatorial complexity and improves performance.

- The benefits: MergeRules are merged with each other when activated and are combined into a large CCR command. So for instance, if you said "enable key rule", you could then say "press keys arch press keys arch brav" to press A, A, B. If you then said "enable other rule", you could say "press keys arch hello" to press A and print "hello".

## The Context Stack

In addition to new types of rules, Caster provides new types of actions.

### RegisteredAction

The simplest is `RegisteredAction`. (Type aliased to `R` for short.) `R` can wrap any Dragonfly action(s) and adds additional functionality to said wrapped action(s). Let's look at a simple example.

```python
from dragonfly import Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.short import R

class MyRule(MergeRule):
     pronunciation = "my rule"
     mapping = {
        "favorite bird": R(Text("parakeet"), rdescript="Print my favorite bird"),
    }

def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return Birds, details
```

Two things of note here.

- If there is no `pronunciation` property defined. It defaults `class`  name to `Birds`. To enable this rule then, you'd say "enable birds".
- The `R` action has a `rdescript` parameter. This is a description of what the action does and allows the action to be registered with various printing services (such as the Python console, the status window, or loggers) so you can see the order in which actions are executed, or that they _have_ executed.
  - If `rdescript` is not used. `rdescript`  would default to  `favorite bird"`

`R` can also be used to mark a command as a part of another command. This is one significant difference between Caster and Dragonfly. Dragonfly commands are once-and-done. Caster commands can interact with other commands which have been spoken in the past or will be spoken in the future. In order to use this functionality, we set the `rspec` property of the `R` action. Like so:

```python
from dragonfly import Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.short import R

class MyRule(MergeRule):
    pronunciation = "my rule"
	mapping = {
	"favorite bird":   R(Text("parakeet"), rdescript="Print my favorite bird", rspec="favorite_bird"),
  }

def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

### ContextSeeker

`ContextSeeker` is the most complex and powerful Caster action. It is able to look backwards at commands spoken prior to itself and react according to what it finds. It is also able to delay its execution until future commands are spoken and then act according to what comes next.

In order to do this, the ContextSeeker constructor takes one or both of two arrays of command-searching objects, the "backward" array and the "forward" array. Let's look at a simple example first, a ContextSeeker that looks backward one command for the "favorite bird" command and then prints the rest of the sentence if and only if it finds it.

```python
from dragonfly import Text, Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.actions import ContextSeeker
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R, L, S

class MyRule(MergeRule):
    pronunciation = "my rule"
    mapping = {
        "press key arch": R(Key("a"), rdescript="Press the A key"),
        "favorite bird":  R(Text("parakeet"), rdescript="Print my favorite bird", rspec="favorite_bird"),
        "sentence":       ContextSeeker(back=[
                                          L(
                                            S(["!!!"], NullAction()),
                                            S(["parakeet"], Text(" is my favorite bird"))
                                          )
                                         ]
                                    )
  }

def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

_Whoa there!_ you're thinking. _That's a lot of parentheses and square brackets._ It is. Let's go through what's happening here.

- `L` is the type alias for `ContextLevel`. That there is only one of them indicates that this ContextSeeker is going to look backwards at only one command. So, if you say "favorite bird sentence", the context seeker will find what it was looking for (a command one-prior to itself with `rspec` "parakeet"). However, if you say "parakeet press key arch sentence", the favorite bird command will be two back in the Context Stack rather than one back, the context seeker will not find it, and it will execute the default instead.
- `S` is the type alias for `ContextSet`. An `S` is essentially an if-then branch. Its first parameter is an array of acceptable `rspecs` which will cause it to be chosen rather than one of its siblings. In the case of the second `S`, there is only one, "parakeet". An `S`'s second parameter is what will happen if it is chosen.
- **Defaults**. The first `S` in an `L` will be the default action for the ContextSeeker. Since in our example, we want nothing to happen if the "favorite bird" command isn't spoken immediately prior, we give the first `S` a bogus `rspec` to look for. (You can also give it a legitimate `rspec` if you do want to be able to trigger it intentionally sometimes.) Note that unlike a `command`'s `spec`, an `R`'s or `S`'s `rspec`s do not need to be pronounceable.
- **Wildcards**. If an `S`'s `rspec` array includes an asterisk (like `S(["*"], Key("a"))`), that `S` will be chosen unconditionally, using any command as a trigger.

ContextSeekers can look backwards multiple commands, executing conditional logic on each backwards command that they find, in order.

ContextSeekers can also look forward. Let's look at an example of a forward-looking command.

```python
from dragonfly import Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.actions import ContextSeeker
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R, L, S

class MyRule(MergeRule):
  pronunciation = "my rule"
     mapping = {
    "noon time":      R(Text("noon"), rspec="noon"),
    "afternoon":      R(Text("2 PM"), rspec="afternoon"),
    "midnight":       R(Text("midnight"), rspec="midnight"),
    "wait for":       ContextSeeker(forward=
                                         [
                                          L(
                                            S(["no time"], NullAction()),
                                            S(["noon", "afternoon"], Text("day time")),
                                            S(["midnight"], Text("night time")),
                                          )
                                         ]
                                    )
  }
def get_rule():
    details =  RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

In this example, you can first say "noon time", "afternoon", or "midnight" to print "noon", "2 PM", or "midnight" respectively. But if you say "wait for" first, a forward-looking ContextSeeker will be added to the Context Stack. Nothing will happen immediately. If you then follow up by saying "afternoon", the second `S` will be selected, and "day time" will print. The trigger command, "afternoon" will not execute. It has been _consumed_ by the ContextSeeker. Consumption can be disabled -- see the "ContextSet Parameters" section.

### ContextSet Parameters

The `S` object has a lot of options to specify different kinds of behavior. They are as follows.

- `specTriggers`: the (required) array of `rspec`s which cause the `S` to be chosen rather than its siblings
- `f`: the second (required) parameter, either a Dragonfly action or a Python function reference. If it is a Dragonfly action, the appropriate Dragonfly `extra`s will be made available to it, as if it were spoken by itself. If it is a Python function, you have some options about how to deliver parameters to the function when it is executed. See `parameters`, `user_spoken`, and `use_rspec` for details. (Also note, you can set all three, but there is an order of precedence if you do so: rspec, spoken, parameters -- only one will be used.)
- `parameters`: If `f` is a Python function, you may hard-code its parameters by setting `parameters` to an array. Example below.
- `use_spoken`: If set to True, `use_spoken` will cause an array of strings to be delivered to the `f` function when it executes. Example below.
- `use_rspec`: If set to True, `use_rspec` will deliver the `rspec` string to the function as a single parameter. Example below.
- `consume`: If set to False, trigger commands will not be consumed by ContextSeekers.

That's a lot, so let's see it in action.

```python
from dragonfly import Text

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.actions import ContextSeeker
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R, L, S

def print_params_to_console(params):
  print(params)

class MyRule(MergeRule):
  mapping = {
    "noon time":      R(Text("noon"), rspec="noon"),
    "evening":        R(Text("5 PM"), rspec="evening"),
    "midnight":       R(Text("midnight"), rspec="midnight"),
    "wait for":       ContextSeeker(forward=
                                         [
                                          L(
                                            S(["no time"], NullAction()),
                                            S(["noon"], print_params_to_console, parameters=["some parameters"]),
                                            S(["evening"], print_params_to_console, use_spoken=True),
                                            S(["midnight"], print_params_to_console, use_rspec=True),
                                          )
                                         ]
                                    )
  }

def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

In this example, each of the `S` objects (except the first) delivers parameters to the print_params_to_console function differently. If you say "wait for noon time", an array of strings (specifically, ["some", "parameters"]) will be printed to the console. If you say "wait for midnight", the triggering rspec will be printed ("midnight"). The "evening" option is the most interesting though. If you say "wait for evening", an array containing "wait", "for", and "evening" will be printed. However, if you say, "wait for", and then separately say "evening", an array containing only "evening" will be printed.

### AsynchronousAction

`AsynchronousAction` is a special type of ContextSeeker. AsynchronousActions only look forward. They have only one ContextLevel (`L`) and one ContextSet (`S`). The action in an AsynchronousAction's 0-th ContextSet is repeated continuously until a termination condition is met. The termination conditions are the following:

- **Cancellation**: any of the `rspec` triggers in the 0-th ContextSet are detected.
- **Timeout**: the action runs until the maximum repetitions.
- **Success**: the action is a Python function and returns True.

Let's look at a few basic AsynchronousActions:

```python
from dragonfly import Key

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType

from castervoice.lib.merge.state.short import R, L, S
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.actions2 import NullAction

my_value = 0


def repeat_me():
    global my_value
    my_value = my_value + 5
    print(my_value)
    if my_value == 10:
        my_value = 0
        return True
    return False


class MyRule(MergeRule):
    mapping = {
        "term": R(NullAction(), rspec="term_"),
        "key left": AsynchronousAction([L(S(["term_"], Key("left")))]),
        "key right": AsynchronousAction([L(S(["!"], Key("right")))],
                                        time_in_seconds=2, repetitions=5),
        "repeat_me": AsynchronousAction([L(S(["!"], repeat_me))]),
    }


def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return MyRule, details
```

Here we have one `R` and three AsynchronousActions. The first AsynchronousAction will run indefinitely, pressing the left key at one-second intervals (the default for `time_in_seconds`) until the "term" command is spoken. The second AsynchronousAction will run for 10 seconds, pressing the right key at two-second intervals. The third will run the "repeat_me" function twice and then terminate because "repeat_me" returned True.

The parameters for AsynchronousAction are as follows.

- `forward`: described above.
- `repetitions`: maximum repetitions. It is a good habit to set this unless you intend the AsynchronousAction to be able to run forever.
- `time_in_seconds`: the time between executions of the action in `forward`.
- `blocking`: whether the AsynchronousAction should block other commands from executing while it is running. Caster commands, but not Dragonfly's, can be blocked. Defaults to True. Unless cancelled, blocked commands will execute after the AsynchronousAction is finished.
- `finisher`: a Dragonfly action which runs after the AsynchronousAction is finished.

### Understanding Rule Merging.

When MergeRules are activated, they are merged together with each other into one large CCR rule. If rules are incompatible with each other, the more-recently activated rule will deactivate the less-recently activated rule. For instance, both the Java and Python rules have "if" and "else" commands, so either would deactivate the other. Compatibility is based on specs: rules with even one identical spec are incompatible. New merging strategies can be created - see [classic_merging_strategy.py](https://github.com/dictation-toolbox/Caster/tree/master/castervoice/lib/merge/ccrmerging2/merging) for the default strategy with some interesting [notes](https://github.com/synkarius/Caster/issues/46). 

Let's say you have four rules, A, B, C, and D. A is incompatible with D, but B and C are not incompatible with anything. Now suppose you have B, C, and D active, and you speak the command to activate rule A. The current combined rule, composed of B, C, and D, is dropped. A is treated as the new combined rule. It is then merged with B. Now the combined rule consists of A and B. Then C is merged in: still no incompatibilities, so the new combined rule is A, B, and C. Now Caster attempts to merge D in, but discovers the incompatibility and drops D, since A is the more-recently activated of the two incompatible rules.
