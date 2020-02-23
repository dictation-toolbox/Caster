# The Context Stack

Caster augments the Dragonfly command model via the context stack. The context stack is an object which stores Dragonfly commands as they are spoken, then decides how to execute them, and whether to execute them, based on its history of spoken commands. This enables a number of new features (command consumption, asynchronous and context seeking commands, status window hinting and confirmation, sophisticated "undo" behavior).

**New Actions**

- [RegisteredAction](#registeredaction)
- [ContextSeeker](#contextseeker)
- [AsynchronousAction](#asynchronousaction)

---

## RegisteredAction

A RegisteredAction wraps a Dragonfly action. When Dragonfly executes the RegisteredAction, an object representing it is passed to the context stack, which then figures out what to do with it. It is used as follows.

```python
"some spec":        RegisteredAction(Key("c-f"), rdescript="Find")
# RegisteredAction can be shortened to `R`
"some spec":        R(Key("c-f"), rdescript="Find")
```

RegisteredAction has a number of optional parameters which affect its processing in the context stack.

- `rspec` - registers this command as a key which is able to trigger specific behavior in ContextSeekers and AsynchronousActions
- `rdescript` - the description of this command which will appear in the status window
- `rundo` - another Dragonfly action which is used to undo the base action (not implemented yet)
- `show` - whether or not to show the `rdescript` in the status window.

## ContextSeeker

A ContextSeeker requires the context of other context stack actions in order to determine how it should execute. It can look backward at previously spoken commands, or not execute immediately and wait for future commands to be spoken.

Its constructor requires either or both of two lists, and has a bunch of optional parameters. The first list is a list of ContextLevels with which to look backward; the second is the same sort of list, with which to look forward.

**ContextLevel and ContextSet**

A ContextLevel is a set of possible outcomes which can be triggered by a RegisteredAction or other context stack action. Each outcome is called a ContextSet. Each ContextSet requires a set of trigger words to select it with, an outcome, and optionally some other parameters. It looks like one of these:

```python
ContextSet(["hello", "goodbye"], Text, "greeting"),
ContextSet(["banana"], myfunction, -1),
ContextSet(["apple"], otherfunction)
```

A few points about the ContextSet:

- `specTriggers` - The trigger words in the first parameter will be matched against the RegisteredActions' `rspec`. So if you have a RegisteredAction with `rspec="banana"`, it will trigger the second of the three ContextSets above. You could use either `rspec="hello"` or `rspec="goodbye"` to trigger the first.
- `f` - The second parameter, the outcome, can be a Python function or any of the following Dragonfly actions: Text, Key, Mimic, Function, Paste. It can also be `None` if you want outcome function to do nothing. (This is often useful as a default.)
- `parameters` - The first optional parameter, `parameters`, is a parameter or list of parameters which will be passed to the outcome function (the second parameter).
- `consume` - This is simply whether or not the triggering action should be executed. `True` means it shouldn't be executed.
- `use_spoken` - If True, the outcome function will receive the words the user spoke when they used the RegisteredAction which selected this ContextSet. This overrides `parameters`.
- `use_rspec` - Same as `use_spoken`, but instead of receiving the spoken words the outcome function will receive the RegisteredAction's rspec. This overrides `parameters` and `use_spoken`.

ContextLevel example:

```python
ContextLevel([
    ContextSet(["hello", "goodbye"], Text, "greeting"),
    ContextSet(["banana"], myfunction, -1),
    ContextSet(["apple"], otherfunction)
            ])
```

**Back To ContextSeeker**

A ContextSeeker can have multiple ContextLevels in both its backward list and its forward list. For each level added to the backward or forward list, a ContextSeeker will look backward or forward on the context stack one more command. For instance, if a ContextSeeker has two ContextLevels in its forward list, it will not execute until two more commands have been spoken after it, each of which can have some impact on how it executes via the ContextSets being selected by RegisteredActions' `rspec`s.

ContextLevel can be shortened to `L`. ContextSet can be shortened to `S`.

If a RegisteredAction command is spoken which selects none of the ContextSets for a given ContextLevel, that ContextLevel will default to the first ContextSet.

ContextSeeker optional parameters:

- `rspec` - same as RegisteredAction
- `rdescript` - same as RegisteredAction

**Some Examples**

Let's say we have these two functions.

```python
def close_last_spoken(spoken):
    first = spoken[0]
    Text("</"+first+">").execute()
def close_last_rspec(rspec):
    Text("</"+rspec+">").execute()
```

We could tie them into a MappingRule like this:

```python
"close last tag":               ContextSeeker([L(S(["cancel"], None),
                                                 S(["html spoken"], close_last_spoken, use_spoken=True),
                                                 S(["span", "div"], close_last_rspec, use_rspec=True))
                                               ]),
"html":                         R(Text("<html>"), rspec="html spoken"),
"divider":                      R(Text("<div>"), rspec="div"),
"span":                         R(Text("<span>"), rspec="span")
```

## AsynchronousAction

AsynchronousAction is a specialized kind of ContextSeeker. It only has one ContextLevel and one ContextSet, in the forward list, and it continually repeats its lone outcome until one of three things occurs.

1. the terminating command is spoken (the terminating command is any of the trigger words in the first ContextSet)
2. a success condition is met (the outcome function returns True)
3. it runs a predetermined number of times (set in the parameters)

AsynchronousAction optional parameters:

- `time_in_seconds` - time between repetitions of repeating function
- `repetitions` - max repetitions
- `rdescript` - same as RegisteredAction
- `blocking` - does it block other context stack actions until it completes

AsynchronousAction also has the special property that you can use `time_in_seconds` and `repetitions` as IntegerRefST extras in the spec, and they will override the defaults or whatever is set in the constructor.

Example AsynchronousActions:

```python
"press right repeatedly":        AsynchronousAction(L([S(["cancel", Key, "right"])]),
                                         repetitions=100, blocking=False),
"print time <time_in_seconds>":  AsynchronousAction(L([S(["stop"], fn_print_time)]))
```
