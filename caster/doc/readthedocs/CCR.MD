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
