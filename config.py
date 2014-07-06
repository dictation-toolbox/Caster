#Based heavily on the work of https://github.com/poppe1219/dragonfly-scripts/blob/master/lib/config.py

import os
import json
import paths, utilities

CONFIG_PATH = paths.get_config_path()
CONFIG = {}  # Empty, default config.

def save_config():
    global CONFIG
    global CONFIG_PATH
    utilities.save_json_file(CONFIG, CONFIG_PATH)

def load_config():
    global CONFIG
    global CONFIG_PATH
    CONFIG = utilities.load_json_file(CONFIG_PATH)
    init_default_values()

def init_default_values():# new languages must be added here and in paths.py
    global CONFIG
    valueChangeCount = 0
    defaultValues = [
        ("java", False),
        ("python", False),
        ("html", False),
        ("pascal", False),
        ("alphabet", False)
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