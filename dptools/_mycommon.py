#-------------------------------------------------------------------------------
# Name:        MyCommon
# Purpose:     General purpose utilities.
#
#
# Author:      Douglas Parent
#
# Created:     12/20/2011
# Copyright:   (c) Douglas Parent 2011
# License:     You are free to use and modify this software for your own use.
#-------------------------------------------------------------------------------
# General purpose functions

import natlink
from natlinkutils import *
import win32gui
import win32process
import win32api
import win32con
import win32com.client
import string
from _keyCodes import *
import win32clipboard
import sys
from threading import Thread
import pythoncom
import time

KEYEVENTF_EXTENDEDKEY = 0x01
KEYEVENTF_KEYUP = 0x02

lettersMap = {
            'a\\alpha': 'a',
            'b\\bravo': 'b',
            'c\\charlie': 'c',
            'd\\delta': 'd',
            'e\\echo': 'e',
            'f\\foxtrot': 'f',
            'g\\golf': 'g',
            'h\\hotel ': 'h',
            'i\\india': 'i',
            'j\\juliet': 'j',
            'k\\kilo': 'k',
            'l\\lima': 'l',
            'm\\mike': 'm',
            'n\\november': 'n',
            'o\\oscar': 'o',
            'p\\papa': 'p',
            'q\\quebec': 'q',
            'r\\romeo': 'r',
            's\\sierra': 's',
            't\\tango': 't',
            'u\\uniform': 'u',
            'v\\victor': 'v',
            'w\\whiskey': 'w',
            'x\\x-ray': 'x',
            'y\\yankee': 'y',
            'z\\zulu': 'z'}


########################
# on the clipboard methods, wait 50 ms before using the clipboard
# many times we use the clipboard after having issued a clipboard action
# So need to leave some time for the clipboard to finish its previous action
def setClipboard(text):
    time.sleep(0.05)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(1, text)
    win32clipboard.CloseClipboard()

def getClipboard():
    time.sleep(0.05)
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return text

def emptyClipboard():
    time.sleep(0.05)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def getDictatedLetters(fullResults):
    results = convertResults(fullResults)
    dictation = results['dgnletters']

    # Build the string.
    capNext = False
    outString = ""
    aString = ""
    aLetter = ""
    for i in range (len(dictation)):
        aString = dictation[i]
        if aString == '\\spelling-space-bar\\space bar' or aString == '\\spelling-space-bar\\space':
            outString += ' '
            continue
        elif aString == '\\spelling-cap\\cap':
            capNext = True
            continue

        aLetter = aString[0]
        if aLetter == '\\':
            continue

        if capNext:
            outString += aLetter.capitalize()
            capNext = False
        else:
            outString += aLetter

    return outString

def getDictatedString(fullResults):
    results = convertResults(fullResults)
    dictation = results['dgndictation']
    text = ""
    for i in range(len(dictation)):
        if i == 0:
            text = dictation[0]
        else:
            text = text + " " + dictation[i]
    return text

# Accepts the array returned by convertResults.
# Returns the words associated with "dgndictation" in camel case
def getCamelCase(dictation, firstCap):
    if len(dictation) == 0: return ""
    out = ""
    for i in range(len(dictation)):
        if i == 0:
            if firstCap == False:
                out = cleanupDictation(dictation[0]).lower()
            else:
                out += cleanupDictation(dictation[0]).capitalize()
        else:
            out += cleanupDictation(dictation[i]).capitalize()
    return out

# Accepts the array returned by convertResults.
# Returns the words associated with "dgndictation" in static case
def getStaticCase(convertedResults):
    dictation = convertedResults['dgndictation']
    if len(dictation) == 0: return
    out = ""
    for i in range(len(dictation)):
        if i == 0:
            out += cleanupDictation(dictation[0]).upper()
        else:
            out += "_" + cleanupDictation(dictation[i]).upper()
    return out

# Accepts the array returned by convertResults.
# Returns the words associated with "dgndictation" in Ada (underscores, all words inital capped) case
def getAdaCase(dictation):
    if len(dictation) == 0: return ""
    out = ""
    for i in range(len(dictation)):
        if i == 0:
            out = cleanupDictation(dictation[0]).capitalize()
        else:
            out = out + '_' + cleanupDictation(dictation[i]).capitalize()

    return out

# Accepts the array returned by convertResults.
# Returns the words associated with "dgndictation" in camel case
def getHyphenCase(dictation):
    if len(dictation) == 0: return ""
    out = ""
    for i in range(len(dictation)):
        if i == 0:
            out = cleanupDictation(dictation[0]).lower()
        else:
            out += '-' + cleanupDictation(dictation[i]).lower()
    return out

# Dictated punctuation includes a backslash and the name like:  .\dot
# Filter out the backslash and name
# Exception: the backslash character
# Input is a single dictaton token
def cleanupDictation(dictation):
    index = 0
    outString = ""
    index = dictation.find('\\')
    if index == -1:
        return dictation

    if len(dictation) > index + 1 and dictation[index + 1] == '\\':
        return '\\'

    return dictation[:index]

# converts a number in text form to a number in form, e.g. one -> 1
def getNumeral(numberWord):
    if numberWord == 'one':
        return 1
    elif numberWord == 'two':
        return 2
    elif numberWord == 'three':
        return 3
    elif numberWord == 'four':
        return 4
    elif numberWord == 'five':
        return 5
    elif numberWord == 'six':
        return 6
    elif numberWord == 'seven':
        return 7
    elif numberWord == 'eight':
        return 8
    elif numberWord == 'nine':
        return 9
    elif numberWord == 'zero':
        return 0
    else:
        return None

# Used by switch commands for switching applications
def doSwitchCheck(hwnd, title):
    #Is this the desired window?  Only want unowned windows, i.e. those without parents
    wndText = win32gui.GetWindowText(hwnd)
    if wndText and wndText == "":
        return 1
    wndText = string.lower(wndText)
    # Look for text at start of window title
    if wndText[0:len(title)] == title:
        # This is it.
        #print hwnd
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
#        print "Found window: " + wndText

        # Stops enumeration
        return 0
    else:
        # Not found.  This causes the next window to be enumerated
        return 1

def doSwitchCheckByProcessName(hwnd, name):
    filename = getHwndProcessName(hwnd)
    if filename.find(name) > -1:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
        #print hwnd
        # stops numeration
        return 0
    else:
        # Not it.  Keep looking.  This causes the next window to be enumerated.
        return 1

def getHwndProcessName(hwnd):
    retTuple = win32process.GetWindowThreadProcessId(hwnd)
    if retTuple:
        pid = retTuple[1]
        pHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, int(pid))
        if pHandle:
            return win32process.GetModuleFileNameEx(pHandle, 0)

# The following method stores the found hwnd in this global variable
foundProcessHwnd = None
def checkHwndForProcessName(hwnd, name):
    global foundProcessHwnd
    foundProcessHwnd = None
    filename = getHwndProcessName(hwnd)
    print filename
    if filename.find(name) > -1:
        foundProcessHwnd = hwnd
        # stop enumeration
        return 0
    else:
        # continue enumeration
        return 1

def getProcessIdForModule(moduleName):
    # Get all process ids
    moduleName = string.lower(moduleName)
    pids = win32process.EnumProcesses()
    for i in range(len(pids)):
        # Get handle for a process
        try:
            pHandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, int(pids[i]))
            if pHandle:
                try:
                    # Get process modules
                    try:
                        modHandles = win32process.EnumProcessModules(pHandle)

                        for j in range(len(modHandles)):
                            # Get process file name
                            name = win32process.GetModuleFileNameEx(pHandle, modHandles[j])
                            name = string.lower(name)
                            if string.find(name, moduleName) != -1:
                                # Found it.
                                return pids[i]
                    except win32process.error, ex:
                        pass
                finally:
                    win32api.CloseHandle(pHandle)
        except win32api.error, ex:
            if ex.args[0] not in (5, 6, 87):
                # Ignore the following:
                #   api_error: (87, 'GenerateConsoleCtrlEvent', 'The parameter is incorrect.')
                #   api_error: (6, 'GenerateConsoleCtrlEvent', 'The handle is invalid.')
                # Get error 6 if there is no console.
                raise

    return -1

def keyDown(key):
    win32api.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY | 0, 0)


def keyUp(key):
    win32api.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

# Presses the windows key and the indicated key
def winKey(key):
    keyDown(VK_LWIN)
    keyDown(key)
    keyUp(key)
    keyUp(VK_LWIN)

def dictionaryValuesToArray(dict):
    arrayVals = []
    i = 0
    for val in dict.values:
        arrayVals[i] = val
        i = i + 1

    return arrayVals

##########################
# Message Box methods
##########################
# Full details:  http://msdn.microsoft.com/en-us/library/ms645505%28VS.85%29.aspx
# Button Types
MESSAGEBOX_OK = 0x0
MESSAGEBOX_OK_CANCEL = 0x1
MESSAGEBOX_ABORT_RETRY_IGNORE = 0x2
MESSAGEBOX_YES_NO_CANCEL = 0x3
MESSAGEBOX_YES_NO = 0x4
MESSAGEBOX_RETRY_CANCEL = 0x5
MESSAGEBOX_CANCEL_TRY_CONTINUE = 0x6

# Icon Types
ICON_STOP = 0x10
ICON_QUESTION = 0x20
ICON_EXCLAMATION = 0x30
ICON_INFORMATION = 0x40

# Other type values
DEFAULT_SECOND_BUTTON = 0x100
DEFAULT_THIRD_BUTTON = 0x200
SYSTEM_MODAL = 0x1000
RIGHT_JUSTIFIED = 0x80000
RIGHT_TO_LEFT_READING_ORDER = 0x100000

# Return values
MESSAGEBOX_RETURN_TIMEOUT = -1
MESSAGEBOX_RETURN_OK = 1
MESSAGEBOX_RETURN_CANCEL = 2
MESSAGEBOX_RETURN_ABORT = 3
MESSAGEBOX_RETURN_RETRY = 4
MESSAGEBOX_RETURN_IGNORE = 5
MESSAGEBOX_RETURN_YES = 6
MESSAGEBOX_RETURN_NO = 7
MESSAGEBOX_RETURN_TRY_AGAIN = 10
MESSAGEBOX_RETURN_CONTINUE = 11

MESSAGEBOX_APP_MODAL = 0
MESSAGEBOX_SYS_MODAL = 0x1000
MESSAGEBOX_TASK_MODAL = 0x2000
MESSAGEBOX_SERVICE_NOTIFICATION = 0x200000

# do not run any of the message box from a natlink thread.
# it may cause the entire NaturallySpeaking process to abruptly terminate.
# Instead, call one of the methods on the MessageBoxThread class.
class MessageBoxThread(Thread):
    global MESSAGEBOX_OK, MESSAGEBOX_OK_CANCEL, MESSAGEBOX_YES_NO, MESSAGEBOX_YES_NO_CANCEL
    global ICON_QUESTION, ICON_INFORMATION

    returnValue = True

    # Defines some common message box styles
    # Pass these into the object constructor
    STYLE_OK = MESSAGEBOX_OK + ICON_INFORMATION
    STYLE_OK_CANCEL = MESSAGEBOX_OK_CANCEL + ICON_QUESTION
    STYLE_YES_NO = MESSAGEBOX_YES_NO + ICON_QUESTION
    STYLE_YES_NO_CANCEL = MESSAGEBOX_YES_NO_CANCEL + ICON_QUESTION

    def __init__(self, prompt, title, style = MESSAGEBOX_OK + ICON_INFORMATION):
        Thread.__init__(self)
        self.prompt = prompt
        self.title = title
        self.style = style

    def run(self):
        sys.conit_flags = 0
        pythoncom.CoInitializeEx(0)
        shell = win32com.client.Dispatch("WScript.Shell")
        self.returnValue = shell.Popup(self.prompt, 0, self.title, self.style)
        """
        vbhost = win32com.client.Dispatch("ScriptControl")
        vbhost.language = "vbscript"
        vbhost.AllowUI = "True"
        returnValue = vbhost.Eval('InputBox("Hi there")')
        vbhost.Eval('MsgBox("' + returnValue + '")')
        print "test"
        print returnValue

        """
        #for id in range(1, 5000):
        #    print id

        pythoncom.CoUninitialize()
        return

################################
# Non-thread version of Messagebox

# Returns one of the return values
def messageBox(prompt, title, style):
    shell = win32com.client.Dispatch("WScript.Shell")
    return shell.Popup(prompt, 0, title, style)

# Always returns true
def messageBoxOK(prompt, title):
    return messageBox(prompt, title, MESSAGEBOX_OK + ICON_INFORMATION)

# Returns True if the default button is clicked, False if the secondary button is clicked.
def messageBoxOKCancel(prompt, title):
    return messageBox(prompt, title, MESSAGEBOX_OK_CANCEL + ICON_QUESTION)

# Returns True if the default button is clicked, False if the secondary button is clicked.
def messageBoxYesNo(prompt, title):
    return messageBox(prompt, title, MESSAGEBOX_YES_NO + ICON_QUESTION)

# Returns True if the default button is clicked, False if the secondary button is clicked.
def messageBoxYesNoCancel(prompt, title):
    return messageBox(prompt, title, MESSAGEBOX_YES_NO_CANCEL + ICON_QUESTION)

# Returns a tuple of the mouse position relative to current app
def getMousePositionApp():
    x, y = win32api.getCursorPos()

    # Use relative coordinates
    left, top, right, bottom = win32gui.GetWindowRect(win32gui.GetForegroundWindow())

    # Mouse relative to north west corner of app window
    x = x - left
    y = y - top

    return x, y

#######################################
# Call back

# Use these functions to set or get a call back.  If you want a command to actually be a collection of commands
# you can set a callback in the first command and then have the subsequent commands check for callback.
# For example, if when you say "lock workstation" you want to actually run a command
# that changes status followed by a command that locks the workstation, set a call back to lock the workstation,
# then call the command to change the status.  In the status change command, have it checked for callback
# and if found, run the callback.

callbackFunction = None
callbackArgs = None

# Sets the callback function.  Pass in the function pointer and any args after
def setCallbackFunction(function, *args):
    global callbackFunction, callbackArgs
    callbackFunction = function
    callbackArgs = args

def clearCallbackFunction():
    global callbackFunction, callbackArgs
    callbackFunction = None
    callbackArgs = None

# check to see if there is a callback function.  Returns true if there is, false if there is not
def checkCallbackFunction():
    global callbackFunction
    if callbackFunction == None:
        return False
    else:
        return True

def getCallbackFunction():
    global callbackFunction
    return callbackFunction

def getCallbackArgs():
    global callbackArgs
    return callbackArgs

# runs the call back function, passing in the call backk args
def runCallbackFunction():
    global callbackFunction, callbackArgs
    if callbackFunction == None:
        return

    returnVal = callbackFunction(*callbackArgs)
    clearCallbackFunction()
    return returnVal

def unload():
    global callbackFunction
    global callbackArgs
    global foundProcessHwnd
    callbackFunction = None
    callbackArgs = None
    foundProcessHwnd = None
