import json
import os
import sys

SETTINGS = None
BAD_LOAD = False
INISETPATH = 'C:/NatLink/NatLink/MacroSystem/caster/bin/data/settings.json'

# title
SOFTWARE_VERSION_NUMBER = "0.4.7"
SOFTWARE_NAME = "Caster v " + SOFTWARE_VERSION_NUMBER
S_LIST_VERSION = "Sticky List v " + SOFTWARE_VERSION_NUMBER
DISPEL_VERSION = "Dispel v " + SOFTWARE_VERSION_NUMBER
HOMUNCULUS_VERSION = "HMC v " + SOFTWARE_VERSION_NUMBER
HMC_TITLE_VOCABULARY = " :: Vocabulary Manager"
HMC_TITLE_RECORDING = " :: Recording Manager"
HMC_TITLE_DIRECTORY = " :: Directory Selector"
LEGION_TITLE = "legiongrid"
RAINBOW_TITLE = "rainbowgrid"
DOUGLAS_TITLE = "douglasgrid"

# enums
QTYPE_DEFAULT = "def"
QTYPE_SET = "set"
QTYPE_REM = "rem"
QTYPE_INSTRUCTIONS = "ins"
QTYPE_RECORDING = "rec"
QTYPE_DIRECTORY = "dir"

def register_language(extension, language):
    '''
    This is for automatic language switching
    '''
    global SETTINGS
    if extension not in SETTINGS["ccr"]["registered_extensions"]:
        
        SETTINGS["ccr"]["registered_extensions"][extension] = get_ccr_config_file_pronunciation(language.lower())
        save_config()

def get_list_of_ccr_config_files():
    global SETTINGS
    results = []
    for f in os.listdir(SETTINGS["paths"]["GENERIC_CONFIG_PATH"]):
        if f.endswith(".txt"):
            results.append(f.replace("config", "").replace(".txt", "").lower())
    return results

def get_ccr_config_file_pronunciation(config_file_name):
    global SETTINGS
    if config_file_name in SETTINGS["pronunciations"]:
        return SETTINGS["pronunciations"][config_file_name]
    return config_file_name

def _save(data, path):
    '''only to be used for settings file'''
    try:
        formatted_data = json.dumps(data, sort_keys=True, indent=4,
            ensure_ascii=False)
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()
        f = open(path, "w")
        f.write(formatted_data)
        f.close()
    except Exception:
        print "error saving json file: " + path

def _load(path):
    '''only to be used for settings file'''
    result = {}
    try:
        f = open(path, "r")
        result = json.loads(f.read())
        f.close()
    except ValueError:
        global BAD_LOAD 
        BAD_LOAD = True
        print "\n\nValueError while loading settings file: " + path + "\n\n"
        print sys.exc_info()
    except IOError:
        print "\n\nIOError: Could not find settings file: " + path + "\nInitializing file...\n\n"
#         print sys.exc_info()
    return result

def save_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    _save(SETTINGS, INISETPATH if SETTINGS == None or not "SETTINGS" in SETTINGS.keys() else SETTINGS["SETTINGS_PATH"])

def load_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    SETTINGS = _load(INISETPATH if SETTINGS == None else SETTINGS["SETTINGS_PATH"])
    init_default_values()

def init_default_values():
    global SETTINGS
    values_change_count = 0
    
    
    
    # paths section
    if not "paths" in SETTINGS.keys():
        SETTINGS["paths"] = {}
        values_change_count += 1
    if not "BASE_PATH" in SETTINGS["paths"]:
        SETTINGS["paths"]["BASE_PATH"] = "C:/NatLink/NatLink/MacroSystem/caster"
    for (name, value) in [
        # DATA
        ("DLL_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/dll/"),
        ("SETTINGS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/settings.json"),
        ("PITA_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/pita.json"),
        ("S_LIST_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/s_list.json"),
        ("DISPEL_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/dispel.json"),
        ("SAVED_CLIPBOARD_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/clipboard.json"),
        ("RECORDED_MACROS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/recorded_macros.json"),
        ("ALIASES_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/ccr/configaliases.txt"),
        ("LOG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/log.txt"),
        ("SIKULI_SCRIPTS_FOLDER_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/sikuli/scripts"),
        
        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        ("REMOTE_DEBUGGER_PATH" , "C:/PROG/alt ec/eclipse/plugins/org.python.pydev_3.9.2.201502050007/pysrc"),
        
        # EXECUTABLES
        ("WSR_PATH", "C:/Windows/Speech/Common/sapisvr.exe"),
        ("STATUS_WINDOW_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/statuswindow.py"),
        ("STICKY_LIST_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/stickylist.py"),
        ("LEGION_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/legion.py"),
        ("RAINBOW_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/grids.py"),
        ("DOUGLAS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/grids.py"),
        ("HOMUNCULUS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/hmc/h_launch.py"),
        ("DEFAULT_BROWSER_PATH", "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"),
        ("SIKULI_IDE_JAR_PATH", ""),
        ("SIKULI_SCRIPTS_JAR_PATH", ""),
        ("SIKULI_SERVER_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/sikuli/scripts/xmlrpc_server.sikuli"),
        ("SIKULI_COMPATIBLE_JAVA_EXE_PATH", ""),
        ("ENGINE_PATH", "C:/Program Files (x86)/Nuance/NaturallySpeaking12/Program/natspeak.exe"),
        ("REBOOT_PATH", SETTINGS["paths"]["BASE_PATH"] + "/bin/reboot.bat"),
        
        # CCR
        ("GENERIC_CONFIG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/ccr"),
                
        # MISC
        ("ALARM_SOUND_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media/49685__ejfortin__nano-blade-loop.wav"),
        ("MEDIA_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media"),
                                  
        ]:
        if not name in SETTINGS["paths"]:  # .keys()
            SETTINGS["paths"][name] = value
            values_change_count += 1
    if not SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"] in sys.path and os.path.isdir(SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"]):
        sys.path.append(SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"])
    
    
    # CCR section
    ccrNamesFromFiles = []
    for ccrn in get_list_of_ccr_config_files():
        if ccrn in ["navigation", "alphabet", "numbers", "punctuation"]:
            ccrNamesFromFiles.append((ccrn, True))
        else:
            ccrNamesFromFiles.append((ccrn, False))
    if not "ccr" in SETTINGS.keys():
        SETTINGS["ccr"] = {}
        SETTINGS["ccr"]["modes"] = {}
        SETTINGS["ccr"]["common"] = []
        SETTINGS["ccr"]["standard"] = ["alphabet", "navigation", "punctuation", "numbers"]
        SETTINGS["ccr"]["registered_extensions"] = {}
        SETTINGS["ccr"]["default_lower"] = True
        values_change_count += 1
    for (name, value) in ccrNamesFromFiles:
        if not name in SETTINGS["ccr"]["modes"]:
            SETTINGS["ccr"]["modes"][name] = value
            values_change_count += 1
    SETTINGS["nodes"] = {}
    
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
        SETTINGS["miscellaneous"]["status_window_enabled"] = True
        values_change_count += 1
    
    # element section
    if not "pita" in SETTINGS.keys():
        SETTINGS["pita"] = {}
        SETTINGS["pita"]["recent_files"] = 10
        SETTINGS["pita"]["extensions"] = [".py", ".java", ".cpp", ".h", ".js"]
        SETTINGS["pita"]["filter_strict"] = False
        SETTINGS["pita"]["use_bonus"] = True
        SETTINGS["pita"]["use_penalty"] = True
        SETTINGS["pita"]["automatic_lowercase"] = True
        values_change_count += 1
        
    # auto_com section
    if not "auto_com" in SETTINGS.keys():
        SETTINGS["auto_com"] = {}
        SETTINGS["auto_com"]["active"] = False
        SETTINGS["auto_com"]["change_language"] = False
        SETTINGS["auto_com"]["change_language_only"] = False
        SETTINGS["auto_com"]["interval"] = 3
        SETTINGS["auto_com"]["executables"] = ["pycharm.exe", "WDExpress.exe", "notepad++.exe"]
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
    
    if not "one time warnings" in SETTINGS.keys():
        SETTINGS["one time warnings"] = {}
        values_change_count += 1
    
    global BAD_LOAD
    if values_change_count > 0 and not BAD_LOAD:
        print "settings values changed: ", values_change_count
        save_config()

def get_settings():
    global SETTINGS
    return SETTINGS

def get_default_browser_executable():
    global SETTINGS
    return SETTINGS["paths"]["DEFAULT_BROWSER_PATH"].split("/")[-1]

def report_to_file(message):
    global SETTINGS
    f = open(SETTINGS["paths"]["LOG_PATH"], 'a') 
    f.write(str(message) + "\n")
    f.close()

load_config()
