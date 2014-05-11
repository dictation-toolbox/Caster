
#Based heavily on the work of https://github.com/poppe1219/dragonfly-scripts/blob/master/lib/config.py

"""Configuration module, saves the config in a json file.

Keeping the configuration in a json file has the advantage that it can be
changed in runtime by voice commands.
For instace, the dynamic grammars saves their state of enabled or disabled in
runtime. If Natlink is reloaded or Dragon is restarted, the previous state is
loaded and the previously enabled dynamic grammars are enabled again.

The advantage of using a flat structure in the config, as opposed to a nested,
is that the code for reading and writing becomes very simple.

Example config:
{
    "aenea.enabled": false,
    "aenea.path": null,  // Set path if Aenea is outside MacroSystem dir.
    "dynamics.bash.enabled": true,
    "dynamics.css.enabled": false,
    "dynamics.git.enabled": false,
    "dynamics.html.enabled": false,
    "dynamics.javascript.enabled": false,
    "dynamics.python.enabled": false,
    "system.base_path": "C:\\Natlink\\Natlink\\MacroSystem"
}

If you want to set a value like a path, you have to do that manually in the
json file.

"""
import os
import sys
import json

WORKING_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = WORKING_PATH + "\\config.json"
CONFIG = {}  # Empty, default config.
print CONFIG_PATH

def save_config():
    global CONFIG
    global CONFIG_PATH
    try:
        configData = json.dumps(CONFIG, sort_keys=True, indent=4,
            ensure_ascii=False)
        with open(CONFIG_PATH, "w+") as f:
            f.write(configData)  # Save config to file.
    except Exception as e:
        print("Could not save config file: %s" % str(e))


def load_config():
    global CONFIG
    global CONFIG_PATH
    try:
        if os.path.isfile(CONFIG_PATH):  # If the config file exists.
            with open(CONFIG_PATH, "r") as f:
                CONFIG = json.loads(f.read())  # Load saved configuration.
                init_default_values()
        else:  # If the config file does not exist.
            save_config()  # Save the default config to file.
    except Exception as e:
        print("Could not load config file: %s" % str(e))


def init_default_values():
    global CONFIG
    valueChangeCount = 0
    defaultValues = [
        ("aenea.enabled", False),
        ("aenea.path", None),
    ]
    for (name, value) in defaultValues:
        if not name in CONFIG.keys():
            CONFIG[name] = value
            valueChangeCount += 1
    if valueChangeCount > 0:
        save_config()


def get_config():
    global CONFIG
    return CONFIG


load_config()

# aeneaPath = CONFIG.get("aenea.path", None)
# if not aeneaPath:
#     path = os.path.dirname(os.path.abspath(__file__))
#     aeneaPath = os.path.split(path)[:-1]
# if not aeneaPath in sys.path:
#     sys.path.insert(0, aeneaPath)