import json
import os
import sys

SETTINGS = None
BAD_LOAD = False
INISETPATH = os.path.realpath(__file__).split("lib")[0]+"bin\\data\\settings.json"
BASE_PATH = os.path.realpath(__file__).split("\\lib")[0].replace("\\", "/")

# title
SOFTWARE_VERSION_NUMBER = "0.5.8"
SOFTWARE_NAME = "Caster v " + SOFTWARE_VERSION_NUMBER
HOMUNCULUS_VERSION = "HMC v " + SOFTWARE_VERSION_NUMBER
HMC_TITLE_VOCABULARY = " :: Vocabulary Manager"
HMC_TITLE_RECORDING = " :: Recording Manager"
HMC_TITLE_DIRECTORY = " :: Directory Selector"
HMC_TITLE_CONFIRM = " :: Confirm"
LEGION_TITLE = "legiongrid"
RAINBOW_TITLE = "rainbowgrid"
DOUGLAS_TITLE = "douglasgrid"
SETTINGS_WINDOW_TITLE = "Caster Settings Window v "

# enums
QTYPE_DEFAULT = "0"
QTYPE_INSTRUCTIONS = "3"
QTYPE_RECORDING = "4"
QTYPE_DIRECTORY = "5"
QTYPE_CONFIRM = "6"
WXTYPE_SETTINGS = "7"

HMC_SEPARATOR = "[hmc]"

WSR = False

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
        print("error saving json file: " + path)

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
        print("\n\nValueError while loading settings file: " + path + "\n\n")
        print(sys.exc_info())
    except IOError:
        print("\n\nIOError: Could not find settings file: " + path + "\nInitializing file...\n\n")
    return result

def save_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    _save(SETTINGS, INISETPATH if SETTINGS is None or not "SETTINGS" in SETTINGS.keys() else SETTINGS["SETTINGS_PATH"])

def load_config():
    global SETTINGS
    global SETTINGS_PATH
    global INISETPATH
    SETTINGS = _load(INISETPATH if SETTINGS is None else SETTINGS["SETTINGS_PATH"])
    init_default_values()

def update_values(d, key_values):
    values_change_count = 0
    for key, value in key_values:
        if not key in d:
            d[key] = value
            values_change_count += 1
    return values_change_count

def init_default_values():
    global SETTINGS, BASE_PATH
    values_change_count = 0
    
    # paths section
    values_change_count += update_values(SETTINGS, [("paths", {})])
    values_change_count += update_values(SETTINGS["paths"], [("BASE_PATH", BASE_PATH)])
    values_change_count += update_values(SETTINGS["paths"], [
        # DATA
        ("DLL_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/lib/dll/"),
        ("SETTINGS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/settings.json"),
        ("CCR_CONFIG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/ccr.json"),
        ("S_LIST_JSON_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/s_list.json"),
        ("SAVED_CLIPBOARD_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/clipboard.json"),
        ("RECORDED_MACROS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/recorded_macros.json"),
        ("ALIAS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/aliases.json."),
        ("LOG_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/log.txt"),
        ("SIKULI_SCRIPTS_FOLDER_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/sikuli/scripts"),
        ("FILTER_DEFS_PATH", SETTINGS["paths"]["BASE_PATH"] + "/user/words.txt"),
        
        # REMOTE_DEBUGGER_PATH is the folder in which pydevd.py can be found
        ("REMOTE_DEBUGGER_PATH" , "C:/PROG/alt ec/eclipse/plugins/org.python.pydev_3.9.2.201502050007/pysrc"),
        
        # EXECUTABLES
        ("WSR_PATH", "C:/Windows/Speech/Common/sapisvr.exe"),
        ("LEGION_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/legion.py"),
        ("RAINBOW_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/grids.py"),
        ("DOUGLAS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/mouse/grids.py"),
        ("HOMUNCULUS_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/asynch/hmc/h_launch.py"),
        ("DEFAULT_BROWSER_PATH", "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"),
        ("SIKULI_IDE_JAR_PATH", ""),
        ("SIKULI_SCRIPTS_JAR_PATH", ""),
        ("SIKULI_SERVER_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/sikuli/scripts/xmlrpc_server.sikuli"),
        ("SIKULI_COMPATIBLE_JAVA_EXE_PATH", ""),
        ("ENGINE_PATH", "C:/Program Files (x86)/Nuance/NaturallySpeaking14/Program/natspeak.exe"),
        ("REBOOT_PATH", SETTINGS["paths"]["BASE_PATH"] + "/bin/reboot.bat"),
        ("REBOOT_PATH_WSR", SETTINGS["paths"]["BASE_PATH"] + "/bin/reboot_wsr.bat"),
        ("SETTINGS_WINDOW_PATH", SETTINGS["paths"]["BASE_PATH"] + "/asynch/settingswindow.py"), 
        
        # CCR
        ("CONFIGDEBUGTXT_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/data/configdebug.txt"),
                
        # MISC
        ("ALARM_SOUND_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media/49685__ejfortin__nano-blade-loop.wav"),
        ("MEDIA_PATH" , SETTINGS["paths"]["BASE_PATH"] + "/bin/media"),
        
        # PYTHON
        ("WXPYTHON_PATH" , "C:/Python27/Lib/site-packages/wx-3.0-msw"),
                                  
        ])
    if not SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"] in sys.path and os.path.isdir(SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"]):
        sys.path.append(SETTINGS["paths"]["REMOTE_DEBUGGER_PATH"])
    if not SETTINGS["paths"]["WXPYTHON_PATH"] in sys.path and os.path.isdir(SETTINGS["paths"]["WXPYTHON_PATH"]):
        sys.path.append(SETTINGS["paths"]["WXPYTHON_PATH"])
        
    # detect the version of Dragon
    if not os.path.isfile(SETTINGS["paths"]["ENGINE_PATH"]):
        dragon_13_path = "C:/Program Files (x86)/Nuance/NaturallySpeaking13/Program/natspeak.exe"
        dragon_12_path = "C:/Program Files (x86)/Nuance/NaturallySpeaking12/Program/natspeak.exe"
        if os.path.isfile(dragon_13_path):
            SETTINGS["paths"]["ENGINE_PATH"] = dragon_13_path
        elif os.path.isfile(dragon_12_path):
            SETTINGS["paths"]["ENGINE_PATH"] = dragon_12_path
        else:
            print("Cannot find default dragon engine path")
    
    # apps section
    values_change_count += update_values(SETTINGS, [("apps", {})])
    values_change_count += update_values(SETTINGS["apps"], [
                       ("atom", True), 
                       ("chrome", True),
                       ("cmd", True),
                       ("dragon", True),
                       ("eclipse", True),
                       ("emacs", True),
                       ("explorer", True),
                       ("firefox", True),
                       ("flashdevelop", True),
                       ("foxitreader", True),
                       ("gitbash", True),
                       ("kdiff3", True),
                       ("douglas", True),
                       ("legion", True),
                       ("rainbow", True),
                       ("ssms", True),
                       ("jetbrains", True),
                       ("msvc", True),
                       ("notepadplusplus", True),
                       ("sqldeveloper", True),
                       ("sublime", True),
                       ("visualstudio", True),
                       ("winword", True),
                       ("wsr", True),
                       ])
    
    # feature switches
    values_change_count += update_values(SETTINGS, [("feature_rules", {})])
    values_change_count += update_values(SETTINGS["feature_rules"], [
                       ("hmc", True),
                       ("again", True),
                       ("alias", True),
                       ("chainalias", True),
                       ])
    
    # node rules
    values_change_count += update_values(SETTINGS, [("nodes", {})])
    
    # passwords section
    values_change_count += update_values(SETTINGS, [("password", {})])
    values_change_count += update_values(SETTINGS["password"], [
                       ("seed1", "change these"), 
                       ("seed2", "if you use"),
                       ("seed3", "password"),
                       ("seed4", "generation")
                       ])
    
    # miscellaneous section
    values_change_count += update_values(SETTINGS, [("miscellaneous", {})])
    values_change_count += update_values(SETTINGS["miscellaneous"], [
                       ("debug_speak", False), 
                       ("dev_commands", False),
                       ("sikuli_enabled", False),
                       ("keypress_wait", 50), # milliseconds
                       ("max_ccr_repetitions", 16), 
                       ("enable_match_logging", False),
                       ("atom_palette_wait", "30"),
                       ("rdp_mode", False),
                       ("integer_remap_opt_in", False), 
                       ("integer_remap_crash_fix", False),
                       ("print_rdescripts", False)
                       ])
    
    # pronunciations section
    values_change_count += update_values(SETTINGS, [("pronunciations", {})])
    values_change_count += update_values(SETTINGS["pronunciations"], [
        ("c++", "C plus plus"),
        ("jquery", "J query"),
        ])
    
    values_change_count += update_values(SETTINGS, [("one time warnings", {})])
    
    global BAD_LOAD
    if values_change_count > 0 and not BAD_LOAD:
        print("settings values changed: "+ str(values_change_count))
        save_config()

def get_settings():
    global SETTINGS
    return SETTINGS

def get_default_browser_executable():
    global SETTINGS
    return SETTINGS["paths"]["DEFAULT_BROWSER_PATH"].split("/")[-1]

def report_to_file(message, path=None):
    global SETTINGS
    _path = SETTINGS["paths"]["LOG_PATH"]
    if path is not None: _path = path
    f = open(_path, 'a') 
    f.write(str(message) + "\n")
    f.close()

load_config()
