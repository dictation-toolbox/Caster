# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs

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

def get_window_by_title(title):
    hwnd = win32gui.FindWindowEx(0,0,0, title)
    return hwnd

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
        if not os.path.exists(path):
            f= open(path,"w")
            f.close()
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
    if log:
        f = open(paths.get_log_path(),'a') 
        f.write(str(message)+"\n")
        f.close()
    
def list_to_string(l):
    return "\n".join([str(x) for x in l])

def alarm(minutes):
    minutes=int(minutes)*60
    BringApp("python", paths.BASE_PATH+"\\alarm.py", str( minutes ))._execute()

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
        if not os.path.exists(target_location+"\\dist"):
            os.makedirs(target_location)
            os.makedirs(target_location+"\\dist")
        for fb in ["utilities.py","paths.py","settings.py"]:  # base path
            shutil.copyfile(paths.BASE_PATH+fb,target_location+"\\"+fb)
        for fp in ["compile.bat","icon.ico","msvcp90.dll","msvcr90.dll"]:                           # py2exe path
            shutil.copyfile(paths.get_py2exe_path()+"\\"+fp,target_location+"\\"+fp)
        shutil.copyfile(paths.get_py2exe_path()+"\\"+dirname+"_run.py",target_location+"\\run.py")
        if not dirname=="CustomGrid":
            shutil.copyfile(paths.BASE_PATH+"exe\\homebrew\\"+dirname+".py",target_location+"\\"+dirname+".py")
        else:
            shutil.copyfile(paths.BASE_PATH+"dptools\\"+dirname+".py",target_location+"\\"+dirname+".py")
            for fcg in ["argparse.py","_keyCodes.py","_myclickLocations.py","_mycommon.py"]:
                shutil.copyfile("C:\\NatLink\\NatLink\\MacroSystem\\dptools\\"+fcg,target_location+"\\"+fcg)
        # next, copy any additional required files
        if dirname=="element":
            os.makedirs(target_location+"\\dist\\data")
            shutil.copyfile(paths.get_py2exe_path()+"\\"+"tk85.dll",target_location+"\\dist\\tk85.dll")
            shutil.copyfile(paths.get_py2exe_path()+"\\"+"tcl85.dll",target_location+"\\dist\\tcl85.dll")

        # run the batch file
        time.sleep(1)
        os.chdir(target_location)
        BringApp(target_location+ "\\compile.bat")._execute()
    except Exception:
        report(list_to_string(sys.exc_info()))
        
def handle_remove_readonly(func, path, exc):# for use with py2exe_compile 
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise
