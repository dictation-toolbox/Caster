"""
---------------------------
Custom Grid Help
---------------------------
usage: CustomGrid.py [-h] [-p] [--width WIDTH] [--height HEIGHT]
                     [--locationx LOCATIONX] [--locationy LOCATIONY]
                     [--sizeToClient SIZETOCLIENT] [--rowheight ROWHEIGHT]
                     [--columnwidth COLUMNWIDTH] [--numrows NUMROWS]
                     [--numcolumns NUMCOLUMNS] [--sticky] [--opacity OPACITY]
                     [--alwaysontop]

Displays a custom grid to assist with voice recognition control of the mouse.

optional arguments:
  -h, --helpdisplay            show this helpdisplay message and exit
  -p, --positionMode    Allows you to resize the grid and determine the
                        desired parameters. When the window is closed,
                        parameters are printed to the command line.
  --width WIDTH         Specify the width of the grid in pixels. You may omit
                        this switch if you specify both --columnwidth and
                        --numcolumns.
  --height HEIGHT       Specify the height of the grid in pixels. You may omit
                        this switch if you specify both --rowheight and
                        --numrows.
  --locationx LOCATIONX
                        Specify the x pixel screen coordinates of the upper
                        left corner of the grid. Default is 0.
  --locationy LOCATIONY
                        Specify the y pixel screen coordinates of the upper
                        left corner of the grid. Default is 0.
  --sizeToClient SIZETOCLIENT
                        Use this switch to size and position the grid over the
                        client window of the given application. Specify the
                        process file name of the target application or the
                        HWND of the application window. This switch overrides
                        the width, height, locationx and locationy switches.
                        It is ignored in position mode.
  --rowheight ROWHEIGHT
                        Specify the height of a grid row in pixels.
  --columnwidth COLUMNWIDTH
                        Specify the width of a grid column in pixels.
  --numrows NUMROWS     Specify the number of rows in the grid.
  --numcolumns NUMCOLUMNS
                        Specify the number of columns in the grid.
  --sticky              Include this switch to make the grid sticky.
  --opacity OPACITY     Value from 0 to 100. 0 makes the grid completely
                        transparent. 100 makes the grid completely opaque.
  --alwaysontop         Include this switch to make the grid stay on top of
                        all windows.

Once the grid is displayed, you can control the application using the following commands:
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

In position mode, the origin of the grid as indicated by a small circle at the top left corner of the grid.  This point will be the locationx and location y values.

"""


#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, MappingRule,
                       Choice, IntegerRef, Playback,
                       Key, Function)
import sys
from lib import paths, utilities

BASE_PATH=paths.BASE_PATH

def navigate_grid(n, n2, click):
    Key("c").execute()
    utilities.press_digits(n)
    Key("r").execute()
    utilities.press_digits(n2)
    Key("enter").execute()
    if not click=="0":
        Key(str(click)).execute()
        
def single_line(line,n):
    try:
        Key(line).execute()
        utilities.press_digits(n)
        Key("enter").execute()
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
    
class CommandRule(MappingRule):

    mapping = {
        'helpdisplay':                 Key("question"),
        "(<n> by <n2> | row <n2> column <n> | column <n> row <n2>) [<click>]":Function(navigate_grid,extra={'n', 'n2','click'}),
        "<line> <n>":           Function(single_line,extra={'line','n'}),
        
        "I left":               Key("s"),
        "I double":             Key("d"),
        "I right":              Key("t"),
        
        "sticky":               Key("y"),
        "refresh":              Key("h"),
        "reconfigure":          Key("l"),
        "increase row height":  Key("up"),
        "decrease row height":  Key("down"),
        "decrease column width":Key("left"),
        "increase column width":Key("right"),
        "copy parameters":      Key("c-c"),
        "hide":                 Key("escape"),
        "exit":                 Key("x"),
        

        
        }
    extras = [
              IntegerRef("n", 1, 1000),
              IntegerRef("n2", 1, 1000),
              Choice("click",
                    {"default": "0", "left": "s", "double": "d",
                     "dub": "d", "right": "t", "kick": "s"
                    }),
              Choice("line",
                    {"row": "r", "column": "c",
                    }),
             ]
    defaults ={"n": 1,"click":"0"}

#---------------------------------------------------------------------------

context = AppContext(executable="CustomGrid")
grammar = Grammar("Custom Grid", context=context)
grammar.add_rule(CommandRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None