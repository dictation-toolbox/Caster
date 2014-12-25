import json
import os
import sys
inisetpath='C:/NatLink/NatLink/MacroSystem/bin/data/settings.json'

SPEAK = False  # to do,: add this value to the config
ELEMENT_VERSION = "Element v.04"
DISPEL_VERSION = "Dispel v.02"
HOMUNCULUS_VERSION = "HMC v.01"
PBASE1 = "4dg62sQ$Pm&"
PBASE2 = "4dg62sQ4Pm7"
PBASE3 = "1Q2w3"
PBASE4 = "4"

SETTINGS = None

def get_list_of_ccr_config_files():
    global SETTINGS
    results = []
    for f in os.listdir(SETTINGS["paths"]["GENERIC_CONFIG_PATH"]):
        if f.endswith(".txt"):
            f = f.replace("+", " plus")
            results.append(f.replace("config", "").replace(".txt", ""))
    return results

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
        print "error saving json file: "+path

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
        print "error loading json file: "+path
    return result

def save_config():
    global SETTINGS
    global SETTINGS_PATH
    global inisetpath
    save_json_file(SETTINGS, inisetpath if SETTINGS==None or not "SETTINGS" in SETTINGS.keys() else SETTINGS["SETTINGS_PATH"])

def load_settings():
    global SETTINGS
    global SETTINGS_PATH
    global inisetpath
    SETTINGS = load_json_file(inisetpath if SETTINGS==None else SETTINGS["SETTINGS_PATH"])
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
        ("MONITOR_INFO_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/monitorscans/"),
        ("LOG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/log.txt"),
        
        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        ("REMOTE_DEBUGGER_PATH" , "D:/PROGRAMS/NON_install/eclipse/plugins/org.python.pydev_3.4.1.201403181715/pysrc"),
        
        # EXECUTABLES
        ("WSR_PATH", "C:/Windows/Speech/Common/sapisvr.exe"),
        ("ELEMENT_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/element_src.py"),
        ("LEGION_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/legion.py"),
        ("RAINBOW_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/display.py"),
        ("DOUGLAS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/display.py"),
        ("HOMUNCULUS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/hmc/h_launch.py"),
        ("NIRCMD_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/nircmd/nircmd.exe"),
        ("MMT_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/MultiMonitorTool/MultiMonitorTool.exe"),
        
        
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
    
    # macros section
    if not "macros" in SETTINGS.keys():
        SETTINGS["macros"] = {}
        values_change_count += 1
    
    if values_change_count > 0:
        save_config()
    
    # CCR section
    ccrNamesFromFiles = []
    for ccrn in get_list_of_ccr_config_files():
        ccrNamesFromFiles.append((ccrn, False))
    if not "ccr" in SETTINGS.keys():
        SETTINGS["ccr"] = {}
        values_change_count += 1
    for (name, value) in ccrNamesFromFiles:
        if not name in SETTINGS["ccr"]:  # .keys()
            SETTINGS["ccr"][name] = {}
            SETTINGS["ccr"][name]["active"] = value
            SETTINGS["ccr"][name]["pronunciation"] = ""
            values_change_count += 1

def get_settings():
    global SETTINGS
    return SETTINGS

load_settings()