'''
Created on Jun 12, 2014

@author: dave
'''
from dragonfly import Key, BringApp
import natlink
import win32gui, win32process, win32api
import os, json, shutil,sys
import paths

BASE_PATH = paths.get_base()

MULTI_CLIPBOARD = {}

def press_digits(n):
    number=str(n)
    for digit in number:
        Key(digit).execute()
        
def get_active_window_hwnd():
    return str(win32gui.GetForegroundWindow())

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def get_active_window_path():
    name = win32gui.GetForegroundWindow()
    t,p = win32process.GetWindowThreadProcessId(name)
    handle = win32api.OpenProcess(0x0410,False,p)
    return win32process.GetModuleFileNameEx( handle, 0 )

def clear_pyc():
    global BASE_PATH
    os.chdir(BASE_PATH)
    for files in os.listdir("."):
        if files.endswith(".pyc"):
            filepath=BASE_PATH+files
            os.remove(filepath)
            report("Deleted: "+filepath)

def save_json_file(data, path):
    try:
        formatted_data = json.dumps(data, sort_keys=True, indent=4,
            ensure_ascii=False)
        with open(path, "w+") as f:
            f.write(formatted_data)
            f.close()
    except Exception as e:
        report("Could not save file: %s" % str(e))

def load_json_file(path):
    result={}
    try:
        if os.path.isfile(path):  # If the file exists.
            with open(path, "r") as f:
                result = json.loads(f.read())
                f.close()
        else:
            save_json_file(result, path)
    except Exception as e:
        report("Could not load file: %s" % str(e))
    return result

def remote_debug():
    import pydevd;#@UnresolvedImport
    pydevd.settrace()
    
def report(message, speak=False, console=True, log=False):
    if console:
        print message
    if speak:
        natlink.execScript ("TTSPlayString \"" +message+ "\"")
    #To do: logging
    
def list_to_string(l):
    return "\n".join([str(x) for x in l])

def alarm(minutes):
    minutes=int(minutes)*60
    BringApp("python", paths.BASE_PATH+"\\alarm.py", str( minutes ))._execute()
    
def py2exe_compile(choice):
    dirname=str(choice)
    
    try:
        # zero, check to see if the target directory exists, if it does delete it
        target_location=paths.get_homebrew_path()+"\\"+dirname
        if os.path.isdir(target_location):
            shutil.rmtree(target_location)
        # first, copy all the files needed- standard stuff plus utilities, paths, and whatever is getting turned into an executable
        shutil.copytree(paths.get_py2exe_path(),target_location+"\\setup")
        # next, modify run.py, replacing "target" with whatever the actual file is
        # run the batch file
        # move the results to the desired location
        
#         shutil.copyfile(paths.BASE_PATH+"old\\helpdisplay.py" ,paths.BASE_PATH+"old\\helpdisplay2.py" )
#         shutil.copytree(paths.BASE_PATH+"media",paths.BASE_PATH+"old\\media")
    except Exception:
        report(list_to_string(sys.exc_info()))
    
    
