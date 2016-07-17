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
  
  mapping = {
    "hello":    Text("hello"),
  }

control.nexus().merger.add_global_rule(MyMergeRule())
control.nexus().merger.add_global_rule(OtherRule())

```
Differences you should notice here:
* The `pronunciation` property: this is what you say in order to enable or disable the rule. If it is not specified, the pronunciation will be the name of the class. So, to enable the first MergeRule, you'd say, "enable key rule". To disable it, you'd say, "disable key rule".
* The `non` property: this is a reference to a MappingRule. This MappingRule will be activated alongside the MergeRule when it is activated. See how we are not creating a Grammar object and using it to add the MappingRule like we would normally? Although the MergeRule will be added to the CCR pool, the MappingRule will not. All of its commands will remain as singular, uncombineable. This is often desirable because either (1) certain specs don't blend well, or (2) certain commands are not usually combined with others and so keeping them out of the CCR pool reduces combinatorial complexity and improves performance.
* Using the Nexus. Caster MergeRules are usually added to the "nexus". This is a singleton object which manages the CCR pool and various other Caster services. You can add a MergeRule to a Dragonfly Grammar object, but you won't get the benefits that way.
* The benefits. MergeRules are merged with each other when activated and are combined into a large CCR command. So for instance, if you said "enable key rule", you could then say "press keys arch press keys arch brav" to press A, A, B. If you then said "enable other rule", you could say "press keys arch hello" to press A and print "hello".

##The Context Stack
In addition to new types of rules, Caster provides new types of actions. 

###RegisteredAction

The simplest is `RegisteredAction`. (Type aliased to  `R` for short.) `R` can wrap any Dragonfly action(s) and adds additional functionality to said wrapped action(s). Let's look at a simple example.
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class Birds(MergeRule):
  mapping = {
    "favorite bird":   R(Text("parakeet"), rdescript="Print my favorite bird"),
  }
control.nexus().merger.add_global_rule(Birds())
```
Two things of note here.
* There is no `pronunciation` property. To enable this rule then, you'd say "enable birds".
* The `R` action has a `rdescript` parameter. This is a description of what the action does, and allows the action to be registered with various printing services (such as the Python console, the status window, or loggers) so you can see the order in which actions executed, or that they *have* executed.

`R` can also be used to mark a command as a part of another command. This is one significant difference between Caster and Dragonfly. Dragonfly commands are once-and-done. Caster commands can interact with other commands which have been spoken in the past or will be spoken in the future. In order to use this functionality, we set the `rspec` property of the `R` action. Like so:
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class Birds(MergeRule):
  mapping = {
    "favorite bird":   R(Text("parakeet"), rdescript="Print my favorite bird", rspec="favorite_bird"),
  }
control.nexus().merger.add_global_rule(Birds())
```

###ContextSeeker

`ContextSeeker` is the most complex and powerful Caster action. It is able to look backwards at commands spoken prior to itself, and react according to what it finds. It is also able to delay its execution until future commands are spoken, and then act according to what comes next.

In order to do this, the `ContextSeeker` constructor takes one or both of two arrays of command-searching objects, the "backward" array and the "forward" array. Let's look at a simple example first, a `ContextSeeker` that looks backward one command for the "favorite bird" command and then prints the rest of the sentence if and only if it finds it.
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R, S, L

class Birds(MergeRule):
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
control.nexus().merger.add_global_rule(Birds())
```
*Whoa there!* you're thinking. *That's a lot of parentheses and square brackets.* It is. Let's go through what's happening here.
* `L` is the type alias for `ContextLevel`. That there is only one of them indicates that this `ContextSeeker` is going to look backwards only one command. So, if you say "favorite bird sentence", the context seeker will find what it was looking for (a command one-prior to itself with `rspec` "parakeet"). However, if you say "parakeet press key arch sentence", the favorite bird command will be two back in the Context Stack rather than one back and the context seeker will not find it, and will execute the default instead.
* `S` is the type alias for `ContextSet`. An `S` is essentially an if-then branch. Its first parameter is an array of acceptable `rspec`s which will cause it to be chosen rather than one of its siblings. In the case of the second `S`, there is only one, "parakeet". An `S`'s second parameter is what will happen if it is chosen.
* **Defaults**. The first `S` in an `L` will be the default action for the `ContextSeeker`. Since in our example, we want nothing to happen if the "favorite bird" command isn't spoken immediately prior, we give the first `S` a bogus `rspec` to look for. (You can also give it a legitimate `rspec` if you do want to be able to trigger it intentionally sometimes.) Note that unlike a `command`'s `spec`, an `R`'s or `S`'s `rspec`s do not need to be pronounceable.
* **Wildcards**. If an `S`'s `rspec` array includes an asterisk (like `S(["*"], Key("a"))`), that `S` will be chosen unconditionally, using any command as a trigger.
 
`ContextSeeker`s can look backwards multiple commands, executing conditional logic on each backwards command that they find, in order.

`ContextSeeker`s can also look forward. Let's look at an example of a forward-looking command.
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R, S, L

class Times(MergeRule):
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
control.nexus().merger.add_global_rule(Times())
```
In this example, you can first say "noon time", "afternoon", or "midnight" to print "noon", "2 PM", or "midnight" respectively. But if you say "wait for" first, a forward-looking `ContextSeeker` will be added to the Context Stack. Nothing will happen immediately. If you then follow up by saying "afternoon", the second `S` will be selected, and "day time" will print. The trigger command, "afternoon" will not execute. It has been *consumed* by the `ContextSeeker`. Consumption can be disabled -- see the "ContextSet Parameters" section.

###ContextSet Parameters

The `S` object has a lot of options to specify different kinds of behavior. They are as follows.
* `specTriggers`: the (required) array of `rspec`s which cause the `S` to be chosen rather than its siblings
* `f`: the second (required) parameter, either a Dragonfly action or a Python function reference. If it is a Dragonfly action, the appropriate Dragonfly `extra`s will be made available to it, as if it were spoken by itself. If it is a Python function, you have some options about how to deliver parameteres to the function when it is executed. See `parameters`, `user_spoken`, and `use_rspec` for details. (Also note, you can set all three, but there is an order of precedence if you do so: rspec, spoken, parameters -- only one will be used.)
* `parameters`: If `f` is a Python function, you may hard-code its parameters by setting `parameters` to an array. Example below.
* `use_spoken`: If set to True, `use_spoken` will cause an array of strings to be delivered to the `f` function when it executes. Example below. 
* `use_rspec`: If set to True, `use_rspec` will deliver the `rspec` string to the function as a single parameter. Example below.
* `consume`: If set to False, trigger commands will not be consumed by `ContextSeeker`s.
 
That's a lot, so let's see it in action.
```
from dragonfly import *

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R, S, L

def print_params_to_console(params):
  print(params)

class Times(MergeRule):
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
control.nexus().merger.add_global_rule(Times())
```
In this example, each of the `S` objects (except the first) delivers parameters to the print_params_to_console function differently. If you say "wait for noon time", an array of strings (specifically, ["some", "parameters"]) will be printed to the console. If you say "wait for midnight", the triggering rspec will  be printed ("midnight"). The "evening" option is the most interesting though. If you say "wait for evening", an array containing "wait", "for", and "evening" will be printed. However, if you say, "wait for", and then separately say "evening", an array containing only "evening" will be printed.

###AsynchronousAction
TODO: AsynchronousAction, progressive examples

##Pre-made Rules

Out-of-the-box, Caster gives the user new mouse navigation commands (see the Mouse page), text formatting and navigation commands, and programming-language specific rules. (See the Quick Reference for more details.) Unlike Dragonfly, Caster is targeted at programmers specifically, and so more technical knowledge is assumed of its user base.

##Modifying the Pre-made Rules

If you want to modify the pre-made ruleset, there are a few ways to go about it. Of course, you could just edit the source, but then you'd have to deal with merge conflicts when updating to newer versions of Caster. There are two ways to get around this:
* **Make a copy in the safe zone.** (1) Copy the file you'd like to change into your `caster/user` folder. (2) Disable the original rule in your `settings.json` file. (3) Give the new MergeRule a `pronunciation` which is distinct from that of the original. For example, if you're modifying java.py, give the new Java rule a `pronunciation` of "my java" rather than "java". 
* **Use rule filters.** This is the recommended way. Rule filters allow you to change any part of any rule, either at boot time or when the rule is activated ("merge time"). See the Rule Filters section of the CCR page for more details.

##Rule Filters
TODO: explanation, progressive examples
