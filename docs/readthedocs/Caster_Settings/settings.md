# Settings

Explanation of `settings.toml`. Caster settings can be edited in the following ways:

- Edited through a GUI. Say `launch caster settings`. Once done, say `complete` to save the file

- The settings file can be summoned manually by saying `bring me caster settings file` to your default editor for `.toml` files
  
  The following is an `example.toml` settings file with comments explaining the various settings. Some of the settings fields have been truncated for brevity as noted in the comments.

```toml
[Tree_Node_Path] # Paths for Node Tree Rules
SM_CSS_TREE_PATH = "C:\\Users\\Main\\AppData\\Local\\caster\\data\\sm_css_tree.toml"

[engine] # controls configuration of engine.
default_engine_mode = false #  Changes default mode when caster starts
engine_mode = "normal" # Currently implementfor DNS Only/DPI.
# Valid mic_mode options
# 'normal': dictation and command (Default: Only/DPI only)
# 'dictation': Dictation only 
# 'command': Commands only (Default: Other engines)
# 'numbers': Numbers only
# 'spell': Spelling only

default_mic = false # Changes default mic mode when caster starts
mic_mode = "on"
# 'on': mic is on # default
# 'sleeping': mic from the sleeping and can be woken up by command
# 'off': mic off and cannot be turned back on by voice. (DNS Only)

mic_sleep_timer_on = true 
mic_sleep_timer = 300 # A timer puts microphone to after X seconds after last successful recognition.
#DNS/DPI has its own built-in sleep mode timer defaults to 5 minutes. Caster mic sleep timer will not work as expected beyond DNS/DPI 5 #minutes default timer (microphone will go to sleep prematurely). if you increase the default timer to greater than 5 minutes. Anything under 5 minutes/300 seconds caster mic sleep timer will work as expected.

[formats] # Truncated - Control setting dictation formatting per programming language.
# Legend - Represents text formatting (capitalization and spacing) rules.
# Each language can hold two formats. You can have differen formats for classes and variables for example.

[formats."C plus plus"] # Language
# The first number is capitalization and the second is spacing.
secondary_format = [2, 1] 
text_format = [3, 1]

[formats."C sharp"]
secondary_format = [2, 1]
text_format = [3, 1]

#    Commands for capitalization:
#    1 yell - ALLCAPS
#    2 tie - TitleCase
#    3 Gerrish - camelCase
#    4 sing - Sentencecase
#    5 laws (default) - alllower

#   Commands for word spacing:
#    0 (default except Gerrish) - words with spaces
#    1 gum (default for Gerrish)  - wordstogether
#    2 spine - words-with-hyphens
#    3 snake - words_with_underscores
#    4 pebble - words.with.fullstops
#    5 incline - words/with/slashes

[hooks]
default_hooks = ["PrinterHook"] # Default hooks. Do not edit. 

[miscellaneous]
atom_palette_wait = 30 # Milliseconds to pause for atom palette functions
ccr_on = true # Toggle on and off all CCR commands regardless of grammar.
dev_commands = true # No longer used
history_playback_delay_secs = 1.0 # How fast the `playback` command replays from 'record from history'
hmc = true # Turns off GUI components of Caster
integer_remap_crash_fix = false # Unknown
integer_remap_opt_in = false # Unknown
keypress_wait = 50 # Configurable keypress outer pause wait from dragonfly
legion_vertical_columns = 30 # How many vertical lines are in the Legion MouseGrid
max_ccr_repetitions = 16 # How many CCR commands can uttered in a row. Affects grammar complexity
print_rdescripts = true # Prints out commands to the status window after dictation
short_integer_opt_out = false # Unknown
status_window_foreground_on_error = false # If Caster logs an error, the status window will appear for end user to evaluate error message
use_aenea = false # Enables aenea third-party integration

[online]
last_update_date = "2020-01-18" # Last time Caster looked for an Dragonfly update 
online_mode = true #  Disables all Caster features that utilize an internet connection 
update_interval = 7 #  Interval days between checking for updates

[paths] # Default generated paths: "." placeholder for empty path.
# Most of the settings here are auto generated which have been omitted except for the following.

AHK_PATH = "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe" # Change the location of AutoHotkey
REMOTE_DEBUGGER_PATH = "." # Path to remote debugger
SIKULI_IDE = "." # To set up Sikuli
SIKULI_RUNNER = "."
TERMINAL_PATH = "C:\\Program Files\\Git\\git-bash.exe" # Customized to your preferred git bash

# Auto generated
BASE_PATH = "D:\\Backup\\Library\\Documents\\Caster\\castervoice" # Caster source code 
USER_DIR = "C:\\Users\\Main\\AppData\\Local\\caster" # Caster user directory 

[python] # Unused: future feature.
automatic_settings = true
pip = "pip"
version = "python"

[sikuli] 
enabled = false # Toggle sikuli third-party integration 
version = "" # Sikuli Version
```
