# What can it do?
Caster implements three main types of command:

## Language specific coding commands
Caster contains continuous command recognition (CCR) modules for a number of languages, and it is simple to add new ones. These modules are activated and deactivated with the `enable/disable <language>` voice command. For example, saying

`enable python`

will activate the Python module, giving access to commands like

* `for loop` which will insert `for i in range(0, ):`
* `print to console` - `print()`

**A complete list** of supported languages and available commands can be found in the [CCR languages quick reference](readthedocs/CCR%20languages%20Quick%20Reference.md)

## Context specific control commands
These commands are only activated when a particular program is the active window, and they provide support for text editors, IDEs, web browsers etc. For example, while the Sublime text editor is the active window, saying

* `find` will execute a `ctrl-f` keystroke, bringing up the find and replace prompt,
* `open file` will execute a `ctrl-o` keystroke,
* `edit next <n>` will execute `ctrl-d` n times, selecting the next n instances of the currently selected word.

**A complete list** of supported applications and available commands can be found in the [Application commands quick reference](readthedocs/Application%20Commands%20Quick%20Reference.md)

## Universal navigation and editing commands
These commands are active all the time, and provide input commands for letters, numbers and punctuation, as well as the ability to easily manipulate windows and text. For example

* `window right` moves the active window to the right-hand side of the screen,
* `prekris` inserts a pair of brackets `()` and moves the cursor inside them,
* `shackle` selects the current line.

**A complete list** of these commands can be found in the [Quick reference](../../CasterQuickReference0.5.8.pdf)

## Chaining them together
With CCR, multiple commands can be executed in quick succession, allowing quick code dictation. For example,

* `print to console quotes tie bow hello world clamor` - `print("Hello World!")`
* `shin ross wally clear` - `select to the end of the line, delete`
* `queue lease stoosh` - `copy the previous word/variable name`
