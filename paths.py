'''
Created on May 17, 2014

@author: dave
'''
import sys, os

BASE_PATH='C:\NatLink\NatLink\MacroSystem\\'

REMOTE_DEBUGGER_PATH ="D:\PROGRAMS\NON_install\eclipse\plugins\org.python.pydev_3.4.1.201403181715\pysrc"

NIRCMD_PATH=r"C:\NatLink\NatLink\MacroSystem\exe\nircmd\nircmd.exe"
MMT_PATH =r"C:\NatLink\NatLink\MacroSystem\exe\MultiMonitorTool\MultiMonitorTool.exe"

JAVA_CONFIG_PATH = "C:\NatLink\NatLink\MacroSystem\languages\configjava.txt"
PYTHON_CONFIG_PATH = "C:\NatLink\NatLink\MacroSystem\languages\configpython.txt"
HTML_CONFIG_PATH = "C:\NatLink\NatLink\MacroSystem\languages\confightml.txt"

def get_base():
    global BASE_PATH
    return BASE_PATH

def get_nircmd():
    global NIRCMD_PATH
    return NIRCMD_PATH

def get_mmt():
    global MMT_PATH
    return MMT_PATH

def get_all_language_configs():
    global JAVA_CONFIG_PATH
    global PYTHON_CONFIG_PATH
    global HTML_CONFIG_PATH
    return [JAVA_CONFIG_PATH, PYTHON_CONFIG_PATH, HTML_CONFIG_PATH]

if not REMOTE_DEBUGGER_PATH in sys.path:
    sys.path.append(REMOTE_DEBUGGER_PATH)