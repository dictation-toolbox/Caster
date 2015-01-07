import json
import os
import sys

SETTINGS = None

INISETPATH = 'C:/NatLink/NatLink/MacroSystem/bin/data/settings.json'

#titles
ELEMENT_VERSION = "Element v.10"
DISPEL_VERSION = "Dispel v.02"
HOMUNCULUS_VERSION = "HMC v.03"
HMC_TITLE_VOCABULARY = " :: Vocabulary Manager"

#enums
QTYPE_DEFAULT = "default"
QTYPE_SET = "set"
QTYPE_REM = "rem"
QTYPE_INSTRUCTIONS = "instructions"

#listening ports
ELEMENT_LISTENING_PORT = 1337
LEGION_LISTENING_PORT = 1338
HMC_LISTENING_PORT = 1339
SIKULI_LISTENING_PORT = 8000

def get_list_of_ccr_config_files():
    global SETTINGS
    results = []
    for f in os.listdir(SETTINGS["paths"]["GENERIC_CONFIG_PATH"]):
        if f.endswith(".txt"):
            results.append(f.replace("config", "").replace(".txt", ""))
    return results

def get_ccr_config_file_pronunciation(config_file_name):
    global SETTINGS
    if config_file_name in SETTINGS["pronunciations"]:
        return SETTINGS["pronunciations"][config_file_name]
    return config_file_name

def save_json_file(data, path):
    try:
        formatted_data = json.dumps(data, sort_keys=True, indent=4,
            ensure_ascii=False)
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()
        with open(path, "w") as f:
            f.write(formatted_data)
    except Exception:
        print "error saving json file: " + path

def load_json_file(path):
    result = {}
    try:
        if os.path.isfile(path):  # If the file exists.
            with open(path, "r") as f:
                result = json.loads(f.read())
                f.close()
        else:
            save_json_file(result, path)
    except Exception:
        print "error loading json file: " + path
    return result

def save_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    save_json_file(SETTINGS, INISETPATH if SETTINGS == None or not "SETTINGS" in SETTINGS.keys() else SETTINGS["SETTINGS_PATH"])

def load_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    SETTINGS = load_json_file(INISETPATH if SETTINGS == None else SETTINGS["SETTINGS_PATH"])
    init_default_values()

def init_default_values():
    global SETTINGS
    values_change_count = 0
    
    
    
    # paths section
    if not "paths" in SETTINGS.keys():
        SETTINGS["paths"] = {}
        values_change_count += 1
    if not "BASE_PATH" in SETTINGS["paths"]:
        SETTINGS["paths"]["BASE_PATH"] = "C:/NatLink/NatLink/MacroSystem"
    for (name, value) in [
        # DATA
        ("DLL_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/dll/"),
        ("SETTINGS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/settings.json"),
        ("ELEMENT_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/element.json"),
        ("DISPEL_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/dispel.json"),
        ("SAVED_CLIPBOARD_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/clipboard.json"),
        ("RECORDED_MACROS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/recorded_macros.json"),
        ("LOG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/log.txt"),
        ("SIKULI_SCRIPTS_FOLDER_PATH", ""),
        
        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        ("REMOTE_DEBUGGER_PATH" , "D:/PROGRAMS/NON_install/eclipse/plugins/org.python.pydev_3.4.1.201403181715/pysrc"),
        
        # EXECUTABLES
        ("WSR_PATH", "C:/Windows/Speech/Common/sapisvr.exe"),
        ("ELEMENT_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/element.py"),
        ("LEGION_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/legion.py"),
        ("RAINBOW_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/display.py"),
        ("DOUGLAS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/display.py"),
        ("HOMUNCULUS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/hmc/h_launch.py"),
        ("NIRCMD_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/nircmd/nircmd.exe"),
        ("MMT_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/MultiMonitorTool/MultiMonitorTool.exe"),
        ("DEFAULT_BROWSER_PATH", "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"),
        ("SIKULI_IDE_JAR_PATH", ""),
        ("SIKULI_SCRIPTS_JAR_PATH", ""),
        ("SIKULI_SERVER_PATH", SETTINGS["paths"]["BASE_PATH"] +"asynch/sikuli/scripts/xmlrpc_server.sikuli"),
        ("SIKULI_COMPATIBLE_JAVA_EXE_PATH", ""),
        
        # CCR
        ("GENERIC_CONFIG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/ccr"),
        ("UNIFIED_CONFIG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/ccr/unified/config.txt"),
        
        # MISC
        ("ALARM_SOUND_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media/49685__ejfortin__nano-blade-loop.wav"),
        ("MEDIA_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media"),
        ("HOMEBREW_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/homebrew")                          
        ]:
        if not name in SETTINGS["paths"]:  # .keys()
            SETTINGS["paths"][name] = value
            values_change_count += 1
    if not SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"] in sys.path:
        sys.path.append(SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"])
    
    
    # CCR section
    ccrNamesFromFiles = []
    for ccrn in get_list_of_ccr_config_files():
        ccrNamesFromFiles.append((ccrn, False))
    if not "ccr" in SETTINGS.keys():
        SETTINGS["ccr"] = {}
        SETTINGS["ccr"]["modes"] = {}
        SETTINGS["ccr"]["common"] = []
        SETTINGS["ccr"]["standard"] = ["alphabet", "navigation", "punctuation"]
        SETTINGS["ccr"]["nonglobal_sets"] = []
        values_change_count += 1
    for (name, value) in ccrNamesFromFiles:
        if not name in SETTINGS["ccr"]["modes"]:
            SETTINGS["ccr"]["modes"][name] = value
            values_change_count += 1
    
    # passwords section
    if not "password" in SETTINGS.keys():
        SETTINGS["password"] = {}
        SETTINGS["password"]["seed1"] = "abc123"
        SETTINGS["password"]["seed2"] = "abd124"
        SETTINGS["password"]["seed3"] = "abe125"
        SETTINGS["password"]["seed4"] = "abf126"
        values_change_count += 1
    
    # miscellaneous section
    if not "miscellaneous" in SETTINGS.keys():
        SETTINGS["miscellaneous"] = {}
        SETTINGS["miscellaneous"]["debug_speak"] = False
        SETTINGS["miscellaneous"]["dev_commands"] = False
        SETTINGS["miscellaneous"]["sikuli_enabled"] = False
        values_change_count += 1
    
    # pronunciations section
    if not "pronunciations" in SETTINGS.keys():
        SETTINGS["pronunciations"] = {}
        values_change_count += 1
    for (word, pronunciation) in [
        ("c++", "C plus plus"),
        ("jquery", "J query"),
        ]:
        if not word in SETTINGS["pronunciations"]:  # .keys()
            SETTINGS["pronunciations"][word] = pronunciation
            values_change_count += 1
    
    if values_change_count > 0:
        print "settings values changed: ", values_change_count
        save_config()

def get_settings():
    global SETTINGS
    return SETTINGS

def get_default_browser_executable():
    global SETTINGS
    return SETTINGS["paths"]["DEFAULT_BROWSER_PATH"].split("/")[-1]

load_config()
