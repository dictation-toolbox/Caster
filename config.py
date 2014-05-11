#Based heavily on the work of https://github.com/poppe1219/dragonfly-scripts/blob/master/lib/config.py

import os
import sys
import json

WORKING_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = WORKING_PATH + "\\config.json"
CONFIG = {}  # Empty, default config.

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
        ("java", False),
        ("python", False),
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