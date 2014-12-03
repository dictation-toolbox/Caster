from __future__ import division

import multiprocessing
import os
import re 
import signal
import sys
import threading
import time

from PIL import ImageGrab, ImageTk, ImageDraw, ImageFont
import win32api

import Tkinter as tk
from asynch.bottleserver import BottleServer


try:
    from lib import utilities
except ImportError:
    BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
    sys.path.append(BASE_PATH)
    from lib import utilities

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
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.bind("<Key>", self.key)
        # self.mainloop()#do this in the child classes
    
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
        
    def on_exit(self):
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
        
    def move_mouse(self, mx, my):
        win32api.SetCursorPos((mx, my))
    
class LegionGrid(TkTransparent):
    class LServer(BottleServer):
        def __init__(self):
            ''''''
            
            self.most_recent_scan=None
            BottleServer.__init__(self, 1340)
        
        def process_requests(self):
            '''takes most recent scan result and makes it ready to be read by grid app, then discards everything'''
#             with self.lock: 
                
            
    
    def __init__(self, grid_size=None):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "legiongrid", grid_size)
        self.attributes("-alpha", 0.5)
        self.server = self.LServer()
        '''mode information:
        r  = refresh
        
        any other sequence should activate null-mode
        '''
        self.mode = ""  # null-mode
        self.digits = ""
        self.allowed_characters = r"[cnx0-9]"
        self.mainloop()

    def draw(self):
        self.pre_redraw()
        # drawing code here
        self.unhide()
        
    def draw_squares(self):
        ''''''

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
        '''mode information:
        p  = the next input will be an int representing pre-color information (which red do I want? the first, second? etc.)
        c  = the next input will be an int representing the selected color (1-"red", 5-"blue", etc.)
        n  = the next input will be 2 ints representing a number between 0-99
        xx = exit program
        r  = refresh
        
        any other sequence should activate null-mode
        '''
        self.mode = ""  # null-mode
        self.digits = ""
        self.allowed_characters = r"[pcnxr0-9]"
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
    
    def key(self, e):
        if re.search(self.allowed_characters, e.char):
            if e.char == 'x':
                if self.mode == "x":
                    self.on_exit()
                self.mode = "x"
            elif e.char == 'r':
                self.refresh()
            elif e.char == 'p':
                self.mode = "p"
                self.digits = ""
            elif e.char == 'c':
                self.mode = "c"
                self.digits = ""
            elif e.char == 'n':
                self.mode = "n"
                self.digits = ""
            else:
                self.digits += e.char
                if len(self.digits) == 2:
                    self.process()
    
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
        # drawing code here
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
        '''square_size is an integer'''
        TkTransparent.__init__(self, "douglasgrid", grid_size)
        self.square_size = square_size if square_size else 25
        
        '''mode information:
        b  = separator for X and Y grid number values
        xx = exit program
        
        any other sequence should activate null-mode
        '''
        self.mode = "y"  # null-mode
        self.digits = ""
        self.allowed_characters = r"[bx0-9]"
        self.y_coord = None
        
        self.draw()
        self.mainloop()
    
    def key(self, e):
        if re.search(self.allowed_characters, e.char):
            if e.char == 'b':
                self.mode = "x"
            elif e.char == 'x':
                if self.mode == "e":
                    self.on_exit()
                self.mode = "e"
            else:
                if self.mode == "e":
                    self.mode = "y"
                self.digits += e.char
                if len(self.digits) == 2:
                    self.process()
                    self.digits = ""
    
    def process(self):
        ''''''
        if self.mode == "y":
            self.y_coord = int(self.digits) * self.square_size + int(self.square_size / 2)
        elif self.mode == "x":
            x_coord = int(self.digits) * self.square_size + int(self.square_size / 2)
            self.move_mouse(x_coord, self.y_coord)
            self.mode = "y"
    
    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width / self.square_size) + 2):
                self.xs.append(x * self.square_size)
            for y in range(0, int(self.dimensions.height / self.square_size)):
                self.ys.append(y * self.square_size)
        
    def draw(self):
        self.pre_redraw()
        # drawing code here
        self.draw_lines_and_numbers()
        
        
        self.unhide()

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


        

def run():
    dg = DouglasGrid(grid_size=Dimensions(400, 300, 0, 0))  # grid_size=Dimensions(400, 300, 0, 0)
    

if __name__ == '__main__':
    p = multiprocessing.Process(target=run)
    p.start()
#     p.join(300)
#  
#     if p.is_alive():
#         p.terminate()
#         p.join()
#     utilities.run_in_separate_thread(run)
