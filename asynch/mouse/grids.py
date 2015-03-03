from __future__ import division

import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
import getopt
import signal
import sys
from threading import Timer
import time

from PIL import ImageGrab, ImageTk, ImageDraw, ImageFont
import win32api

import Tkinter as tk


try:
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
    from lib import  settings
except Exception:
    from lib import  settings

def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.GRIDS_LISTENING_PORT))

class Dimensions:
    def __init__(self, w, h, x, y):
        self.width = w
        self.height = h
        self.x = x
        self.y = y



# rewrite dp grid using this
class TkTransparent(tk.Tk):
    
    def reset_xs_ys(self):
        self.xs = []
        self.ys = []
        
    def xs_ys_filled(self):
        return len(self.xs) > 0 or len(self.ys) > 0;
    
    def get_dimensions_fullscreen(self):
        return Dimensions(self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0)
    
    def get_dimensions_string(self):
        return "%dx%d+%d+%d" % (self.dimensions.width, self.dimensions.height, self.dimensions.x, self.dimensions.y)
    
    def key(self, e):
        '''virtual method'''  # e.char
    
    def __init__(self, name, dimensions=None):
        tk.Tk.__init__(self, baseName="")
        self.setup_XMLRPC_server()
        if not dimensions:
            dimensions = self.get_dimensions_fullscreen()
        self.dimensions = dimensions
        self.reset_xs_ys()
        self.overrideredirect(True)  
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.wait_visibility(self)
        self.attributes("-alpha", 0.5)
        self.wm_title(name)
        self.wm_geometry(self.get_dimensions_string())
        self._canvas = tk.Canvas(master=self, width=dimensions.width, height=dimensions.height, bg='white', bd=-2)
        self._canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)
#        self.bind("<Key>", self.key)
        # self.mainloop()#do this in the child classes
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", settings.GRIDS_LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_kill, "kill")
    
    def pre_redraw(self):
        '''gets the window ready to be redrawn'''
        self.deiconify()
        self._canvas.delete("all")
        
    
    def unhide(self):
        ''''''
        self.deiconify()
        self.lift()
        time.sleep(0.1) 
        self.focus_force()
        self.focus_set() 
        self.focus() 
    
    def hide(self):
        self.withdraw()
    
    def xmlrpc_kill(self):
        self.after(10, self.die)
    
    def die(self):
        self.server_quit = 1
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
        
    def move_mouse(self, mx, my):
        win32api.SetCursorPos((mx, my))

            
            

class RainbowGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, square_alpha=None):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "rainbowgrid", grid_size)
        self.attributes("-alpha", 0.5)
        self.square_size = square_size if square_size else 37
        self.square_alpha = square_alpha if square_alpha else 125
        self.colors = [(255, 0, 0, self.square_alpha),  # red
                       (187, 122, 0, self.square_alpha),  # orange 255, 165, 0
                       (255, 255, 0, self.square_alpha),  # yellow
                       (0, 128, 0, self.square_alpha),  # green
                       (0, 0, 125, self.square_alpha),  # blue
                       (128, 0, 128, self.square_alpha)  # purple
                       ]
        self.position_index = None

        self.info_pre = 0
        self.info_color = 0
        self.info_num = 0
        
        self.refresh()
        self.mainloop()
    
    def refresh(self):
        '''thread safe'''
        self.hide()
        self.after(10, self.draw)
    
    def finalize(self):
        self.imgtk = ImageTk.PhotoImage(self.img)
        self._canvas.create_image(self.dimensions.width / 2, self.dimensions.height / 2, image=self.imgtk)
    
    def setup_XMLRPC_server(self):
        TkTransparent.setup_XMLRPC_server(self)
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")
    
    def xmlrpc_move_mouse(self, pre, color, num):
        if pre > 0:
            pre -= 1
        selected_index = self.position_index[color + pre * len(self.colors)][num]
        self.move_mouse(selected_index[0], selected_index[1])
    
    def process(self):
        ''''''
        if self.mode == "p":
            self.info_pre = int(self.digits)
            if self.info_pre > 0:
                self.info_pre -= 1
        elif self.mode == "c":
            self.info_color = int(self.digits)
        elif self.mode == "n":
            self.info_num = int(self.digits)
            
            # have all required info, proceed to do action
            selected_index = self.position_index[self.info_color + self.info_pre * len(self.colors)][self.info_num]
#             self.hide()
            self.move_mouse(selected_index[0], selected_index[1])
            self.mode = ""
                
    
    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width / self.square_size) + 2):
                self.xs.append(x * self.square_size)
            for y in range(0, int(self.dimensions.height / self.square_size) + 2):
                self.ys.append(y * self.square_size)
        self.position_index = []
        # add first "color":
        self.position_index.append([])
        
    def draw(self):
        self.pre_redraw()
        self.img = ImageGrab.grab()  # .filter(ImageFilter.BLUR)
        self.draw_squares()
        self.finalize()
        self.unhide()
        
    def draw_squares(self):
        self.fill_xs_ys()
        # 
        
        text_background_buffer = int(self.square_size / 6)
        xs_size = len(self.xs)
        ys_size = len(self.ys)
        box_number = 0
        colors_index = 0
        font = ImageFont.truetype("arialbd.ttf", 15)
        draw = ImageDraw.Draw(self.img, 'RGBA')
        
        for ly in range(0, ys_size):
            if  ly + 1 < ys_size:
                for lx in range(0, xs_size):
                    if lx + 1 < xs_size:
                        txt = str(box_number)
                        tw, th = draw.textsize(txt, font)
                        text_x = int((self.xs[lx] + self.xs[lx + 1] - tw) / 2) + 1
                        text_y = int((self.ys[ly] + self.ys[ly + 1] - th) / 2) - 1
                        draw.rectangle([self.xs[lx] + text_background_buffer,
                                                       self.ys[ly] + text_background_buffer,
                                                       self.xs[lx + 1] - text_background_buffer,
                                                       self.ys[ly + 1] - text_background_buffer], fill=self.colors[colors_index], outline=False)
                        
                        draw.text((text_x + 1, text_y + 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x - 1, text_y + 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x + 1, text_y - 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x - 1, text_y - 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x, text_y), txt, (255, 255, 255), font=font)
                        # index the position
                        self.position_index[len(self.position_index) - 1].append((int((self.xs[lx] + self.xs[lx + 1]) / 2), int((self.ys[ly] + self.ys[ly + 1]) / 2)))
                        
                        # update for next iteration
                        box_number += 1
                        if box_number == 100:
                            # next color
                            box_number = 0
                            colors_index += 1
                            self.position_index.append([])
                            if colors_index == len(self.colors):
                                colors_index = 0
        del draw

class DouglasGrid(TkTransparent):
    
    def __init__(self, grid_size=None, square_size=None):
        TkTransparent.__init__(self, "douglasgrid", grid_size)
        self.square_size = square_size if square_size else 25
                
        self.draw()
        self.mainloop()
    
    def setup_XMLRPC_server(self):
        TkTransparent.setup_XMLRPC_server(self)
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")
    
    def xmlrpc_move_mouse(self, x, y):
        self.move_mouse(x* self.square_size + int(self.square_size / 2), y* self.square_size + int(self.square_size / 2))
    
    def draw(self):
        self.pre_redraw()
        self.draw_lines_and_numbers()
        self.unhide()
    
    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width / self.square_size) + 2):
                self.xs.append(x * self.square_size)
            for y in range(0, int(self.dimensions.height / self.square_size)):
                self.ys.append(y * self.square_size)
    
    def draw_lines_and_numbers(self):
        
        self.fill_xs_ys()
        
        text_background_buffer = int(self.square_size / 10)
        xs_size = len(self.xs)
        for lx in range(0, xs_size):
            fill = "black"
            if lx % 3:
                fill = "gray"
            self._canvas.create_line(self.xs[lx], 0, self.xs[lx], self.dimensions.height - self.dimensions.y, fill=fill)
            if lx + 1 < xs_size:
                self._canvas.create_rectangle(
                                              self.xs[lx] + text_background_buffer,
                                              0 + text_background_buffer,
                                              self.xs[lx + 1] - text_background_buffer,
                                              self.square_size - text_background_buffer, fill='Black')
                self._canvas.create_rectangle(self.xs[lx] + text_background_buffer,
                                              self.dimensions.height - self.square_size + text_background_buffer,
                                              self.xs[lx + 1] - text_background_buffer,
                                              self.dimensions.height - text_background_buffer, fill='Black')
                text_x = int((self.xs[lx] + self.xs[lx + 1]) / 2)
                self._canvas.create_text(
                    text_x,
                    int(self.square_size / 2),
                    text=str(lx), font="Arial 10 bold", fill='White')
                self._canvas.create_text(
                        text_x,
                        self.dimensions.height - int(self.square_size / 2),
                        text=str(lx), font="Arial 10 bold", fill='White')
            
        ys_size = len(self.ys)
        for ly in range(0, ys_size):
            fill = "black"
            if ly % 3:
                fill = "gray"
            self._canvas.create_line(0, self.ys[ly], self.dimensions.width - self.dimensions.x, self.ys[ly], fill=fill)
            if ly + 1 < ys_size and ly != 0:
                self._canvas.create_rectangle(
                                              0 + text_background_buffer,
                                              self.ys[ly] + text_background_buffer,
                                              self.square_size - text_background_buffer,
                                              self.ys[ly + 1] - text_background_buffer, fill='Black')
                self._canvas.create_rectangle(
                                              self.dimensions.width - self.square_size + text_background_buffer,
                                              self.ys[ly] + text_background_buffer,
                                              self.dimensions.width - text_background_buffer,
                                              self.ys[ly + 1] - text_background_buffer, fill='Black')
                text_y = int((self.ys[ly] + self.ys[ly + 1]) / 2)
                self._canvas.create_text(
                    int(self.square_size / 2),
                    text_y,
                    text=str(ly), font="Arial 10 bold", fill='White')
                self._canvas.create_text(
                    self.dimensions.width - int(self.square_size / 2),
                    text_y,
                    text=str(ly), font="Arial 10 bold", fill='White')


        


    
def main(argv):
    help_message = 'mouse.py -m <mode>\nr\trainbow grid\nd\tdouglas grid'
    try:
        opts, args = getopt.getopt(argv, "hm:")
    except getopt.GetoptError:
        print help_message
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_message
            sys.exit()
        elif opt == '-m':
            if arg=="r":
                rg=RainbowGrid()
            elif arg == 'd':
                dg = DouglasGrid()  # grid_size=Dimensions(400, 300, 0, 0)  
            

if __name__ == '__main__':
    main(sys.argv[1:])
