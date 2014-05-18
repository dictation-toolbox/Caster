'''
Created on May 17, 2014

@author: dave
'''
BASE_PATH='C:\NatLink\NatLink\MacroSystem\\'
NIRCMD_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\nircmd\nircmd.exe"
MMT_PATH =r"C:\NatLink\NatLink\MacroSystem\exe\MultiMonitorTool\MultiMonitorTool.exe"
JAVA_CONFIG_PATH = "C:\NatLink\NatLink\MacroSystem\languages\configjava.txt"
PYTHON_CONFIG_PATH = "C:\NatLink\NatLink\MacroSystem\languages\configpython.txt"

def get_base():
    global BASE_PATH
    return BASE_PATH

def get_nircmd():
    global NIRCMD_PATH
    return NIRCMD_PATH

def get_javaconfig():
    global JAVA_CONFIG_PATH
    return JAVA_CONFIG_PATH

def get_mmt():
    global MMT_PATH
    return MMT_PATH

def get_all_language_configs():
    global JAVA_CONFIG_PATH
    global PYTHON_CONFIG_PATH
    return [JAVA_CONFIG_PATH, PYTHON_CONFIG_PATH]