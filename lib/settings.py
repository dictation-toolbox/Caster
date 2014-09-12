#Based heavily on the work of https://github.com/poppe1219/dragonfly-scripts/blob/master/lib/config.py
from lib import utilities
import paths

SETTINGS_PATH = paths.SETTINGS_PATH
SETTINGS = {}  # Empty, default config.
SPEAK = False # to do,: add this value to the config
ELEMENT_VERSION="Element v.04"
DISPEL_VERSION="Dispel v.02"

def save_config():
    global SETTINGS
    global SETTINGS_PATH
    utilities.save_json_file(SETTINGS, SETTINGS_PATH)

def load_settings():
    global SETTINGS
    global SETTINGS_PATH
    SETTINGS = utilities.load_json_file(SETTINGS_PATH)
    init_default_values()

def init_default_values():
    global SETTINGS
    valueChangeCount = 0
    defaultValues = []
    for c in utilities.get_list_of_individual_config_files():
        defaultValues.append((c,False))
    for (name, value) in defaultValues:
        if not name in SETTINGS.keys():
            SETTINGS[name] = value
            valueChangeCount += 1
    if valueChangeCount > 0:
        save_config()

def get_settings():
    global SETTINGS
    return SETTINGS