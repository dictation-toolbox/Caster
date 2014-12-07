
from lib import utilities
import paths


SETTINGS_PATH = paths.SETTINGS_PATH
SETTINGS = {"ccr":{}, "monitors":[]}  # Empty, default config.
SPEAK = False  # to do,: add this value to the config
ELEMENT_VERSION = "Element v.04"
DISPEL_VERSION = "Dispel v.02"
PBASE1="4dg62sQ$Pm&"
PBASE2="4dg62sQ4Pm7"
PBASE3="1Q2w3"
PBASE4="4"

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
    ccrNames = []
    for c in utilities.get_list_of_ccr_config_files():
        ccrNames.append((c, False))
    #
    if not "ccr" in SETTINGS.keys():  # enter
        SETTINGS["ccr"] = {}
        valueChangeCount += 1
    if not "last_monitor_was_flipped" in SETTINGS.keys():  # enter
        SETTINGS["last_monitor_was_flipped"] = False
        valueChangeCount += 1
    #
    for (name, value) in ccrNames:
        if not name in SETTINGS["ccr"]:  # .keys()
            SETTINGS["ccr"][name] = value
            valueChangeCount += 1
    if valueChangeCount > 0:
        save_config()

def get_settings():
    global SETTINGS
    return SETTINGS
