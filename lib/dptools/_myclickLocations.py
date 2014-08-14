#-------------------------------------------------------------------------------
# Name:        Click Locations
# Purpose:     Use voice to create commands that remember mouse locations.
#
#
# Author:      Douglas Parent
#
# Created:     12/20/2011
# Copyright:   (c) Douglas Parent 2011
# License:     You are free to use and modify this software for your own use.
#-------------------------------------------------------------------------------
#

import natlink
from natlinkutils import *
import _mycommon
import win32gui
import win32ui
import win32api
import string
import win32con
import win32clipboard
import subprocess
import natlinkstatus
status = natlinkstatus.NatlinkStatus()
import time
import shelve

class ThisGrammar(GrammarBase):

    gramSpec = """
        <dgndictation> imported;

        <saveMouseLocationClick> exported = ['set'] 'click location' <dgndictation>;
        <returnMouseLocationClick> exported  = {savedMouseLocation};
        <clearMouseLocations> exported = 'clear' ('mouse positions' | 'click locations');
        <deleteMouseLocation> exported = 'delete' ('mouse position' | 'click location') <dgndictation>;
        <showMouseLocations> exported = 'show' ('mouse positions' | 'click locations');

    """

    # This is a dictionary of dictionaries.
    # The outer dictionary is keyed by module name.
    # The inner dictionary is keyed by command name.
    savedMouseLocations = {}
    savedMouseLocationsFile = "savedMouseLocations.obj"

    currentModule = "";
    mouseLocationCommandList = 'savedMouseLocation'

    def initialize(self):
        self.load(self.gramSpec)
        self.activateAll()
        self.savedMouseLocations = shelve.open(status.getUserDirectory() + '\\' + self.savedMouseLocationsFile,
                                               writeback=True)

    def gotBegin(self, moduleInfo):
        self.currentModule = string.lower( getBaseName(moduleInfo[0]) )
        self.loadMouseClickCommands()

    def loadMouseClickCommands(self):
        self.emptyList(self.mouseLocationCommandList)
        if not self.savedMouseLocations.has_key(self.currentModule):
            return

        self.setList(self.mouseLocationCommandList,
                     self.savedMouseLocations[self.currentModule].keys())

    # the difference between this and "save mouse location" is that
    # this command makes the location into a standalone command.
    # for example, if you say "set mouse location top", you can then say "top"
    # and the mouse will return to the spot and click
    def gotResults_saveMouseLocationClick(self, words, fullResults):
        text = _mycommon.getDictatedString(fullResults)
        self.doSaveMouseLocation(text)


    def doSaveMouseLocation (self, locationName):
        # Get screen mouse position in pixels
        words = ['get', 'mouse position', 'pixels']
        fullResults = [('get', 'getMousePosition'),
                       ('mouse position', 'getMousePosition'),
                       ('pixels', 'getMousePosition')]
        self.getMousePosition(words, fullResults)
        mouseLocation = _mycommon.getClipboard().split(', ')
        if not self.savedMouseLocations.has_key(self.currentModule):
            self.savedMouseLocations[self.currentModule] = {}
        self.savedMouseLocations[self.currentModule][locationName] = mouseLocation
        print self.savedMouseLocations[self.currentModule][locationName]
        self.savedMouseLocations.sync()
        # make the location a standalone command
        self.loadMouseClickCommands();
        #print self.savedMouseLocations

    def getMousePosition(self,words,fullResults):
        results = convertResults(fullResults)
        dictated = results['getMousePosition']
        x, y = win32api.GetCursorPos()
        if 'screen' not in dictated:
            # Use relative coordinates by default
            left, top, right, bottom = win32gui.GetWindowRect(win32gui.GetForegroundWindow())

            # which corner is mouse position relative to?
            if 'north east' in dictated:
                x = right - x
                y = y - top
            elif 'south west' in dictated:
                x = x - left
                y = bottom - y
            elif 'south east' in dictated:
                x = right - x
                y = bottom - y
            else:
                # North west corner by default
                x = x - left
                y = y - top

        if 'pixels' not in dictated:
            # Grid coordinates by default
            x = x / pixelsPerGridUnit
            y = y / pixelsPerGridUnit
            print "Mouse position in grid units:  " + str(x) + ", " + str(y)
        else:
            print "Mouse position in pixels:  " + str(x) + ", " + str(y)
        _mycommon.setClipboard(str(x) + ", " + str(y))

    def gotResults_returnMouseLocationClick(self, words, fullResults):
        self.doReturnMouseLocation(words[0])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def doReturnMouseLocation(self, locationName):
        if not self.savedMouseLocations[self.currentModule].has_key(locationName):
            print '"' + locationName + '" is not a saved mouse location.'
            return

        commands = self.savedMouseLocations[self.currentModule]
        mouseLocation = commands[locationName]
        mousex = int(mouseLocation[0])
        mousey = int(mouseLocation[1])

        # Location is relative to app window
        # Find screen coords
        left, top, right, bottom = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        mousex = left + mousex
        mousey = top + mousey
        # Stupid method takes a tuple, so need extra parens
        win32api.SetCursorPos((mousex, mousey))

    def gotResults_clearMouseLocations(self, words, fullResults):
        messageboxThread = _mycommon.MessageBoxThread("Do you want to clear ALL saved mouse locations?", \
                                                      'Clear saved mouse locations', \
                                                      _mycommon.MessageBoxThread.STYLE_YES_NO)
        messageboxThread.start()
        messageboxThread.join()

        if messageboxThread.returnValue == _mycommon.MESSAGEBOX_RETURN_YES:
            self.savedMouseLocations.clear()
            self.savedMouseLocations.sync()
            self.loadMouseClickCommands()

    def gotResults_deleteMouseLocation(self, words, fullResults):
        text = _mycommon.getDictatedString(fullResults)

        if not self.savedMouseLocations.has_key(self.currentModule):
            messageboxThread = _mycommon.MessageBoxThread('No commands available to delete.', \
                                                          "Delete location commands")
            messageboxThread.start()
            messageboxThread.join()
            return

        if not self.savedMouseLocations[self.currentModule].has_key(text):
            messageboxThread = _mycommon.MessageBoxThread("No command named '" + text + "'.", \
                                                          "Delete location commands")
            messageboxThread.start()
            messageboxThread.join()
            return

        messageboxThread = _mycommon.MessageBoxThread("Do you want to delete the '" + text + "' location?", \
                                                      'Delete saved mouse location', \
                                                      _mycommon.MessageBoxThread.STYLE_YES_NO)
        messageboxThread.start()
        messageboxThread.join()
        if messageboxThread.returnValue == _mycommon.MESSAGEBOX_RETURN_NO:
            return

        commands = self.savedMouseLocations[self.currentModule]
        del commands[text]
        self.savedMouseLocations.sync()
        self.loadMouseClickCommands()

    def gotResults_showMouseLocations(self, words, fullResults):
        if not self.savedMouseLocations.has_key(self.currentModule):
            messageboxThread = _mycommon.MessageBoxThread('No commands for this application.', \
                                                          "Show location commands")
            messageboxThread.start()
            messageboxThread.join()
            return

        locations = ''
        for location in self.savedMouseLocations[self.currentModule].keys():
            if len(locations) != 0:
                locations = locations + '\n'
            locations = locations + location

        if len(locations) == 0:
            locations = 'There are no click locations defined for this application.'

        messageboxThread = _mycommon.MessageBoxThread(locations, \
                                                      "Show location commands")
        messageboxThread.start()
        messageboxThread.join()


thisGrammar = ThisGrammar()
thisGrammar.initialize()

def unload():
    global thisGrammar
    thisGrammar.savedMouseLocations.close()
    if thisGrammar: thisGrammar.unload()
    thisGrammar = None