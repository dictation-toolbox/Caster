# Continuous Command Recognition

**Contents**
* [Introduction](#introduction)
* [Rationale](#rationale)
* [How It Works](#how-it-works)
* [Adding and Editing CCR Modules](#adding-and-editing-ccr-modes)
* [Non-CCR Sections in CCR Modules](#non-ccr-sections-in-ccr-modules)

***
## Introduction
For an introduction to CCR, check out [this video](http://www.youtube.com/watch?v=g3c5H7sAbBQ). The short version is, CCR allows you to speak sequential commands without pauses between them, greatly speeding up your ability to use commands in general.

## Rationale
CCR really matters with programming because you want to be able to speak long chains of code into existence. The original [_multiedit.py](https://code.google.com/p/dragonfly-modules/source/browse/trunk/command-modules/_multiedit.py) module by Christo Butcher was pretty powerful, but it had some drawbacks. You couldn't selectively enable and disable sections of it. It was all or nothing. Also, it didn't allow for multiple programming languages which use the same keywords. The Caster version improves upon the original by fixing these two problems.

## How It Works
All CCR modules (.txt files) are stored in the [bin/data/ccr folder](https://github.com/synkarius/caster/tree/master/caster/bin/data/ccr). When you say, for example "enable html", HTML is added to the list of enabled modes (provided that it is compatible with everything else already enabled). The list is then read and all of the text files of the enabled modes are combined into one large text file and interpreted by Dragonfly via the original _multiedit.py method.

Compatibility is handled by checking the mode(s) being enabled against the already enabled modes for identical commands, extras, or defaults. If duplicates in any of these categories are found, the new mode is incompatible, and whatever old modes caused the incompatibility are disabled.

## Adding and Editing CCR Modules
Adding a new CCR mode is simple: add a new text file to the data/ccr folder which follows the _multiedit.py text format and the following naming convention:
* The file must be named **config\<something\>.txt**. \<something\> will be the word that you speak to enable that mode in the enable and disable commands. For example, to enable the commands in confightml.txt, you would say "enable html".

## Non-CCR Sections in CCR Modules
Some modules have non-CCR sections in them which are activated when the CCR parts are. This functionality is intended for cases where those extra commands should only be available at the same time as the CCR commands in that module, but there's no need for them to be chainable, and for accuracy's sake it's actually undesirable for them to be chainable. The navigation module, for instance, has many non-CCR commands in it. See everything under "cmd.ncactive=True".