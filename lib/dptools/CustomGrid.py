#-------------------------------------------------------------------------------
# Name:        Custom Grid
# Purpose:     Click the mouse using only the keyboard.  Intended to be easily
#               and precisely used with macros.
#
#
# Author:      Douglas Parent
#
# Created:     12/20/2011
# Copyright:   (c) Douglas Parent 2011
# License:     You are free to use and modify this software for your own use.
#-------------------------------------------------------------------------------
#!/cygdrive/c/ProgramFiles/Python25 python

"""
This script allows you to easily click anywhere on a workspace using only the keyboard.
It overlays a grid onto any area of the computer screen that you wish and then
allows you to apply a mouse click to any area of the grid using simple keystrokes.
The script is very customizable, allowing you to specify
    * the grid placement and size
    * how wide grid columns and how high grid rows are
    * whether the grid remains displayed or is hidden after a mouse click
    * a single mouse click, double-click, or right-click
    * grid transparency
    * "always on top" behavior
    * display the grid exactly over the client area of any application
The grid was primarily intended to be used with macros and so can be completely
customized using the command line.  For better performance, new "command line" parameters
can be applied without having to restart the grid, so that the grid window can be minimized
in between grid usages.

For example, to display the grid over your entire desktop, you might use this command line:
pythonw <mypath>CustomGrid.py --width 1658 --height 961 --locationx 6 --locationy 22 --rowheight 20 --columnwidth 20 --numrows 20 --numcolumns 20

To display the grid over the client area of a certain application:
pythonw <mypath>CustomGrid.py --sizeToClient winword.exe --rowheight 20 --columnwidth 20 --numrows 20 --numcolumns 20

To display the grid over the client area of a window with a certain HWND:
pythonw <mypath>CustomGrid.py --sizeToClient 1234567 --rowheight 20 --columnwidth 20 --numrows 20 --numcolumns 20

For a complete description of all command line switches, use:
pythonw <mypath>CustomGrid.py ?

To make it easier to figure out what the desired parameter values are,
run the grid in position mode:
pythonw <mypath>CustomGrid.py --positionMode

The grid will appear with a draggable title bar and can be resized.  Exit the grid by typing 'x'
and you'll be prompted to copy onto the clipboard the required command line parameters that could be used to display the grid
exactly the same way.  You can then go and simply paste commandline parameters in a macro
and call the macro to display the grid.

"""

import sys
import os
import wx
import argparse
import win32api
import win32con
import win32gui
import _mycommon
import natlinkutils
from threading import Timer

class MainFrame (wx.Frame):

    opacity = 0
    LABEL_WIDTH = 10
    LABEL_HEIGHT = 15
    FONT_SIZE = 8
    keyMode = None
    keyRegister = None
    isSticky = False

    # For position mode
    pinColumnWidth = False
    pinNumColumns = False
    pinNumRows = False
    pinRowHeight = False

    # For moving mouse
    nextCursorX = 0
    nextCursorY = 0


    def __init__(self):
        self.ProcessCommandline()

        if self.positionMode:
            wx.Frame.__init__(self, None, title="Custom Grid", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        else:
            if self.alwaysOnTop:
                wx.Frame.__init__(self, None, title="Custom Grid", style=wx.BORDER_NONE | wx.STAY_ON_TOP)
            else:
                wx.Frame.__init__(self, None, title="Custom Grid", style=wx.BORDER_NONE)

        self.windowStyle = self.GetWindowStyle()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)

        self.SetBackgroundColour("White")

        self.CalculateGrid()
        self.DrawGrid()

        self.nextCursorX, self.nextCursorY = win32api.GetCursorPos()

        # Draw background on frame
        self.Show()

        if self.opacity > 0:
            self.MakeTransparent(self.opacity)

    def CalculateGrid(self):
        if self.positionMode:
            # Need to determine x, y of client area
            # In position mode, we just show the frame and fit the grid to the client area
            self.screenClientX, self.screenClientY = win32gui.ClientToScreen(self.GetHandle(), (0, 0))
            clientrect = self.GetClientRect()
            self.clientWidth = clientrect.width
            self.clientHeight = clientrect.height
            self.gridWidth = self.clientWidth - self.LABEL_WIDTH * 2
            self.gridHeight = self.clientHeight - self.LABEL_HEIGHT * 2
            if self.columnWidth == None or self.pinNumColumns:
                self.pinNumColumns = True
                self.columnWidth = self.gridWidth / self.numColumns
            elif self.numColumns == None or self.pinColumnWidth:
                self.pinColumnWidth = True
                self.numColumns = self.gridWidth / self.columnWidth

            if self.rowHeight == None or self.pinNumRows:
                self.pinNumRows = True
                self.rowHeight = self.gridHeight / self.numRows
            elif self.numRows == None or self.pinRowHeight:
                self.pinRowHeight = True
                self.numRows = self.gridHeight / self.rowHeight

            self.screenGridX = self.screenClientX + self.LABEL_WIDTH
            self.screenGridY = self.screenClientY + self.LABEL_HEIGHT
        else:
            # In regular mode, we size the grid according to command line args
            if self.sizeToClient != None:
                # conform grid to the client size
                # get target window
                # is the size to client parameter a string or integer?
                # if it is an integer, assume it is a HWND of an application window.
                # otherwise, it is the name of the process.
                processHwnd = ""
                if self.isInteger(self.sizeToClient):
                    #sizeToClient is an application window HWND
                    processHwnd = int(self.sizeToClient)

                else:
                    #sizeToClient is a process File name.
                    try:
                        win32gui.EnumWindows(_mycommon.checkHwndForProcessName, self.sizeToClient)
                    except:
                        # enumeration complete
                        pass

                    # Found hwnd is stored in mycommon global variable
                    if _mycommon.foundProcessHwnd == None:
                        _mycommon.messageBoxOK('Cannot find window for process "' + self.sizeToClient + '".', "Custom Grid Error")
                        self.DoExit()
                    processHwnd = _mycommon.foundProcessHwnd

                self.screenGridX, self.screenGridY = win32gui.ClientToScreen(processHwnd, (0, 0))
                # returns a tuple (left, top, right, bottom)
                clientrect = win32gui.GetClientRect(processHwnd)

                self.clientWidth = clientrect[2] - clientrect[0] + self.LABEL_WIDTH * 2
                self.clientHeight = clientrect[3] - clientrect[1] + self.LABEL_WIDTH * 2
                self.screenGridX, self.screenGridY = win32gui.ClientToScreen(processHwnd, (0, 0))
                self.gridWidth = self.clientWidth
                self.gridHeight = self.clientHeight
            else:
                # Calculate width if necessary
                if self.gridWidth == None:
                    self.gridWidth = self.columnWidth * self.numColumns

                # Calculate width if necessary
                if self.gridHeight == None:
                    self.gridHeight = self.rowHeight * self.numRows

                # for client width and height add some space to the grid width and height for the labels
                self.clientWidth = self.gridWidth + self.LABEL_WIDTH * 2
                self.clientHeight = self.gridHeight + self.LABEL_HEIGHT * 2

            # Position the grid over the given location.  Push the window up and to the right.
            self.screenClientX = self.screenGridX - self.LABEL_WIDTH
            self.screenClientY = self.screenGridY - self.LABEL_HEIGHT

            # Client area and window area are the same because of no border
            self.SetRect(wx.Rect(self.screenClientX , self.screenClientY, self.clientWidth, self.clientHeight))


    def isInteger(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def DrawGrid(self):
        # Do Screen capture of desktop behind window client area
        self.clientBitmap = wx.EmptyBitmap(self.clientWidth, self.clientHeight)

        memoryDc = wx.MemoryDC()
        memoryDc.SelectObject(self.clientBitmap)

        # If in position mode, do not draw what is behind the frame.
        if self.positionMode:
            memoryDc.SetBackground(wx.Brush(wx.Colour(255, 255, 255)))
            memoryDc.Clear()
        else:
            self.ClearBackground()
            sourceDc = wx.ScreenDC()
            memoryDc.Blit(0, 0, self.clientWidth, self.clientHeight, sourceDc, self.screenClientX, self.screenClientY)

        # Draw grid

        # Labels setup
        memoryDc.SetTextForeground(wx.Colour(255, 255, 255))
        memoryDc.SetTextBackground(wx.Colour(0, 0, 0))
        memoryDc.SetBackgroundMode(wx.SOLID)

        # Columns
        columnx = self.LABEL_WIDTH
        gridWidth = 0
        memoryDc.SetPen(wx.Pen ("#000000", 1))
        columnNum = 1
        if self.columnWidth == None:
              self.columnWidth = self.gridWidth / self.numColumns

        # Make sure label is not too big
        fontSize = self.FONT_SIZE
        memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        extentx, extenty = memoryDc.GetTextExtent('99')
        while extentx > self.columnWidth:
            fontSize = fontSize - 1
            memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            extentx, extenty = memoryDc.GetTextExtent('99')

        # Print columns
        while gridWidth <= self.gridWidth:
            # print line to the left
            memoryDc.DrawLine(columnx, 0, columnx, self.clientHeight)
            # print top label
            memoryDc.DrawText(str(columnNum), columnx + 1, 1)
            # print final label
            memoryDc.DrawText(str(columnNum), columnx + 1, self.clientHeight - extenty)
            columnx = columnx + self.columnWidth
            gridWidth = gridWidth + self.columnWidth
            columnNum = columnNum + 1

        # Right side border
        memoryDc.DrawLine(self.clientWidth - 1, 0, self.clientWidth - 1, self.clientHeight)

        # Rows
        rowy = self.LABEL_HEIGHT
        gridHeight = 0
        rowNum = 1

        if self.rowHeight == None:
            self.rowHeight = self.gridHeight / self.numRows

        # Make sure label is not too big
        fontSize = self.FONT_SIZE
        memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        extentx, extenty = memoryDc.GetTextExtent('99')
        while extenty > self.rowHeight:
            fontSize = fontSize - 1
            memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            extentx, extenty = memoryDc.GetTextExtent('99')

        # print rows
        while gridHeight <= self.gridHeight:
            # Print line above
            memoryDc.DrawLine(0, rowy, self.clientWidth, rowy)
            # Print left label
            memoryDc.DrawText(str(rowNum), 1, rowy + 1)
            # Print right labal
            memoryDc.DrawText(str(rowNum), self.clientWidth - extentx, rowy + 1)
            rowy = rowy + self.rowHeight
            gridHeight = gridHeight + self.rowHeight
            rowNum = rowNum + 1

        # Bottom border
        memoryDc.DrawLine(0, self.clientHeight - 1, self.clientWidth, self.clientHeight - 1)

        # Draw dot at top left corner for position mode
        if self.positionMode:
            memoryDc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
            memoryDc.DrawCircle(self.LABEL_WIDTH, self.LABEL_HEIGHT, 2)

        # All done
        memoryDc.SelectObject(wx.NullBitmap)

    def OnPaint(self, event):
        if self.positionMode:
            dc = wx.PaintDC(self)
            self.CalculateGrid()
            self.DrawGrid()
            dc.DrawBitmap(self.clientBitmap, 0, 0)
        else:
            dc = wx.BufferedPaintDC(self, self.clientBitmap)

        return

    def OnActivate(self, event):
        # This prevents an annoying beep from occurring when the application is activated
        # via AppBringUp in a macro.
        self.SetFocus()
        event.Skip()

    def OnKeyDown (self, event) :
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_ESCAPE:
            # hide the grid
            self.Iconize()
        elif  keycode == wx.WXK_RETURN:
            # Move the mouse to the next location
            self.FinishKeyMode()
            Timer(0.1, self.moveMouse).start()
            #wx.CallAfter(self.moveMouse)
        elif keycode == wx.WXK_UP:
            # increase row height
            self.rowHeight = self.rowHeight + 1
            self.CalculateGrid()
            self.DrawGrid()
            self.Refresh()
        elif keycode == wx.WXK_DOWN:
            # decrease row height
            self.rowHeight = self.rowHeight - 1
            self.CalculateGrid()
            self.DrawGrid()
            self.Refresh()
        elif keycode == wx.WXK_LEFT:
            # decrease column width
            self.columnWidth = self.columnWidth - 1
            self.CalculateGrid()
            self.DrawGrid()
            self.Refresh()
        elif keycode == wx.WXK_RIGHT:
            # increase column width
            self.columnWidth = self.columnWidth + 1
            self.CalculateGrid()
            self.DrawGrid()
            self.Refresh()
        else:
            # Characters
            try:
                key = chr(keycode).lower()
            except:
                # Not a character
                return

            if keycode >= ord('0') and keycode <= ord('9'):
                if self.keyMode == 'r' or self.keyMode == 'c':
                    # Entering a row or column number
                    if self.keyRegister == None:
                        self.keyRegister = ""
                    self.keyRegister = self.keyRegister + key
            elif key == 'r':
                # row
                self.FinishKeyMode()
                self.keyMode = 'r'
            elif key == 'c':
                # column
                if event.ControlDown():
                    # copy the current parameters onto the clipboard
                    self.ReportValues(False)
                else:
                    # Select column
                    self.FinishKeyMode()
                    self.keyMode = 'c'
            elif key == 's':
                # single click
                self.doHide()
                self.FinishKeyMode()
                Timer(0.1, self.clickMouse).start()
            elif key == 'd':
                # double click
                self.doHide()
                self.FinishKeyMode()
                Timer(0.1, self.doubleClickMouse).start()
            elif key == 't':
                # right-click
                self.doHide()
                self.FinishKeyMode()
                Timer(0.1, self.rightClickMouse).start()
            elif key == 'y':
                # toggle sticky setting.
                # If sticky, the grid will remain visible
                # after issuing a click command
                self.isSticky = not self.isSticky;
            elif key  == 'h':
                # refresh display
                self.DrawGrid()
                self.Refresh()
            elif key == 'x':
                # Terminate
                self.Close()
            elif key == 'l':
                # Prompt for new command line and apply settings
                dlg = wx.TextEntryDialog(self, "Enter the new command line switches you would like to apply:",
                                                "Custom Grid Change Settings")
                if dlg.ShowModal() == wx.ID_OK:
                    newSettings = dlg.GetValue()
                    self.ProcessCommandline(newSettings)
                    self.CalculateGrid()
                    self.DrawGrid()
                    if self.opacity > 0:
                        self.MakeTransparent(self.opacity)
                    if self.alwaysOnTop:
                        self.SetWindowStyle(self.windowStyle | wx.STAY_ON_TOP)
                    else:
                        self.SetWindowStyle(self.windowStyle)
                    self.Refresh()
                dlg.Destroy()
            elif key == '/':
                parser = self.getParser()
                helpString = parser.format_help()
                _mycommon.messageBoxOK(helpString, "Custom Grid Help")
            else:
                self.FinishKeyMode()

        event.Skip()

    def FinishKeyMode (self):
        # If specifying the row or column, save the new location
        # Based on the number in the key register
        if self.keyMode == 'r':
            self.nextCursorY = self.screenClientY + self.LABEL_HEIGHT + self.rowHeight * (int(self.keyRegister) - 1) + self.rowHeight / 2
        elif self.keyMode == 'c':
            self.nextCursorX = self.screenClientX + self.LABEL_WIDTH + self.columnWidth * (int(self.keyRegister) - 1) + self.columnWidth / 2

        self.keyMode = None
        self.keyRegister = None

    def moveMouse(self):
        win32api.SetCursorPos((self.nextCursorX, self.nextCursorY))

    def clickMouse(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
        self.stickyShow()

    def doubleClickMouse(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
        self.stickyShow()

    def rightClickMouse(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.nextCursorX, self.nextCursorY, 0, 0)
        self.stickyShow()

    def doHide(self):
        # Is a sticky, then hide the window rather than minimize it.
        # Hiding and showing is faster than minimizing and maximizing
        if self.isSticky:
            self.Show(False)
        else:
            self.Iconize()

    def stickyShow(self):
        if self.isSticky:
            #Timer(0.5, self.delayedShow).start()
            wx.CallAfter(self.delayedShow)

    def delayedShow(self):
        self.DrawGrid()
        self.Refresh()
        self.Show(True)
        win32gui.SetForegroundWindow(self.GetHandle())

    def OnClose(self, event):
        if self.positionMode:
            self.ReportValues(True)

        event.Skip()

    def ReportValues(self, promptBeforeCopy):
        # update values
        self.CalculateGrid()
        data = "Grid location x: " + str(self.screenGridX)  + \
                "\nGrid location y: " + str(self.screenGridY) + \
                "\nGrid width: " + str(self.gridWidth) + \
                "\nGrid height: " + str(self.gridHeight) + \
                "\nColumn width: " + str(self.columnWidth) + \
                "\nRow height: " + str(self.rowHeight) + \
                "\nNumber columns: " + str(self.numColumns) + \
                "\nNumber rows: " + str(self.numRows)

        # Print to command line
        print data

        doCopy = False
        if promptBeforeCopy:
            data += '\n\nCopy the parameters into the clipboard as the commandline switches needed to run the grid?'
            if _mycommon.messageBoxYesNo(data, "Custom Grid Results") == _mycommon.MESSAGEBOX_RETURN_YES:
                doCopy = True
        else:
            # Just copy
            doCopy = True

        if doCopy:
            _mycommon.setClipboard('--width ' + str(self.gridWidth) + \
                                   ' --height ' + str(self.gridHeight) + \
                                   ' --locationx ' + str(self.screenGridX) + \
                                   ' --locationy ' + str(self.screenGridY) + \
                                   ' --rowheight ' + str(self.rowHeight) + \
                                   ' --columnwidth ' + str(self.columnWidth) + \
                                   ' --numrows ' + str(self.numRows) + \
                                   ' --numcolumns ' + str(self.numColumns))

        if not promptBeforeCopy:
            data += '\n\nCommandline switches for the above parameters have been copied into the clipboard.'
            _mycommon.messageBoxOK(data, "Custom Grid Results")

    def getParser(self):
        parser = argparse.ArgumentParser(description="Displays a custom grid to assist with voice recognition control of the mouse.",
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=
'''Once the grid is displayed, you can control the application using the following commands:
    ?: show this helpdisplay text.

    r##: move the pointer to the indicated row.  To move to row 23, type 'r23' followed by <enter>.
    c##: move the pointer to the indicated column.  To move to column 45, type 'c45' followed by <enter>.
    You can also combine a row and column in a single command:  'r23c45' followed by <enter>  does a single move.

    s: single click the mouse.
    d: double click the mouse.
    t: right click the mouse.

    y: toggle the sticky setting.  If sticky, the grid will remain displayed after issuing a click.
                                   If not sticky, the grid will close after issuing a click.
    h: refresh the display. This is especially useful with the "sticky" setting turned on.
    l: allow you to enter new command line arguments and reconfigure the grid without restarting the application.

    <up arrow>: increase row height
    <down arrow>: decrease row height
    <left arrow>: decrease column width
    <right arrow>: increase column width

    <ctrl>c: copy the current parameters into the clipboard as the commandline switches needed to run the grid

    <esc>: hide the grid.
    x: close the application.

In position mode, the origin of the grid as indicated by a small circle at the top left corner of the grid.  This point will be the locationx and location y values.''')

        parser.add_argument("-p", "--positionMode", action="store_true",
                help="Allows you to resize the grid and determine the desired parameters.  When the window is closed, parameters are printed to the command line.")
        parser.add_argument("--width", action="store", type=int,
                help="Specify the width of the grid in pixels.  You may omit this switch if you specify both --columnwidth and --numcolumns.")
        parser.add_argument("--height", action="store", type=int,
                help="Specify the height of the grid in pixels.  You may omit this switch if you specify both --rowheight and --numrows.")
        parser.add_argument("--locationx", action="store", type=int, default='0',
                help="Specify the x pixel screen coordinates of the upper left corner of the grid.  Default is 0.")
        parser.add_argument("--locationy", action="store", type=int, default='0',
                help="Specify the y pixel screen coordinates of the upper left corner of the grid.  Default is 0.")
        parser.add_argument("--sizeToClient", action="store",
                help="Use this switch to size and position the grid over the client window of the given application.  " + \
                     "Specify the process file name of the target application or the HWND of the application window. " + \
                     "This switch overrides the width, height, locationx and locationy switches.  " + \
                     "It is ignored in position mode.")
        parser.add_argument("--rowheight", action="store", type=int, help ='Specify the height of a grid row in pixels.')
        parser.add_argument("--columnwidth", action="store", type=int, help ='Specify the width of a grid column in pixels.')
        parser.add_argument("--numrows", action="store", type=int, help ='Specify the number of rows in the grid.')
        parser.add_argument("--numcolumns", action="store", type=int, help ='Specify the number of columns in the grid.')
        parser.add_argument("--sticky", action="store_true", help='Include this switch to make the grid sticky.')
        parser.add_argument("--opacity", action="store", type=int, help='Value from 0 to 100.  0 makes the grid completely transparent.  100 makes the grid completely opaque.')
        parser.add_argument("--alwaysontop", action="store_true", help='Include this switch to make the grid stay on top of all windows.')
        return parser

    def ProcessCommandline(self, argsString=None):
        parser = self.getParser()
        try:
            if argsString == None:
                # use sys.argv
                args = parser.parse_args()
            else:
                # Use given argsString
                args = parser.parse_args(argsString.split())
        except Exception, ex:
            _mycommon.messageBoxOK("Error while parsing arguments: " + ex.message, 'Custom Grid Error')

        self.positionMode = args.positionMode
        self.gridWidth = args.width
        self.gridHeight = args.height
        self.screenGridX = args.locationx
        self.screenGridY = args.locationy
        self.sizeToClient = args.sizeToClient
        self.rowHeight = args.rowheight
        self.columnWidth= args.columnwidth
        self.numRows = args.numrows
        self.numColumns = args.numcolumns
        self.isSticky = args.sticky
        self.opacity= args.opacity
        self.alwaysOnTop= args.alwaysontop

        # When in position mode, you must specify either the column width or the number of columns
        # The --width switch is ignored.
        if self.positionMode and (self.columnWidth == None and self.numColumns == None):
            # provide defaults
            self.numColumns = 20
            #self.DoExit('When using the --positionMode switch, you must specify either --columnwidth or --numcolumns.  --width is ignored.')

        # When in position mode, you must specify either the Row height or the number of Rose
        # The --height switch is ignored.
        if self.positionMode and (self.rowHeight == None and self.numRows == None):
            # provide defaults
            self.numRows = 20
            # self.DoExit('When using the --positionMode switch, you must specify either --rowheight or --numrows.  --height is ignored.')

        # You must specify 2 of the following 3 switches --width, --columnwidth, --numcolumns
        if (self.gridWidth == None and self.columnWidth == None) or \
           (self.gridWidth == None and self.numColumns == None) or \
           (self.columnWidth == None and self.numColumns == None):
            # provide defaults
            self.columnWidth = 20
            self.numColumns= 20
            # self.DoExit(' You must specify 2 of the following 3 switches:  --width, --columnwidth, --numcolumns')


        # You must specify 2 of the following 3 switches --height, --rowheight, --numrows
        if (self.gridHeight == None and self.rowHeight == None) or \
           (self.gridHeight == None and self.numRows == None) or \
           (self.rowHeight == None and self.numRows == None):
            # provide defaults
            self.rowHeight = 20
            self.numRows = 20
            # self.DoExit(' You must specify 2 of the following 3 switches:  --height, --rowheight, --numrows')

        if self.opacity != None:
            if self.opacity < 0 or self.opacity > 100:
                self.DoExit('The value for the opacity switch must be between 0 and 100, inclusive.')

        # set default opacity for position mode
        if self.opacity == None:
            if self.positionMode:
                self.opacity = 25
            else:
                self.opacity = 50


        if self.sizeToClient != None:
            if self.sizeToClient == '':
                self.DoExit('The value for the sizeToClient must be an application file name.')

    def DoExit(self, message):
        print message
        wx.MessageBox(message, "Custom Grid Error")
        os._exit(1)

    # Got from http://wiki.wxpython.org/Transparent%20Frames
    # 0 = fully transparent
    # 100 = fully opaque
    def MakeTransparent(self, alpha):
        import os, sys

        # input parameter Excel you from 0 to 100 to be consistent with other
        # transparency models.
        # The method below takes a value from 0 to 255.  Need to make the mapping.
        winAlpha = int(alpha * 2.55)

        if sys.platform == 'win32':
            hwnd = self.GetHandle()
            try :
                import ctypes   # DLL library interface constants' definitions
                _winlib = ctypes.windll.user32    # create object to access DLL file user32.dll
                style = _winlib.GetWindowLongA( hwnd, 0xffffffecL )
                style |= 0x00080000
                _winlib.SetWindowLongA( hwnd, 0xffffffecL, style )
                _winlib.SetLayeredWindowAttributes( hwnd, 0, winAlpha, 2 )

            except ImportError :
                import win32api, win32con, winxpgui
                _winlib = win32api.LoadLibrary( "user32" )
                pSetLayeredWindowAttributes = win32api.GetProcAddress(_winlib, "SetLayeredWindowAttributes" )
                if pSetLayeredWindowAttributes == None :
                    return
                exstyle = win32api.GetWindowLong( hwnd, win32con.GWL_EXSTYLE )
                if 0 == ( exstyle & 0x80000 ) :
                    win32api.SetWindowLong( hwnd, win32con.GWL_EXSTYLE, exstyle | 0x80000 )
                winxpgui.SetLayeredWindowAttributes( hwnd, 0, amount, 2 )
        else :
            print '####  OS Platform must be MS Windows'
            self.Destroy()


app = wx.App(False)
frame = MainFrame()
app.MainLoop()