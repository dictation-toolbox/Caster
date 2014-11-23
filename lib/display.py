from __future__ import division

import math
import multiprocessing
import os
import signal
import threading
import time

from PIL import ImageGrab, ImageTk, ImageFilter, ImageDraw, ImageFont
import win32api
import win32con
import wx

import Tkinter as tk


class Dimensions:
    def __init__(self, w, h, x, y):
        self.width = w
        self.height = h
        self.x = x
        self.y = y

# class WxTransparent(wx.Frame):
#     def __init__(self, wtitle):
#         self.dimensions = self.get_dimensions_fullscreen()
#         self.clientBitmap=None
#         self.FONT_SIZE=20
#         self.columnWidth=30
#         
#         wx.Frame.__init__(self, None, title=wtitle, style=wx.BORDER_NONE | wx.STAY_ON_TOP)
#         
#         self.Bind(wx.EVT_PAINT, self.on_paint)
#         self.Bind(wx.EVT_KEY_UP, self.on_key_up)
#         self.Bind(wx.EVT_CLOSE, self.on_close)
#         self.Bind(wx.EVT_ACTIVATE, self.on_activate)
#         self.Bind(wx.EVT_MIDDLE_DCLICK, self.on_exit)
#         
#         self.SetBackgroundColour("White")
#         self.DrawGrid()
#         self.Show()
#     
#     def DrawGrid(self):
#         # Do Screen capture of desktop behind window client area
#         self.clientBitmap = wx.EmptyBitmap(self.dimensions.width, self.dimensions.height)
# 
#         memoryDc = wx.MemoryDC()
#         memoryDc.SelectObject(self.clientBitmap)
# 
# 
#         self.ClearBackground()
#         sourceDc = wx.ScreenDC()
#         memoryDc.Blit(0, 0, self.dimensions.width, self.dimensions.height, sourceDc, self.dimensions.x, self.dimensions.y)
# 
#         # Draw grid
# 
#         # Labels setup
#         memoryDc.SetTextForeground(wx.Colour(255, 255, 255))
#         memoryDc.SetTextBackground(wx.Colour(0, 0, 0))
#         memoryDc.SetBackgroundMode(wx.SOLID)
# 
#         # Columns
# #         columnx = self.LABEL_WIDTH
# #         gridWidth = 0
#         memoryDc.SetPen(wx.Pen ("#000000", 1))
# #         columnNum = 1
# #         if self.columnWidth == None:
# #               self.columnWidth = self.gridWidth / self.numColumns
# 
#         # Make sure label is not too big
#         fontSize = self.FONT_SIZE
#         memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#         extentx, extenty = memoryDc.GetTextExtent('99')
#         while extentx > self.columnWidth:
#             fontSize = fontSize - 1
#             memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#             extentx, extenty = memoryDc.GetTextExtent('99')
# 
#         # Print columns
#         '''
#         while gridWidth <= self.gridWidth:
#             # print line to the left
#             memoryDc.DrawLine(columnx, 0, columnx, self.clientHeight)
#             # print top label
#             memoryDc.DrawText(str(columnNum), columnx + 1, 1)
#             # print final label
#             memoryDc.DrawText(str(columnNum), columnx + 1, self.clientHeight - extenty)
#             columnx = columnx + self.columnWidth
#             gridWidth = gridWidth + self.columnWidth
#             columnNum = columnNum + 1
#         '''
#         # Right side border
# #         memoryDc.DrawLine(self.clientWidth - 1, 0, self.clientWidth - 1, self.clientHeight)
# # 
# #         # Rows
# #         rowy = self.LABEL_HEIGHT
# #         gridHeight = 0
# #         rowNum = 1
# # 
# #         if self.rowHeight == None:
# #             self.rowHeight = self.gridHeight / self.numRows
# # 
# #         # Make sure label is not too big
# #         fontSize = self.FONT_SIZE
# #         memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
# #         extentx, extenty = memoryDc.GetTextExtent('99')
# #         while extenty > self.rowHeight:
# #             fontSize = fontSize - 1
# #             memoryDc.SetFont(wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
# #             extentx, extenty = memoryDc.GetTextExtent('99')
# # 
# #         # print rows
# #         while gridHeight <= self.gridHeight:
# #             # Print line above
# #             memoryDc.DrawLine(0, rowy, self.clientWidth, rowy)
# #             # Print left label
# #             memoryDc.DrawText(str(rowNum), 1, rowy + 1)
# #             # Print right labal
# #             memoryDc.DrawText(str(rowNum), self.clientWidth - extentx, rowy + 1)
# #             rowy = rowy + self.rowHeight
# #             gridHeight = gridHeight + self.rowHeight
# #             rowNum = rowNum + 1
# # 
# #         # Bottom border
# #         memoryDc.DrawLine(0, self.clientHeight - 1, self.clientWidth, self.clientHeight - 1)
# # 
# #         # Draw dot at top left corner for position mode
# #         if self.positionMode:
# #             memoryDc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))
# #             memoryDc.DrawCircle(self.LABEL_WIDTH, self.LABEL_HEIGHT, 2)
# 
#         # All done
#         memoryDc.SelectObject(wx.NullBitmap)
#     
#     def reset_xs_ys(self):
#         self.xs = []
#         self.ys = []
#     
#     def hide(self, minimize=False):
#         if minimize:
#             self.Iconize()
#         else:
#             self.Show(False)
#     
#     def pre_redraw(self):
#         '''gets the window ready to be redrawn'''
#         self.deiconify()
#         self._canvas.delete("all")
#         
#     
#     def unhide(self):
#         ''''''
#         
#         
#     def on_exit(self, e=None):
# #         os.kill(os.getpid(), signal.SIGTERM)
#         self.Close(True)
#         
#     def xs_ys_filled(self):
#         return len(self.xs) > 0 or len(self.ys) > 0;
#     
#     def get_dimensions_fullscreen(self):
#         return Dimensions(win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1), 0, 0)
# 
#     
#     
#     def moveMouse(self):
#         win32api.SetCursorPos((self.nextCursorX, self.nextCursorY))
# 
#     def clickMouse(self):
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
#         self.stickyShow()
# 
#     def doubleClickMouse(self):
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.nextCursorX, self.nextCursorY, 0, 0)
#         self.stickyShow()
# 
#     def rightClickMouse(self):
#         win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.nextCursorX, self.nextCursorY, 0, 0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.nextCursorX, self.nextCursorY, 0, 0)
#         self.stickyShow()
#     
#     # dp stuff
#     def on_paint(self, e):
#         dc = wx.BufferedPaintDC(self, self.clientBitmap)
#         return
#     def on_key_up(self, e):
#         ''''''
#     def on_close(self, e):
#         e.Skip()
#     def on_activate(self, e):  # prevent beep
#         self.SetFocus()
#         e.Skip()

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
        
    



class RainbowGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, square_alpha=None):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "rainbowgrid", grid_size)
        self.attributes("-alpha", 1.0)
        self.square_size = square_size if square_size else 37
        self.square_alpha = square_alpha if square_alpha else 60
        self.colors = [(255, 0, 0, self.square_alpha),  # red
                       (187, 122, 0, self.square_alpha),  # orange 255, 165, 0
                       (255, 255, 0, self.square_alpha),  # yellow
                       (0, 128, 0, self.square_alpha),  # green
                       (0, 0, 125, self.square_alpha),  # blue
                       (128, 0, 128, self.square_alpha)  # purple
                       ]
        self.draw()
        self.mainloop()
        
    def finalize(self):
        self.imgtk = ImageTk.PhotoImage(self.img)
        self._canvas.create_image(self.dimensions.width / 2, self.dimensions.height / 2, image=self.imgtk)
    
    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width / self.square_size) + 2):
                self.xs.append(x * self.square_size)
            for y in range(0, int(self.dimensions.height / self.square_size) + 2):
                self.ys.append(y * self.square_size)
        
    def draw(self):
        self.pre_redraw()
        # drawing code here
        self.img = ImageGrab.grab()  # .filter(ImageFilter.BLUR)
        self.draw_squares()
        self.finalize()
        self.unhide()
        
    def draw_squares(self):
        self.fill_xs_ys()
        text_background_buffer = int(self.square_size / 10)
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
                        text_x = int((self.xs[lx] + self.xs[lx + 1] - tw) / 2)+1
                        text_y = int((self.ys[ly] + self.ys[ly + 1] - th) / 2)-1
                        draw.rectangle([self.xs[lx] + text_background_buffer,
                                                       self.ys[ly] + text_background_buffer,
                                                       self.xs[lx + 1] - text_background_buffer,
                                                       self.ys[ly + 1] - text_background_buffer], fill=self.colors[colors_index], outline=False)
                        
                        draw.text((text_x + 1, text_y + 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x - 1, text_y + 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x + 1, text_y - 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x - 1, text_y - 1), txt, (0, 0, 0), font=font)
                        draw.text((text_x, text_y), txt, (255, 255, 255), font=font)
                        box_number += 1
                        if box_number == 100:
                            box_number = 0
                            colors_index += 1
                            if colors_index == len(self.colors):
                                colors_index = 0
        del draw

class DouglasGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None):
        '''square_size is an integer'''
        TkTransparent.__init__(self, "douglasgrid", grid_size)
        self.square_size = square_size if square_size else 30
        self.draw()
        self.mainloop()
    
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
    dg = RainbowGrid()
    

# t = threading.Thread(target=run)
# t.start()

if __name__ == '__main__':
    # Start bar as a process
    p = multiprocessing.Process(target=run)
    p.start()

    # Wait for 5 minutes or until process finishes
    p.join(300)

    # If thread is still active
    if p.is_alive():
        p.terminate()
        p.join()
