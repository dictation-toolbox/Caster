# Caster

[![Travis Build Status](https://travis-ci.org/dictation-toolbox/Caster.svg?branch=master)](https://travis-ci.org/dictation-toolbox/Caster) [![Documentation Status](https://readthedocs.org/projects/caster/badge/?version=latest)](https://caster.readthedocs.io/en/latest/?badge=latest) ![GitHub top language](https://img.shields.io/github/languages/top/dictation-toolbox/Caster)[![https://github.com/dictation-toolbox/Caster/blob/master/LICENSE](https://img.shields.io/badge/license-GNU-informational)](https://matrix.to/#/!KOGBGqVOBKJjKLgFUY:matrix.org?via=matrix.org)

​	[Caster](https://github.com/dictation-toolbox/Caster) gives you the power to control your computer by voice. Take control of your applications, games, mouse and keyboard to augment your workflow for every day activities or as an accessibility tool to develop applications entirely by voice built upon the [Dragonfly](https://github.com/dictation-toolbox/dragonfly) framework.  

**Note for PyPi Users**: The PIP package is (_Alpha_). Do not use the PIP install. Alternatively use this [Master Branch](https://github.com/dictation-toolbox/Caster) with classic install for the best feature experience.

- Videos by the Caster Community:

  - [Caster voice coding: Advent of Code 2018](https://youtu.be/oDsMGroASSw?t=3) - Programming with Go
  - [VimGolf and Project Euler](https://www.youtube.com/watch?v=T1bKAqDhH_E)
  - [Dictating maths into scientific notebook](https://www.youtube.com/watch?v=oq8EoPu0cGY&t=3s) and [Dictating math by voice using Caster](https://www.youtube.com/watch?v=z-iHvPmjcas)
  
- Read the [Frequently Asked Questions - FAQ](https://caster.readthedocs.io/en/latest/readthedocs/meta/Caster_FAQ/)

- [Getting started with Caster - ReadTheDocs](https://caster.readthedocs.io/en/latest/readthedocs/Getting_Started/Getting_Started_Overview/)

- [How to Speak Code](https://caster.readthedocs.io/en/latest/readthedocs/Getting_Started/How_to_Speak_Code/How_to_Speak_Code_Intro/) - Example Document

- Caster Command Reference Guides:

  - [Caster](https://github.com/dictation-toolbox/Caster/blob/master/CasterQuickReference.pdf) - Universal navigation and editing -  These voice commands are active all the time and provide input commands for letters, numbers, and punctuation, as well as the ability to easily manipulate windows and text. 
    - `window right` moves the active window to the right-hand side of the screen.
    - `prekris` inserts a pair of brackets `()` and moves the cursor inside them.
    - `shackle` selects the current line
  - [Applications](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Application_Commands_Quick_Reference/) - Application specific control - These commands are only activated when a particular program is the active window, and they provide support for text editors, IDEs, web browsers etc. For example, while the Sublime text editor is the active window, saying
    - `find` will execute a `ctrl-f` keystroke, bringing up the find and replace prompt,
    - `open file` will execute a `ctrl-o` keystroke,
    - `edit next <n>` - `ctrl-d` n times, selecting the next n instances of the currently selected word.
  - [Program Languages](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/CCR_languages_Quick_Reference/) - Language specific coding - These modules are activated and deactivated with the `enable/disable <language>` voice command. For example after saying `enable python`, the following commands become available for dictation: 
    - `for loop` which will insert `for i in range(0, ):`
    - `print to console` - `print()`
    - `open file` -  `open('filename', 'r') as f:`

- Application or Language not supported? 

  [Make your own Dragonfly and Caster rules](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Intro_Into_Rules_and_Grammars/) augmented by [Development Commands](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/CCR_languages_Quick_Reference/#VoiceDevCommands)

- [Contributing / How can I help?](https://caster.readthedocs.io/en/latest/Contributing/)

- Do you want to financially support Caster development? 
  Donate at [![IssueHunt](https://img.shields.io/badge/-IssueHunt-blue)](https://issuehunt.io/r/dictation-toolbox/Caster)

- Need support or just curious? Join our community at [![Gitter](https://img.shields.io/gitter/room/dictation-toolbox/Caster?label=Chat)](https://gitter.im/dictation-toolbox/home) [![Discord](https://img.shields.io/discord/431142802005688340?label=Discord)](https://discord.gg/9eAAsCJ) [![Matrix](https://img.shields.io/matrix/caster:matrix.org?label=Matrix%20Chat&server_fqdn=matrix.org)](https://matrix.to/#/+dictation-toolbox:matrix.org)

- The [DictationToolbox.org](https://dictation-toolbox.github.io/dictation-toolbox.org/) (WIP) is a curated webpage of information related to voice programming and accessibility. Content Includes: User Tips, Hardware, Videos, Blogs, Repositories, Presentations, and etc. Pull requests welcome!

# Feature List 

- Configurable Settings in `C:\Users\%USERNAME%\AppData\Local\caster`
- Customize Commands aka `Specs` via [Simplified Transformers](https://caster.readthedocs.io/en/latest/readthedocs/Customize_Caster/Customizing_Starter_Rules/)
- Compatible Speech Recognition Engines

  - [Dragon NaturallySpeaking](https://www.nuance.com/dragon.html) v13 and higher 
  - [Kaldi](https://dragonfly2.readthedocs.io/en/latest/kaldi_engine.html)
  - [Windows Speech Recognition](https://support.microsoft.com/en-us/help/17208/windows-10-use-speech-recognition)

- Supported [Applications](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Application_Commands_Quick_Reference/)

  - IDEs/Editors: Microsoft Visual C++, Visual Studio, Eclipse, Jetbrains IDEs, Emacs, Sublime, Atom, Visual Studio Code, Notepad++, FlashDevelop, Sql Developer, SQL Server Management Studio
  - Development Tools: Command Prompt, GitBash, KDiff3
  - Statistics: RStudio 
  - Word Processor: lyx, Microsoft Word, Typora
  - Browsers: Firefox, Chrome, Internet Explorer
  - Git Client:  Github Desktop 
  - Chat: Microsoft Teams, Gitter
  - Applications: Foxit Reader, fman, Total Commander, Outlook, Excel, Unity3D
- Supported [Programming Languages](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/CCR_languages_Quick_Reference/) - Enhanced by Caster's [Continuous Command Recognition](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Caster_Rules/CCR/) - [Demo](https://www.youtube.com/watch?v=Obdegwr_LFc&index=5&list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc)

  - Python, Java, Bash, C++, C#, Rust, Go, HTML, CSS, JavaScript, SQL, Dart, Latex , Matlab, R, Prolog, VHDL, and Haxe
- [Editing and Navigation](https://github.com/dictation-toolbox/Caster/blob/master/CasterQuickReference.pdf)
- Five additional [mouse navigation modes](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Mouse/): curse, sudoku, douglas, legion, and rainbow - [Demo](https://www.youtube.com/watch?v=UISjQBMmQ-I&feature=youtu.be)
  - [Text navigation commands](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Text_Manipulation/) - [Demo](https://www.youtube.com/watch?v=xj8IzNlfM70), Text formatting commands
  - Alphabet, numbers, punctuation input commands
  - Commands to interact with generic File Dialogues.

- Utilize Powerful Commands

  - "[Alias](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Alias/)" Commands - on-the-fly commands created by highlighting stuff
  - "[Record From History](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Record_Macros/)" - turn previously spoken commands into a voice macro 

- Third-party Integrations

  - [Sikulix](http://sikulix.com/) - [Setup](https://caster.readthedocs.io/en/latest/readthedocs/Third-party_Integrations/Sikuli/): Automates anything you see on the screen of your desktop computer. - [Demo](https://youtu.be/RFdsD2OgDzk?list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc&t=512)
  - [Aenea](https://github.com/dictation-toolbox/aenea) - [Setup](https://caster.readthedocs.io/en/latest/readthedocs/Third-party_Integrations/Aenea/): A client-server library for using voice macros from Dragon NaturallySpeaking and Dragonfly on remote/non-windows hosts.
  - [Autohotkey](https://www.autohotkey.com/): A scripting language that allows the automation of various tasks in Windows. Simply install the latest version. If installed, it can speed up some commands by a few seconds - e.g. [checking out or updating a pull request from github](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Commands/Application_Commands_Quick_Reference/#google-chrome).

- Caster extends the Dragonfly API for even more powerful commands.

  - The [Context Stack](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Caster_Rules/ContextStack/) - Create asynchronous and context seeking commands
  - Spec reduction via [NodeRule](https://caster.readthedocs.io/en/latest/readthedocs/Rule_Construction/Caster_Rules/NodeRule/)
