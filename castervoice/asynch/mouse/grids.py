from __future__ import division

import getopt
import os
import signal
import six
import sys
import threading as th
import time
from dragonfly import monitors
if six.PY2:
    from SimpleXMLRPCServer import SimpleXMLRPCServer  # pylint: disable=import-error
    import Tkinter as tk
else:
    from xmlrpc.server import SimpleXMLRPCServer  # pylint: disable=no-name-in-module
    import tkinter as tk
try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings, utilities
    from castervoice.lib.actions import Mouse
    from castervoice.lib.merge.communication import Communicator
    settings.initialize()
try:
    from PIL import ImageGrab, ImageTk, ImageDraw, ImageFont
except ImportError:
    utilities.availability_message("Douglas Grid / Rainbow Grid / Sudoku Grid", "PIL")


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
            self.server.serve_forever()

        th.Timer(1, start_server).start()

    def setup_xmlrpc_server(self):
        comm = Communicator()
        self.server = SimpleXMLRPCServer(
            (Communicator.LOCALHOST, comm.com_registry["grids"]),
            logRequests=False, allow_none=True)
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
        self.server.shutdown()
        self.destroy()
        os.kill(os.getpid(), signal.SIGTERM)

    @staticmethod
    def move_mouse(mx, my):
        Mouse("[{}, {}]".format(mx, my)).execute()


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


'''
Divide screen into grid of 3 x 3 squares and assign each one a number.
    The user can specify a square number and further refine the selection
    with one of the numbers from 1 to 9.
'''
class SudokuGrid(TkTransparent):
    def __init__(self, grid_size=None, square_size=32):
        TkTransparent.__init__(self, settings.SUDOKU_TITLE, grid_size)

        screen_w = self.dimensions.width
        screen_h = self.dimensions.height

        self.square_width = square_size
        while (screen_w % self.square_width != 0):
            self.square_width -= 1

        self.square_height = square_size
        while (screen_h % self.square_height != 0):
            self.square_height -= 1

        self.width = int(screen_w / self.square_width)
        self.height = int(screen_h / self.square_height)
        self.num_squares = self.width * self.height
        self.up_w = int((self.width - 1) / 3 + 1) * 3
        self.up_h = int((self.height - 1) / 3 + 1) * 3
        self.down_w = (int(self.up_w / 3) - 1) * 3
        self.down_h = (int(self.up_h / 3) - 1) * 3

        # Put this in a try so we don't freeze if draw fails
        try:
            self.draw()
        finally:
            try:
                self.mainloop()
            except KeyboardInterrupt:
                self.server.shutdown()

    def click(self):
        Mouse("left:1").execute()

    # Set up the RPC server
    def setup_xmlrpc_server(self):
        TkTransparent.setup_xmlrpc_server(self)
        self.server.register_function(self.xmlrpc_move_mouse, "move_mouse")
        self.server.register_function(self.xmlrpc_get_mouse_pos, "get_mouse_pos")

    # RPC function to move the mouse using screen number and inner number
    # n1 - the screen number from 1 to m
    # n2 - inner number from 1 to 9
    def xmlrpc_move_mouse(self, n1, n2):
        x, y = self.get_mouse_pos(n1, n2)
        self.move_mouse(x + self.dimensions.x, y + self.dimensions.y)

    # RPC function to get the mouse position from screen number and inner number
    # n1 - the screen number from 1 to m
    # n2 - inner number from 1 to 9
    def xmlrpc_get_mouse_pos(self, n1, n2):
        return self.get_mouse_pos(n1, n2)

    # Draw the grid on screen
    def draw(self):
        self.pre_redraw()
        self.draw_lines_and_numbers()
        self.unhide()

    # Get the mouse position from screen number and enter number
    # n1 - the screen number from 1 to m
    # n2 - inner number from 1 to 9
    def get_mouse_pos(self, n1, n2):
        sq = self.num_to_square(n1)
        sq_refined = self.get_refined_square(sq, n2)
        return self.square_to_pos(self.fit_to_screen(sq_refined))

    # Modify the square based on the inner number
    # sq - square number
    # n2 - inner number from 1 to 9
    def get_refined_square(self, sq, n2):
        if n2 != 0 and n2 != 5:
            n2 -= 1

            # We use the rounded up width because this is the unadjusted square
            x = n2 % 3
            y = int(n2 / 3)

            sq += (x - 1) + (y - 1) * self.up_w

        return sq

    # Convert screen number to position on screen
    # n - the screen number from 1 to m
    def num_to_pos(self, n):
        # The number of squares is based on the rounded-up width and height
        num_squares = self.up_w * self.up_h

        # If the number is out of range, fix it
        if n < 1:
            n = 1
        elif n >= int(num_squares / 9):
            n = int(num_squares / 9)

        sq = self.num_to_square(n)

        return self.square_to_pos(self.fit_to_screen(sq))

    # Adjust the square number if current square is offscreen
    # sq - square number
    def fit_to_screen(self, sq):
        up_x = sq % self.up_w
        up_y = int(sq / self.up_w)

        # adjust square if offscreen
        if up_x >= self.width:
            up_x = self.width - 1
        if up_y >= self.height:
            up_y = self.height - 1

        return up_x + up_y * self.width

    # Convert a screen number to an internal square number
    # n - the screen number from 1 to m
    def num_to_square(self, n):
        # decrement screen number to make 0 to m-1
        n -= 1

        # Use the rounded up width because the center square may be off screen
        up_x = n % int(self.up_w / 3)
        up_y = int(n / (self.up_w / 3))

        sq = (up_x * 3 + 1) + ((up_y * 3 + 1) * self.up_w)

        return sq

    # Convert a square number to a screen position
    # sq - square number
    def square_to_pos(self, sq):
        x, y = self.square_to_xy(sq)
        return (int((x + 0.5) * self.square_width),
                int((y + 0.5) * self.square_height))

    # Convert square number to screen number
    # sq - square number
    def square_to_num(self, sq):
        x, y = self.square_to_xy(sq)

        n = int(x / 3) + int(y / 3) * int(self.up_w / 3)

        # increment for 1...
        return n + 1

    # Convert a square number to grid coordinates
    # sq - square number
    def square_to_xy(self, sq):
        x = sq % self.width
        y = int(sq / self.width)
        return x, y

    # Draw grid on background
    def draw_lines_and_numbers(self):
        canvas = self._canvas

        # Iterate over logical grid of squares
        for sq in range(self.num_squares):
            x, y = self.square_to_xy(sq)
            screen_x = x * self.square_width
            screen_y = y * self.square_height

            fill = "black"
            if sq % 3:
                fill = "gray"

            # draw vertical grid lines
            if x > 0 and sq <= self.width:
                canvas.create_line(
                    screen_x, 0, screen_x, self.dimensions.height, fill=fill)

            # draw horizontal grid lines
            if x == 0:
                canvas.create_line(
                    0, screen_y, self.dimensions.width, screen_y, fill=fill)

            # draw number
            if (x % 3 == 1 or x == self.width - 1) and (y % 3 == 1 or y == self.height - 1):
                n = self.square_to_num(sq)
                pos = self.num_to_pos(n)
                canvas.create_text(pos[0], pos[1], text=str(n),
                                   font="TkFixedFont 14", fill='Black')


# Main function
def main(argv):
    help_message = 'Usage: grids.py -g <GRID_TYPE> [-m <MONITOR>]\n where <GRID_TYPE> is one of:\n  r\trainbow grid\n  d\tdouglas grid\n  s\tsudoku grid'
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
            elif arg == 's':
                g = SudokuGrid
        elif opt == '-m':
            m = arg

    if g is None:
        raise ValueError("Grid mode not specified.")
    r = monitors[int(m) - 1].rectangle
    grid_size = Dimensions(int(r.dx), int(r.dy), int(r.x), int(r.y))
    g(grid_size=grid_size)


if __name__ == '__main__':
    main(sys.argv[1:])
