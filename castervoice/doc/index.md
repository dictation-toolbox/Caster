# Caster

[Caster](http://dictation-toolbox.github.io/caster/) is a collection of tools aimed at enabling programming and accessibility entirely by voice built upon the [Dragonfly](https://github.com/dictation-toolbox/dragonfly) API. Note that the current version of the ReadTheDocs page is based on the [`develop`](https://github.com/dictation-toolbox/Caster/tree/develop) branch so there may be features described here that do not work if you are on the [`master`](https://github.com/dictation-toolbox/Caster/tree/master) branch.

- Videos by the Caster Community.
    - [Caster Demo](https://www.youtube.com/watch?v=oIwh3z2jXD4)
    - [VimGolf and Project Euler](https://www.youtube.com/watch?v=T1bKAqDhH_E)
    - [Dictating maths into scientific notebook](https://www.youtube.com/watch?v=oq8EoPu0cGY&t=3s) and [Dictating math by voice using Caster](https://www.youtube.com/watch?v=z-iHvPmjcas)

- [Instructions for installing](Installation.md)
- [Quick reference](CasterQuickReference.pdf): commands to get started with.
- Documentation on Caster [[ReadTheDocs](http://caster.readthedocs.org/en/latest/)] [[YouTube](https://www.youtube.com/channel/UC2qZzmCj_5ZKkTa3i9X1LCg)] and Dragonfly [[ReadTheDocs](https://dragonfly2.readthedocs.io/en/latest/)] 
- Caster Command Reference Guides 
    - [Caster](CasterQuickReference.pdf) - Universal navigation and editing - These commands are active all the time, and provide input commands for letters, numbers and punctuation, as well as the ability to easily manipulate windows and text. 
        - `window right` moves the active window to the right-hand side of the screen.
        - `prekris` inserts a pair of brackets `()` and moves the cursor inside them.
        - `shackle` selects the current line.
    - [Applications](readthedocs/Application_Commands_Quick_Reference.md) - Application specific control - These commands are only activated when a particular program is the active window, and they provide support for text editors, IDEs, web browsers etc. For example, while the Sublime text editor is the active window, saying
        - `find` will execute a `ctrl-f` keystroke, bringing up the find and replace prompt,
        - `open file` will execute a `ctrl-o` keystroke,
        - `edit next <n>` - `ctrl-d` n times, selecting the next n instances of the currently selected word.
    - [Program Languages](readthedocs/CCR_languages_Quick_Reference.md) - Language specific coding - These modules are activated and deactivated with the `enable/disable <language>` voice command. For example, saying `enable python`. 
        - `for loop` which will insert `for i in range(0, ):`
        - `print to console` - `print()`
        -  `open file` -  `open('filename', 'r') as f:`
  - [Contributing / How can I help?](Contributing.md)
  - Need support or just curious? Join our community at [![Join the chat at https://gitter.im/synkarius/caster](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/synkarius/caster?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) or [Discord](https://discord.gg/9eAAsCJ) for voice chat.
  - The [Voice Index](readthedocs/Voice%20Index/) is a curated source of information: Videos, Blogs, Repositories, Presentations, etc related to Dragonfly, voice programming, and accessibility.

# Feature List

* [Easy Setup](Installation.md) and Configurable Settings

* Customize commands(Specs) and their actions via [simplified filter rules](readthedocs/CCR/#rule-filters-simplified) and [filter rules](readthedocs/examples/rules/Caster%20Rules/#rule-filters)([code](https://github.com/dictation-toolbox/caster/tree/master/caster/user/filters/examples)).

* Compatible Speech Recognition Engines

    *  [Dragon NaturallySpeaking](https://www.nuance.com/dragon.html) v13 and higher
    *  [Windows Speech Recognition](https://support.microsoft.com/en-us/help/17208/windows-10-use-speech-recognition)

* Supported Programming [Languages](readthedocs/CCR_languages_Quick_Reference.md) - Enhanced by Caster's [Continues Command Recognition](readthedocs/CCR/) - [Demo](https://www.youtube.com/watch?v=Obdegwr_LFc&index=5&list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc)

    *  Python, Java, Bash, C++, C#, Rust, Go, HTML, CSS, JavaScript, SQL, Dart, Latex , Matlab, R, Prolog, VHDL, and Haxe

* Supported [Software](readthedocs/Application_Commands_Quick_Reference.md) 

    * IDEs/Editors: Microsoft Visual C++, Visual Studio, Eclipse, Jetbrains IDEs, Emacs, Sublime, Atom, Visual Studio Code, Notepad++, FlashDevelop, Sql Developer, and SQL Server Management Studio
    * Development Tools: Command Prompt, GitBash, KDiff3
    * Statistics: RStudio and lyx
    * Browsers: Firefox, Chrome and Internet Explorer
    * Applications: Foxit Reader, Gitter, Microsoft Word, fman and Total Commander

* [Editing and Navigation](CasterQuickReference.pdf)

    - Four additional [mouse navigation modes](readthedocs/Mouse/): curse, douglas, legion, and rainbow - [Demo](https://www.youtube.com/watch?v=UISjQBMmQ-I&feature=youtu.be)
    - Text/line navigation commands, text formatting commands
    - Alphabet, numbers, punctuation input commands
    - Commands to interact with generic File Dialogues.

* Utilize Powerful Commands

    * "[Alias](readthedocs/Alias/)" Commands - on-the-fly commands created by highlighting stuff
    * "[Record From History](https://www.youtube.com/watch?v=wWDtsrIQ1pc&list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc)" - turn previously spoken commands into a voice macro 

* Third-party Integrations

    - [Sikulix](http://sikulix.com/) - v1.1.2: Automates anything you see on the screen of your desktop computer. - [Demo](https://youtu.be/RFdsD2OgDzk?list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc&t=512)
    - [Aenea](https://github.com/dictation-toolbox/aenea) - A client-server library for using voice macros from Dragon NaturallySpeaking and Dragonfly on remote/non-windows hosts.

* Caster extends the Dragonfly API for even more powerful commands.

    * The [Context Stack](readthedocs/ContextStack/) - Create asynchronous and context seeking commands
    * Spec reduction via [NodeRule](readthedocs/NodeRule/)
