# Caster
[![Travis Build Status](https://travis-ci.org/dictation-toolbox/Caster.svg?branch=master)](https://travis-ci.org/dictation-toolbox/Caster) [![ReadTheDocs Build Status](https://readthedocs.org/projects/pip/badge/)](https://caster.readthedocs.io/en/latest/)

[Caster](https://github.com/dictation-toolbox/Caster)  is a collection of tools aimed at enabling programming and accessibility entirely by voice built upon the [Dragonfly](https://github.com/dictation-toolbox/dragonfly) API.

**Note for PyPi Users**: The PIP package is (_Alpha_). Do not use the PIP install. Alternatively use this [Master Branch](https://github.com/dictation-toolbox/Caster) with classic install for the best feature experience.

- Videos by the Caster Community.
  - [Caster Demo](https://www.youtube.com/watch?v=oIwh3z2jXD4)
  - [VimGolf and Project Euler](https://www.youtube.com/watch?v=T1bKAqDhH_E)
  - [Dictating maths into scientific notebook](https://www.youtube.com/watch?v=oq8EoPu0cGY&t=3s) and [Dictating math by voice using Caster](https://www.youtube.com/watch?v=z-iHvPmjcas)
- [Instructions for installing](https://caster.readthedocs.io/en/latest/Installation/)
- Documentation on Caster [[ReadTheDocs](https://caster.readthedocs.io/en/latest/)]and Dragonfly [[ReadTheDocs](https://dragonfly2.readthedocs.io/en/latest/)] 
- [How to Speak Code](https://caster.readthedocs.io/en/latest/readthedocs/Examples/Speaking/Examples/) - Example Document
- Caster Command Reference Guides 
  - [Caster](https://github.com/dictation-toolbox/Caster/blob/master/CasterQuickReference.pdf) - commands to get started with. Universal navigation and editing - These commands are active all the time, and provide input commands for letters, numbers and punctuation, as well as the ability to easily manipulate windows and text. 
    - `window right` moves the active window to the right-hand side of the screen.
    - `prekris` inserts a pair of brackets `()` and moves the cursor inside them.
    - `shackle` selects the current line.
  - [Applications](https://caster.readthedocs.io/en/latest/readthedocs/Application_Commands_Quick_Reference/) - Application specific control - These commands are only activated when a particular program is the active window, and they provide support for text editors, IDEs, web browsers etc. For example, while the Sublime text editor is the active window, saying
    - `find` will execute a `ctrl-f` keystroke, bringing up the find and replace prompt,
    - `open file` will execute a `ctrl-o` keystroke,
    - `edit next <n>` - `ctrl-d` n times, selecting the next n instances of the currently selected word.
  - [Program Languages](https://caster.readthedocs.io/en/latest/readthedocs/CCR_languages_Quick_Reference/) - Language specific coding - These modules are activated and deactivated with the `enable/disable <language>` voice command. For example say `enable python`. 
    - `for loop` which will insert `for i in range(0, ):`
    - `print to console` - `print()`
    - `open file` -  `open('filename', 'r') as f:`
- [Contributing / How can I help?](https://caster.readthedocs.io/en/latest/Contributing/)
- Do you want to financially support Caster development? 
  Donate at [![Bountysource](https://www.bountysource.com/badge/team?team_id=407907&style=bounties_posted)](https://www.bountysource.com/teams/caster-dictation/bounties?utm_source=Bountysource&utm_medium=shield&utm_campaign=bounties_posted) 
- [Making your own Dragonfly and Caster rules](https://caster.readthedocs.io/en/latest/readthedocs/Examples/Rule_Construction/) augmented by [Development Commands](https://caster.readthedocs.io/en/latest/readthedocs/CCR_languages_Quick_Reference/#VoiceDevCommands)
- Need support or just curious? Join our community at [![Join the chat at https://gitter.im/synkarius/caster](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dictation-toolbox/home) and [Discord](https://discord.gg/9eAAsCJ) for voice chat.
- The [DictationToolbox.org](https://dictation-toolbox.github.io/dictation-toolbox.org/) is a curated webpage of information related to voice programming and accessibility. Content Includes: User Tips, Hardware, Videos, Blogs, Repositories, Presentations, and etc. Pull requests welcome!

# Feature List

- Configurable Settings in `C:\Users\%USERNAME%\.caster`

- Customize Commands aka `Specs` and their actions via [Simplified Filter Rules](https://caster.readthedocs.io/en/latest/readthedocs/CCR/#rule-filters-simplified) and [Filter Rules](https://caster.readthedocs.io/en/latest/readthedocs/CCR/#Rule-Filters) (WIP). Filter Rules code examples can be found in `.caster\filters\examples`.

- Compatible Speech Recognition Engines

  - [Dragon NaturallySpeaking](https://www.nuance.com/dragon.html) v13 and higher
  - [Windows Speech Recognition](https://support.microsoft.com/en-us/help/17208/windows-10-use-speech-recognition)

- Supported [Programming Languages](https://caster.readthedocs.io/en/latest/readthedocs/CCR_languages_Quick_Reference/) - Enhanced by Caster's [Continuous Command Recognition](https://caster.readthedocs.io/en/latest/readthedocs/CCR/) - [Demo](https://www.youtube.com/watch?v=Obdegwr_LFc&index=5&list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc)

  - Python, Java, Bash, C++, C#, Rust, Go, HTML, CSS, JavaScript, SQL, Dart, Latex , Matlab, R, Prolog, VHDL, and Haxe

- Supported [Applications](https://caster.readthedocs.io/en/latest/readthedocs/Application_Commands_Quick_Reference/)

  - IDEs/Editors: Microsoft Visual C++, Visual Studio, Eclipse, Jetbrains IDEs, Emacs, Sublime, Atom, Visual Studio Code, Notepad++, FlashDevelop, Sql Developer, SQL Server Management Studio
  - Development Tools: Command Prompt, GitBash, KDiff3
  - Statistics: RStudio 
  - Word Processor: lyx, Microsoft Word, Typora
  - Browsers: Firefox, Chrome, Internet Explorer
  - Git Client:  Github Desktop 
  - Applications: Foxit Reader, Gitter, fman, Total Commander, Outlook, Excel

- [Editing and Navigation](https://github.com/dictation-toolbox/Caster/blob/master/CasterQuickReference.pdf)

  - Four additional [mouse navigation modes](https://caster.readthedocs.io/en/latest/readthedocs/Mouse/): curse, douglas, legion, and rainbow - [Demo](https://www.youtube.com/watch?v=UISjQBMmQ-I&feature=youtu.be)
  - [Text navigation commands](https://caster.readthedocs.io/en/latest/readthedocs/Text_Manipulation/) - [Demo](https://www.youtube.com/watch?v=xj8IzNlfM70), Text formatting commands
  - Alphabet, numbers, punctuation input commands
  - Commands to interact with generic File Dialogues.

- Utilize Powerful Commands

  - "[Alias](https://caster.readthedocs.io/en/latest/readthedocs/Alias/)" Commands - on-the-fly commands created by highlighting stuff
  - "[Record From History](https://caster.readthedocs.io/en/latest/readthedocs/Record_Macros/)" - turn previously spoken commands into a voice macro 

- Third-party Integrations

  - [Sikulix](http://sikulix.com/) - [Setup](https://caster.readthedocs.io/en/latest/readthedocs/Sikuli/): Automates anything you see on the screen of your desktop computer. - [Demo](https://youtu.be/RFdsD2OgDzk?list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc&t=512)
  - [Aenea](https://github.com/dictation-toolbox/aenea) - [Setup](https://caster.readthedocs.io/en/latest/readthedocs/Aenea/): A client-server library for using voice macros from Dragon NaturallySpeaking and Dragonfly on remote/non-windows hosts.
  - [Autohotkey](https://www.autohotkey.com/): A scripting language that allows the automation of various tasks in Windows. Simply install the latest version. If installed, it can speed up some commands by a few seconds - e.g. [checking out or updating a pull request from github](https://caster.readthedocs.io/en/latest/readthedocs/Application_Commands_Quick_Reference/#google-chrome).

- Caster extends the Dragonfly API for even more powerful commands.

  - The [Context Stack](https://caster.readthedocs.io/en/latest/readthedocs/ContextStack/) - Create asynchronous and context seeking commands
  - Spec reduction via [NodeRule](https://caster.readthedocs.io/en/latest/readthedocs/NodeRule/) (WIP)
