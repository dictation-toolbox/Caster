from __future__ import division

from SimpleXMLRPCServer import SimpleXMLRPCServer

import getopt
import signal
import sys, os
from threading import Timer
import time

import win32api

import Tkinter as tk

from dragonfly import monitors

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings, utilities
    from castervoice.lib.dfplus.communication import Communicator

try:
    from PIL import ImageGrab, ImageTk, ImageDraw, ImageFont
except ImportError:
    utilities.availability_message("Douglas Grid / Rainbow Grid", "PIL")


def wait_for_death(title, timeout=5):
    t = 0.0
    inc = 0.1
    while t < timeout:
        if not utilities.window_exists(None, title):
            break
        t += inc
        time.sleep(inc)
    if t >= timeout:
        print("wait_for_death()" + " timed out (" + title + ")")


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
        return len(self.xs) > 0 or len(self.ys) > 0

    def get_dimensions_fullscreen(self):
        return Dimensions(self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0)

    def get_dimensions_string(self):
        return "%dx%d+%d+%d" % (self.dimensions.width, self.dimensions.height,
                                self.dimensions.x, self.dimensions.y)

    def __init__(self, name, dimensions=None, canvas=True):
        tk.Tk.__init__(self, baseName="")
        self.setup_xmlrpc_server()
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
        if canvas:
            self._canvas = tk.Canvas(
                master=self,
                width=dimensions.width,
                height=dimensions.height,
                bg='white',
                bd=-2)
            self._canvas.pack()
        self.protocol("WM_DELETE_WINDOW", self.xmlrpc_kill)

        #        self.bind("<Key>", self.key)
        # self.mainloop()#do this in the child classes
        def start_server():
            while not self.server_quit:
                self.server._handle_request_noblock()

        Timer(1, start_server).start()

    def setup_xmlrpc_server(self):
        self.server_quit = 0
        comm = Communicator()
        self.server = SimpleXMLRPCServer(
            (Communicator.LOCALHOST, comm.com_registry["grids"]), allow_none=True)
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

    @staticmethod
    def move_mouse(mx, my):
        win32api.SetCursorPos((mx, my))


class RainbowGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None, square_alpha=None):
        '''square_size is an integer'''
        TkTransparent.__init__(self, settings.RAINBOW_TITLE, grid_size)
        self.attributes("-alpha", 0.5)
        self.square_size = square_size if square_size else 37
        self.square_alpha = square_alpha if square_alpha else 125
        self.colors = [
            (255, 0, 0, self.square_alpha),  # red
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
        self._canvas.create_image(
            self.dimensions.width/2, self.dimensions.height/2, image=self.imgtk)

    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")

    def xmlrpc_move_mouse(self, pre, color, num):
        if pre > 0:
            pre -= 1
        selected_index = self.position_index[color + pre*len(self.colors)][num]
        self.move_mouse(selected_index[0] + self.dimensions.x,
                        selected_index[1] + self.dimensions.y)

    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width/self.square_size) + 2):
                self.xs.append(x*self.square_size)
            for y in range(0, int(self.dimensions.height/self.square_size) + 2):
                self.ys.append(y*self.square_size)
        self.position_index = []
        # add first "color":
        self.position_index.append([])

    def draw(self):
        self.pre_redraw()
        self.img = ImageGrab.grab([
            self.dimensions.x, self.dimensions.y,
            self.dimensions.x + self.dimensions.width,
            self.dimensions.y + self.dimensions.height
        ])  # .filter(ImageFilter.BLUR)
        self.draw_squares()
        self.finalize()
        self.unhide()

    def draw_squares(self):
        self.fill_xs_ys()
        #

        text_background_buffer = int(self.square_size/6)
        xs_size = len(self.xs)
        ys_size = len(self.ys)
        box_number = 0
        colors_index = 0
        font = ImageFont.truetype("arialbd.ttf", 15)
        draw = ImageDraw.Draw(self.img, 'RGBA')

        for ly in range(0, ys_size - 1):
            for lx in range(0, xs_size - 1):
                txt = str(box_number)
                tw, th = draw.textsize(txt, font)
                text_x = int((self.xs[lx] + self.xs[lx + 1] - tw)/2) + 1
                text_y = int((self.ys[ly] + self.ys[ly + 1] - th)/2) - 1
                draw.rectangle(
                    [
                        self.xs[lx] + text_background_buffer,
                        self.ys[ly] + text_background_buffer,
                        self.xs[lx + 1] - text_background_buffer,
                        self.ys[ly + 1] - text_background_buffer
                    ],
                    fill=self.colors[colors_index],
                    outline=False)

                draw.text((text_x + 1, text_y + 1), txt, (0, 0, 0), font=font)
                draw.text((text_x - 1, text_y + 1), txt, (0, 0, 0), font=font)
                draw.text((text_x + 1, text_y - 1), txt, (0, 0, 0), font=font)
                draw.text((text_x - 1, text_y - 1), txt, (0, 0, 0), font=font)
                draw.text((text_x, text_y), txt, (255, 255, 255), font=font)
                # index the position
                self.position_index[len(self.position_index) - 1].append(
                    (int((self.xs[lx] + self.xs[lx + 1])/2),
                     int((self.ys[ly] + self.ys[ly + 1])/2)))

                # update for next iteration
                box_number += 1
                if box_number == 100:
                    # next color
                    box_number = 0
                    colors_index += 1
                    colors_index %= len(self.colors)  # cycle colors
                    self.position_index.append([])

        del draw


class DouglasGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=None):
        TkTransparent.__init__(self, settings.DOUGLAS_TITLE, grid_size)
        self.square_size = square_size if square_size else 25

        self.draw()
        self.mainloop()

    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")

    def xmlrpc_move_mouse(self, x, y):
        DouglasGrid.move_mouse(
            x*self.square_size + int(self.square_size/2) + self.dimensions.x,
            y*self.square_size + int(self.square_size/2) + self.dimensions.y)

    def draw(self):
        self.pre_redraw()
        self.draw_lines_and_numbers()
        self.unhide()

    def fill_xs_ys(self):
        # only figure out the coordinates of the lines once
        if not self.xs_ys_filled():
            for x in range(0, int(self.dimensions.width/self.square_size) + 2):
                self.xs.append(x*self.square_size)
            for y in range(0, int(self.dimensions.height/self.square_size)):
                self.ys.append(y*self.square_size)

    def draw_lines_and_numbers(self):

        self.fill_xs_ys()

        text_background_buffer = int(self.square_size/10)
        xs_size = len(self.xs)
        for lx in range(0, xs_size):
            fill = "black"
            if lx % 3:
                fill = "gray"
            self._canvas.create_line(
                self.xs[lx], 0, self.xs[lx], self.dimensions.height, fill=fill)
            if lx + 1 < xs_size:
                self._canvas.create_rectangle(
                    self.xs[lx] + text_background_buffer,
                    0 + text_background_buffer,
                    self.xs[lx + 1] - text_background_buffer,
                    self.square_size - text_background_buffer,
                    fill='Black')
                self._canvas.create_rectangle(
                    self.xs[lx] + text_background_buffer,
                    self.dimensions.height - self.square_size + text_background_buffer,
                    self.xs[lx + 1] - text_background_buffer,
                    self.dimensions.height - text_background_buffer,
                    fill='Black')
                text_x = int((self.xs[lx] + self.xs[lx + 1])/2)
                self._canvas.create_text(
                    text_x,
                    int(self.square_size/2),
                    text=str(lx),
                    font="Arial 10 bold",
                    fill='White')
                self._canvas.create_text(
                    text_x,
                    self.dimensions.height - int(self.square_size/2),
                    text=str(lx),
                    font="Arial 10 bold",
                    fill='White')

        ys_size = len(self.ys)
        for ly in range(0, ys_size):
            fill = "black"
            if ly % 3:
                fill = "gray"
            self._canvas.create_line(
                0, self.ys[ly], self.dimensions.width, self.ys[ly], fill=fill)
            if ly + 1 < ys_size and ly != 0:
                self._canvas.create_rectangle(
                    0 + text_background_buffer,
                    self.ys[ly] + text_background_buffer,
                    self.square_size - text_background_buffer,
                    self.ys[ly + 1] - text_background_buffer,
                    fill='Black')
                self._canvas.create_rectangle(
                    self.dimensions.width - self.square_size + text_background_buffer,
                    self.ys[ly] + text_background_buffer,
                    self.dimensions.width - text_background_buffer,
                    self.ys[ly + 1] - text_background_buffer,
                    fill='Black')
                text_y = int((self.ys[ly] + self.ys[ly + 1])/2)
                self._canvas.create_text(
                    int(self.square_size/2),
                    text_y,
                    text=str(ly),
                    font="Arial 10 bold",
                    fill='White')
                self._canvas.create_text(
                    self.dimensions.width - int(self.square_size/2),
                    text_y,
                    text=str(ly),
                    font="Arial 10 bold",
                    fill='White')


def main(argv):
    help_message = 'Usage: grids.py -g <GRID_TYPE> [-m <MONITOR>]\n where <GRID_TYPE> is one of:\n  r\trainbow grid\n  d\tdouglas grid'
    try:
        opts, args = getopt.getopt(argv, "hg:m:")
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    g = None
    m = 1
    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt == '-g':
            if arg == "r":
                g = RainbowGrid
            elif arg == 'd':
                g = DouglasGrid
        elif opt == '-m':
            m = arg
    if g is None:
        raise ValueError("Grid mode not specified.")
    r = monitors[int(m) - 1].rectangle
    grid_size = Dimensions(int(r.dx), int(r.dy), int(r.x), int(r.y))
    g(grid_size=grid_size)


if __name__ == '__main__':
    main(sys.argv[1:])
