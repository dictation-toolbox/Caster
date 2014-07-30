'''
Created on Jun 12, 2014

@author: dave
'''
from dragonfly import Key, BringApp
import natlink
import win32gui, win32process, win32api
import os, json, shutil,sys,errno,stat,io, time
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

permanent=None
    
def py2exe_compile(choice):# requires the file to be compiled to be in the macrosystem folder
    dirname=str(choice)
    
    try:
        # -1, shut down the process just in case it was open
        BringApp(paths.get_pstools_path()+"\\pskill.exe", dirname+".exe")._execute()
        # zero, check to see if the target directory exists, if it does delete it
        target_location=paths.get_homebrew_path()+"\\"+dirname
        if os.path.isdir(target_location):
            shutil.rmtree(target_location, ignore_errors=False, onerror=handle_remove_readonly)
        # first, copy all the files needed- standard stuff plus utilities, paths, and whatever is getting turned into an executable
        shutil.copytree(paths.get_py2exe_path(),target_location)
        shutil.copyfile(paths.BASE_PATH+"utilities.py",target_location+"\\utilities.py")
        shutil.copyfile(paths.BASE_PATH+"paths.py",target_location+"\\paths.py")
        shutil.copyfile(paths.BASE_PATH+dirname+".py",target_location+"\\"+dirname+".py")
        # next, modify run.py, replacing "target" with whatever the actual file is
#         remote_debug()
        f_in= open(target_location+"\\run.py", "r")
        lines=f_in.readlines()
        f_in.close()
        for i in range(0, len(lines)):
            if "target" in lines[i]:
                lines[i]=lines[i].replace("target","\""+paths.get_homebrew_path()+"\\\\"+dirname+"\\\\"+dirname+".py\"")
                break
        f_out=open(target_location+"\\run.py", "w")
        f_out.writelines(lines)
        f_out.close()
        # run the batch file
        time.sleep(1)
        os.chdir(target_location)
        BringApp("compile.bat")._execute()
    except Exception:
        report(list_to_string(sys.exc_info()))
    
    
def handle_remove_readonly(func, path, exc):# for use with py2exe_compile 
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise