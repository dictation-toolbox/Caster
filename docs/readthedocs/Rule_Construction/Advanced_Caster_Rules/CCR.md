# Continuous Command Recognition

**Contents**

- [Introduction](#introduction)
- [CCR in Caster](#ccr-in-caster)
  - [Command Sets](#command-sets)
  - [Command Standards and Compatibility](#command-standards-and-compatibility)
  - [Types of Rules](#types-of-rules)
  - [Other Features of MergeRule](#other-features-of-mergerule)
  - [How to Register Caster CCR Rules](#how-to-register-caster-ccr-rules)

------

## Introduction

For an introduction to CCR, check out [this video](http://www.youtube.com/watch?v=g3c5H7sAbBQ). The short version is: CCR allows you to speak sequential commands without pauses between them, greatly speeding up your ability to use commands in general.

## CCR In Caster

### Command Sets

Caster groups sets of CCR commands together so that they can be de/activated together. For example, you might want to turn Python and SQL on at the same time, but then switch over to C++ and SQL. To activate a command set, you say `enable <something>` where `<something>` is the name of the set. So, saying `enable Python` turns on Python.

### Command Standards and Compatibility

Caster also has a standard set of language command words ("specs"). For instance, "if" is the same word ("iffae" at time of writing) for Python, C++, Rust, etc. This reduces cognitive load required to program by voice. You don't have to re-learn all of the basic commands for each language you want to use.

However, this also creates the need for compatibility checking. For example, suppose you said `enable Python` to enable Python, then `enable C plus plus` to enable C++. If you then said `iffae` to get Caster to output an "if" statement, would you mean the Python if statement or the C++ if statement? Caster's default behavior is to shut off incompatible command sets, favoring the latest one you activated. So, in the Python/C++ example, Python would get disabled and C++ would remain active. This can be changed (see [classic_merging_strategy.py](https://github.com/dictation-toolbox/Caster/tree/master/castervoice/lib/merge/ccrmerging2/merging)).

### Types of Rules

There are different kinds of Dragonfly and Caster rules which can be created or modified. Each rule is either a single command or a command set. These types include:

- **Rule, CompoundRule, MappingRule**: the original Dragonfly rule types. These can be used with Caster but not for CCR.
- **MergeRule**: the basic Caster CCR building block. It is similar to Dragonfly's MappingRule but has a few extra properties.
- **SelfModifyingRule**: this is a type of MergeRule which modifies its own command set based on some kind of user input. NodeRule, Alias, ChainAlias, and HistoryRule are all SelfModifyingRules.

We'll go into more detail on the differences between these rules elsewhere. For now, know that most rules used for CCR in Caster extend MergeRule.

### Rule Transformers  - Out of date - 

ToDo: Update the concepts of runtime and boot time according to the new CCR Merger paradigm.

There are nine points at which Caster builds or rebuilds its CCR command sets:

- Boot time: (1) base rule, (2, 3) self modifying rules, (4) app rules
- Run time: (5) base rule, (6, 7) self modifying rules, (8) app rules
- Self modifying rule change time (9)

Let's go through these.

**Boot Time**: At boot, Caster checks `.caster\data\ccr.toml` to see what you have enabled. It then takes all global rules (MergeRules which do not have an AppContext) and combines (1) them, one by one. At each intersection of two rules (each "merge"), you have the opportunity to change how the merge happens via transformers. Caster then checks active SelfModifyingRules for compatibility both against the base (global rules) rule (2) and against the other active SelfModifyingRules (3). Finally, when the base + selfmodifyingrules is done merging, one copy of it is made for each app rule (MergeRule with an AppContext) and the copy is merged with a copy of the app rule. The original base rule is also given a context which is the inverse of all of the other contexts. That is, the base rule will run everywhere except in any of the app rules because the app rules each have their own copy of the base rule merged into them.

**Run Time**: The run time merge process is basically the same as the boot time merge process except for the creation of the base rule. Instead of creating it from scratch, the current base rule is used. If the user is enabling a command set, that command set gets compatibility-checked and then merged in (possibly knocking one or more others out unless rule filters specify otherwise). If the user is disabling a command set, that command set's commands are removed from the base rule and then the base rule is rebuilt (again, doing merges at each step of the rebuilding process). Then SelfModifyingRules, then app rules, just as at Boot.

**SelfModifyingRule Change Time**: If a SelfModifyingRule ("SMR") changes its command set, the base rule will remain untouched, but it will still be checked against the new SMR command set, and the new SMR command set will be checked against other active SMR command sets.

### Other Features of MergeRule

MergeRule has a handful of class-level properties which can be defined to enable certain behavior.

- `pronunciation`: This property allows me to change which word I can use in the `enable`/`disable` commands. For example, if my MergeRule-extending class is called `NYCCommands`, I can set `pronunciation="new york city"` in order to be able to say `enable new york city`.
- `non`: Suppose you want a non-CCR rule activated alongside your CCR rule. For instance, let's say there are some Python commands you want available while you're coding in Python, but which you know you'll never use as part of a command sequence and which you don't want in the CCR command set for performance / phonetic distinctness reasons. You can define `non` as the class of that rule, and it will be instantiated and activated alongside the MergeRule you define it on. The same thing works for App CCR rules. These definitions are defined in Companion Rules.

### How to Register Caster CCR Rules

In order to make any new rules you might create available to the CCRMerger, you must register them as follows:

```python
# Global Rules:
def get_rule():
    details =  RuleDetails(ccrtype=CCRType.GLOBAL)
    return SomeRule1, details

# App Rules:
def get_rule():
    details = RuleDetails(ccrtype=CCRType.APP, executable="eclipse", title="application title")
    return SomeRule2, details

# Self Modifying Rules (SMR):
def get_rule():
    details = RuleDetails(ccrtype=CCRType.SELFMOD)
    return SomeRuleSMR, details

```

Both MergeRules and SelfModifyingRules may also be added to Dragonfly Grammars if there is no need for CCR. MergeRules added as such will operate no differently than MappingRules.
