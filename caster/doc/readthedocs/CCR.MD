# Continuous Command Recognition

**Contents**

* [Introduction](#introduction)
* [How It Works](#how-it-works)
* [Adding and Editing CCR Modules](#adding-and-editing-ccr-modes)
* [Non-CCR Sections in CCR Modules](#non-ccr-sections-in-ccr-modules)

***
## Introduction
For an introduction to CCR, check out [this video](http://www.youtube.com/watch?v=g3c5H7sAbBQ). The short version is, CCR allows you to speak sequential commands without pauses between them, greatly speeding up your ability to use commands in general.

## CCR In Caster
### Command Sets
Caster groups sets of CCR commands together so that they can be de/activated together. For example, you might want to turn Python and SQL on at the same time, but then switch over to C++ and SQL. To activate a command set, you say `enable <something>` where `<something>` is the name of the set. So, saying `enable Python` turns on Python.

### Command Standards and Compatibility
Caster also has a standard set of language command words ("specs"). For instance, "if" is the same word ("iffae" at time of writing) for Python, C++, Rust, etc. This reduces cognitive load required to program by voice. You don't have to re-learn all of the basic commands for each language you want to use.

However, this also creates the need for compatibility checking. For example, suppose you said `enable Python` to enable Python, then `enable C plus plus` to enable C++. If you then said `iffae` to get Caster to output an "if" statement, would you mean the Python if statement or the C++ if statement? Caster's default behavior is to shut off incompatible command sets, favoring the latest one you activated. So, in the Python/C++ example, Python would get disabled and C++ would remain active. This can be changed (see Filter Functions).

### Types of Rules
There are different kinds of Dragonfly and Caster rules which can be created or modified. Each rule is either a single command or a command set. These types include:

* **Rule, CompoundRule, MappingRule**: the original Dragonfly rule types. These can be used with Caster, but not for CCR.
* **MergeRule**: the basic Caster CCR building block. It is similar to Dragonfly's MappingRule, but has a few extra properties.
* **SelfModifyingRule**: this is a type of MergeRule which modifies its own command set based on some kind of user input. NodeRule, VanillaAlias, ChainAlias, and HistoryRule are all SelfModifyingRules.

We'll go into more detail on the differences between these rules elsewhere. For now, know that most rules used for CCR in Caster extend MergeRule.

### How to Add and Modify Rules
If you'd like to add rules for new languages or popular libraries for languages, you should create them in the `lib/ccr/` folder. If you want to add a custom command set, say, for work, you should put it in the `user/rules/` folder. This folder is ignored by Git, so you won't upload it if/when you commit other changes.

If you want to personalize existing command sets, you can use filter functions. Filter functions let you instruct Caster as to how it should modify command sets either at boot or at runtime when command sets change (for example, when you say `enable Python`).

### Filter Functions
There are nine points at which Caster builds or rebuilds its CCR command sets:

* Boot time: (1) base rule, (2, 3) self modifying rules, (4) app rules
* Run time: (5) base rule, (6, 7) self modifying rules, (8) app rules
* Self modifying rule change time (9)

Let's go through these.

**Boot Time**: At boot, Caster checks `bin/data/ccr.json` to see what you have enabled. It then takes all global rules (MergeRules which do not have an AppContext) and combines (1) them, one by one. At each intersection of two rules (each "merge"), you have the opportunity to change how the merge happens via filter functions. Caster then checks active SelfModifyingRules for compatibility both against the base (global rules) rule (2) and against the other active SelfModifyingRules (3). Finally, when the base + selfmodifyingrules is done merging, one copy of it is made for each app rule (MergeRule with an AppContext) and the copy is merged with a copy of the app rule. The original base rule is also given a context which is the inverse of all of the other contexts. That is, the base rule will run everywhere except in any of the app rules because the app rules each have their own copy of the base rule merged into them.

**Run Time**: The run time merge process is basically the same as the boot time merge process except for the creation of the base rule. Instead of creating it from scratch, the current base rule is used. If the user is enabling a command set, that command set gets compatibility-checked and then merged in (possibly knocking one or more others out unless filter functions specify otherwise). If the user is disabling a command set, that command set's commands are removed from the base rule and then the base rule is rebuilt (again, doing merges at each step of the rebuilding process). Then SelfModifyingRules, then app rules, just as at Boot.

**SelfModifyingRule Change Time**: If a SelfModifyingRule ("SMR") changes its command set, the base rule will remain untouched, but it will still be checked against the new SMR command set, and the new SMR command set will be checked against other active SMR command sets.

