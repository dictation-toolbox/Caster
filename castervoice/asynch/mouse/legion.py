from builtins import str

import getopt
import os
import re
import sys
import threading
from ctypes import *
from dragonfly import monitors

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.asynch.mouse.grids import TkTransparent, Dimensions
    from castervoice.lib import gdi, settings, utilities
    settings.initialize()

import six
if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error

try:
    from PIL import ImageGrab, ImageFilter, Image
except ImportError:
    utilities.availability_message("Legion", "PIL")
'''
The screen will be divided into vertical columns of equal width.
The width of each Legion box cannot exceed the width of the column.
This way relative partitioning is achieved since larger resolutions 
will be partitioned into columns of larger width.
'''


class Rectangle:
    y1 = None
    y2 = None
    x1 = None
    x2 = None


class LegionGrid(TkTransparent):
    def __init__(self, grid_size=None, tirg=None, auto_quit=False):
        self.setup_xmlrpc_server()
        TkTransparent.__init__(self, settings.LEGION_TITLE, grid_size)
        self.attributes("-alpha", 0.7)
        self.max_rectangle_width = int(
            grid_size.width/settings.SETTINGS["miscellaneous"]["legion_vertical_columns"])
        self.tirg_positions = {}
        if tirg is not None:
            self.process_rectangles(tirg)
            self.draw_tirg_squares()

        self.mainloop()

    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        self.server.register_function(self.xmlrpc_retrieve_data_hlight,
                                      "retrieve_data_for_highlight")
        self.server.register_function(self.xmlrpc_go, "go")

    def xmlrpc_go(self, index):
        self.move_mouse(
            int(self.tirg_positions[index][0] + self.dimensions.x),
            int(self.tirg_positions[index][1] + self.dimensions.y))

    def xmlrpc_retrieve_data_hlight(self, strindex):
        if strindex in self.tirg_positions:
            position_data = self.tirg_positions[strindex]
            return {
                "l": position_data[2] + self.dimensions.x,
                "r": position_data[3] + self.dimensions.x,
                "y": position_data[1] + self.dimensions.y
            }
        else:
            return {"err": strindex + " not in map"}

    def process_rectangles(self, tirg_string):
        self.tirg_rectangles = []
        if tirg_string.endswith(","):
            tirg_string = tirg_string[:-1]
        tirg_list = tirg_string.split(",")
        curr_rect = None
        for i in range(0, len(tirg_list)):
            ii = i % 4
            if ii == 0:
                curr_rect = Rectangle()
                curr_rect.x1 = int(tirg_list[i])
            elif ii == 1:
                curr_rect.y1 = int(tirg_list[i])
            elif ii == 2:
                curr_rect.x2 = int(tirg_list[i])
            elif ii == 3:
                curr_rect.y2 = int(tirg_list[i])
                self.tirg_rectangles.append(curr_rect)
        self.split_rectangles()

    def split_rectangles(self):
        # Split larger rectangles into smaller ones to allow greater precision.
        rectangles_to_split = []
        for rect in self.tirg_rectangles:  # Collect all the rectangles that are too large.
            if rect.x2 - rect.x1 >= self.max_rectangle_width:
                rectangles_to_split.append(rect)
        self.tirg_rectangles = [
            x for x in self.tirg_rectangles if x not in rectangles_to_split
        ]  # Remove large rectangles.
        self.perform_split(rectangles_to_split)

    def perform_split(self, rectangles_to_split):
        # Helper class for splitting larger rectangles to smaller ones.
        for rect in rectangles_to_split:
            width = rect.x2 - rect.x1
            pieces = width/self.max_rectangle_width
            new_width = width/pieces
            for i in range(0, pieces):
                r = Rectangle()
                r.x1 = rect.x1 + new_width*i
                r.y1 = rect.y1
                r.x2 = r.x1 + new_width
                r.y2 = rect.y2
                self.tirg_rectangles.append(r)

    def draw(self):
        ''' or self.server.has_rect_update'''
        self.pre_redraw()
        self.draw_tirg_squares()
        self.unhide()

    def draw_tirg_squares(self):
        ''''''
        font = "Arial 12 bold"
        fill_inner = "Orange"
        fill_outer = "Black"
        rect_num = 0
        for rect in self.tirg_rectangles:
            center_x = int((rect.x1 + rect.x2)/2)
            center_y = int((rect.y1 + rect.y2)/2)
            label = str(rect_num)
            # lines
            self._canvas.create_line(rect.x1, rect.y1, rect.x2, rect.y1, fill=fill_inner)
            self._canvas.create_line(rect.x1, rect.y2, rect.x2, rect.y2, fill=fill_inner)
            self._canvas.create_line(rect.x1, rect.y1, rect.x1, rect.y2, fill=fill_inner)
            self._canvas.create_line(rect.x2, rect.y1, rect.x2, rect.y2, fill=fill_inner)

            # text
            self._canvas.create_text(
                center_x + 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(
                center_x - 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(
                center_x + 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(
                center_x - 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(
                center_x, center_y, text=label, font=font, fill=fill_inner)
            '''rect.x1, rect.x2 are now being saved below for the highlight function'''
            self.tirg_positions[label] = (center_x, center_y, rect.x1, rect.x2)
            rect_num += 1


class LegionScanner:
    def __init__(self):
        # setup dll
        self.tirg_dll = None
        self.setup_dll()

        self.lock = threading.Lock()
        self.last_signature = None
        self.screen_has_changed = False

    def setup_dll(self):
        import sys
        import struct
        try:
            if struct.calcsize("P") * 8 == 32:
                self.tirg_dll = cdll.LoadLibrary(str(Path(settings.SETTINGS["paths"]["DLL_PATH"]).joinpath("tirg-32.dll")).encode(
                sys.getfilesystemencoding()))
            else:
                self.tirg_dll = cdll.LoadLibrary(str(Path(settings.SETTINGS["paths"]["DLL_PATH"]).joinpath("tirg-64.dll")).encode(
                sys.getfilesystemencoding()))
        except Exception as e:
            print("Legion loading failed with '%s'" % str(e))
        self.tirg_dll.getTextBBoxesFromFile.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromFile.restype = c_char_p
        self.tirg_dll.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromBytes.restype = c_char_p

    def tirg_scan(self, img):
        bbstring = self.tirg_dll.getTextBBoxesFromBytes(img.tobytes(), img.size[0],
                                                        img.size[1])
        # clean the results in case any garbage letters come through
        result = re.sub("[^0-9,]", "", bbstring)
        return result

    def scan(self, bbox=None, rough=True):
        # ImageGrab.grab currently doesn't support multiple monitors.
        # If PIL gets updated with multimon support, this can be switched back.
        img = gdi.grab_screen(bbox)  # ImageGrab.grab(bbox)
        if rough:
            factor = settings.SETTINGS["miscellaneous"]["legion_downscale_factor"]
            if str(factor) == "auto":
                # Choose a fixed "rough" final size that will work in most circumstances
                factor = min(1500 / float(img.size[0]), 1)
            new_size = (img.size[0]*factor, img.size[1]*factor)
            img.thumbnail(new_size)
        

        img = img.filter(ImageFilter.FIND_EDGES)
        result = self.tirg_scan(img)
        if rough:
            result = result.split(",")
            result = list(filter(None, result)) # Removes empty items
            result= [int(float(i)/factor) for i in result]
            result = ",".join(str(bit) for bit in result)
            
        if result != self.last_signature:
            with self.lock:
                self.last_signature = result
                self.screen_has_changed = True
        # do rectangle scans here

    def get_update(self):
        with self.lock:
            if self.screen_has_changed:
                self.screen_has_changed = False
                return self.last_signature, None  # None should be replaced with rectangle scan results
            else:
                return None


def main(argv):
    help_message = 'legion.py -t <tirg> [-m <monitor>] [-d <dimensions>] [-a <autoquit>]'
    tirg = None
    monitor = 1
    dimensions = None
    auto_quit = False

    error_code = windll.shcore.SetProcessDpiAwareness(2)  #enable 1-1 pixel mapping
    if error_code == -2147024891:
        raise OSError("Failed to set app awareness")

    try:
        opts, args = getopt.getopt(argv, "ht:a:d:m:",
                                   ["tirg=", "dimensions=", "autoquit="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    try:
        for opt, arg in opts:
            if opt == '-h':
                print(help_message)
                sys.exit()
            elif opt in ("-t", "--tirg"):
                tirg = arg
            elif opt == '-m':
                monitor = arg
            elif opt in ("-d", "--dimensions"):
                # wxh+x+y
                dimensions = Dimensions(*[int(n) for n in arg.split("_")])
            elif opt in ("-a", "--autoquit"):
                auto_quit = arg in ("1", "t")

        if dimensions is None:
            r = monitors[int(monitor) - 1].rectangle
            dimensions = Dimensions(int(r.dx), int(r.dy), int(r.x), int(r.y))

        lg = LegionGrid(grid_size=dimensions, tirg=tirg, auto_quit=auto_quit)
    except Exception:
        utilities.simple_log(True)


if __name__ == "__main__":
    main(sys.argv[1:])
