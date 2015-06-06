from SimpleXMLRPCServer import *
import SimpleXMLRPCServer
from ctypes import *
import getopt
import re
import sys
import threading

from PIL import ImageGrab




try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem/"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from caster.asynch.mouse.grids import TkTransparent, Dimensions
    from caster.lib import settings, utilities

class Rectangle:
    top = None
    bottom = None
    left = None
    right = None

class LegionGrid(TkTransparent):
    def __init__(self, grid_size=None, tirg=None, auto_quit=False):
        self.setup_XMLRPC_server()
        TkTransparent.__init__(self, settings.LEGION_TITLE, grid_size)
        self.attributes("-alpha", 0.7)
        
        self.tirg_positions = {}
        if tirg != None:
            self.process_rectangles(tirg)
            self.draw_tirg_squares()
        
        self.mainloop()
    
    def setup_XMLRPC_server(self): 
        TkTransparent.setup_XMLRPC_server(self)
        self.server.register_function(self.xmlrpc_retrieve_data_for_highlight, "retrieve_data_for_highlight")
        self.server.register_function(self.xmlrpc_go, "go")
    
    def xmlrpc_go(self, index):
        self.move_mouse(int(self.tirg_positions[index][0]+self.dimensions.x), 
                        int(self.tirg_positions[index][1]+self.dimensions.y))
    
    def xmlrpc_retrieve_data_for_highlight(self, strindex):
        if strindex in self.tirg_positions:
            position_data = self.tirg_positions[strindex]
            return {"l": position_data[2]+self.dimensions.x, 
                    "r": position_data[3]+self.dimensions.x, 
                    "y": position_data[1]+self.dimensions.y}
        else:
            return {"err": strindex + " not in map"}
    
    def process_rectangles(self, tirg_string):   
        self.tirg_rectangles = []
        if tirg_string.endswith(",") :
            tirg_string = tirg_string[:-1]
        tirg_list = tirg_string.split(",")
        curr_rect = None
        for i in range(0, len(tirg_list)):
            ii = i % 4
            if ii == 0:
                curr_rect = Rectangle()
                curr_rect.left = int(tirg_list[i])#-self.dimensions.x
            elif ii == 1:
                curr_rect.top = int(tirg_list[i])#-self.dimensions.y
            elif ii == 2:
                curr_rect.right = int(tirg_list[i])#-self.dimensions.x
            elif ii == 3:
                curr_rect.bottom = int(tirg_list[i])#-self.dimensions.y
                self.tirg_rectangles.append(curr_rect) 
    
    
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
            center_x = int((rect.left + rect.right) / 2)
            center_y = int((rect.top + rect.bottom) / 2)
            label = str(rect_num)
            # lines
            self._canvas.create_line(rect.left, rect.top, rect.right, rect.top, fill=fill_inner)
            self._canvas.create_line(rect.left, rect.bottom, rect.right, rect.bottom, fill=fill_inner)
            self._canvas.create_line(rect.left, rect.top, rect.left, rect.bottom, fill=fill_inner)
            self._canvas.create_line(rect.right, rect.top, rect.right, rect.bottom, fill=fill_inner)
            
            # text
            self._canvas.create_text(center_x + 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x - 1, center_y + 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x + 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x - 1, center_y - 1, text=label, font=font, fill=fill_outer)
            self._canvas.create_text(center_x, center_y, text=label, font=font, fill=fill_inner)
            
            # rect.left, rect.right are now being saved below for the highlight function
            self.tirg_positions[label] = (center_x, center_y, rect.left, rect.right)
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
        self.tirg_dll = cdll.LoadLibrary(settings.SETTINGS["paths"]["DLL_PATH"] + "tirg-dll.dll")
        self.tirg_dll.getTextBBoxesFromFile.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromFile.restype = c_char_p
        self.tirg_dll.getTextBBoxesFromBytes.argtypes = [c_char_p, c_int, c_int]
        self.tirg_dll.getTextBBoxesFromBytes.restype = c_char_p
        
    def tirg_scan(self, img):
        bbstring = self.tirg_dll.getTextBBoxesFromBytes(img.tobytes(), img.size[0], img.size[1])
        # clean the results in case any garbage letters come through
        result = re.sub("[^0-9,]", "", bbstring)
        return result
        
    def scan(self, bbox=None):
        #bbox=(10,10,500,500)
        img = ImageGrab.grab(bbox)
        result = self.tirg_scan(img)
        if result != self.last_signature:
            with self.lock:
                self.last_signature = result
                self.screen_has_changed = True
        # do rectangle scans here
        
    def get_update(self):
        with self.lock:
            if self.screen_has_changed:
                self.screen_has_changed = False
                return (self.last_signature, None)  # None should be replaced with rectangle scan results
            else:
                return None


def main(argv):
    help_message = 'legion.py -t <tirg> -d <dimensions> -a <autoquit>'
    tirg = None
    dimensions = None
    auto_quit = False
    try:
        opts, args = getopt.getopt(argv, "ht:a:d:", ["tirg=", "dimensions=", "autoquit="])
    except getopt.GetoptError:
        print help_message
        sys.exit(2)
    try:
        for opt, arg in opts:
            if opt == '-h':
                print help_message
                sys.exit()
            elif opt in ("-t", "--tirg"):
                tirg = arg
            elif opt in ("-d", "--dimensions"):
                # wxh+x+y
                dimensions = Dimensions(*[int(n) for n in arg.split("_")])
            elif opt in ("-a", "--autoquit"):
                auto_quit = arg in ("1", "t")    
        
        lg = LegionGrid(grid_size=dimensions, tirg=tirg, auto_quit=auto_quit)
    except Exception:
        utilities.simple_log(True)
        
        

if __name__ == "__main__":
    main(sys.argv[1:])
