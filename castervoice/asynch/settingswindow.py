from __future__ import print_function

import os
import signal
import sys
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Timer

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings
    from castervoice.lib.dfplus.communication import Communicator

try:
    from wx import (Notebook, NB_MULTILINE, Menu, ID_EXIT, EVT_MENU, MenuBar, BoxSizer,
                    VERTICAL, HORIZONTAL, StaticText, RIGHT, EXPAND, LEFT, TOP, TextCtrl,
                    Panel, App, Frame, CheckBox, EVT_CLOSE)

    from wx.lib.scrolledpanel import ScrolledPanel
except ImportError:
    # TODO: Because the console is invisible, this should be handled by some sort of
    # GUI element like a message box.
    print(
        """
An error was encountered while trying to import the `wxPython` module. Please
use `pip install --upgrade wxPython` to install the latest version.
""" + settings.GENERIC_HELP_MESSAGE,
        file=sys.stderr)
    raise

DICT_SETTING = 1
STRING_SETTING = 2
STRINGLIST_SETTING = 4
INTEGERLIST_SETTING = 8
INTEGER_SETTING = 16
BOOLEAN_SETTING = 32


class Field:
    def __init__(self, wx_field, original, text_type=None):
        self.children = []
        self.wx_field = wx_field
        self.original = original
        self.text_type = text_type

    def add_child(self, field):
        self.children.append(field)


class SettingsFrame(Frame):
    def __init__(self, parent, title):
        Frame.__init__(self, parent, title=title, size=(500, 400))
        self.setup_xmlrpc_server()
        self.completed = False

        # Create the notebook
        self.notebook = Notebook(self, style=NB_MULTILINE)
        # Setting up the menu
        file_menu = Menu()
        exit_item = file_menu.Append(ID_EXIT, '&Exit...', 'Exit Settings Window')
        self.Bind(EVT_MENU, self.prepare_for_exit, exit_item)
        menu_bar = MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

        alpha = settings.SETTINGS.keys()
        alpha.sort()
        self.fields = []
        for top in alpha:
            self.make_page(top)

        self.CenterOnScreen()
        self.Show()

        self.Bind(EVT_CLOSE, self.xmlrpc_kill)

        def start_server():
            while not self.server_quit:
                self.server.handle_request()

        Timer(0.5, start_server).start()
        Timer(300, self.xmlrpc_kill).start()

    def prepare_for_exit(self, e):
        self.Hide()
        self.completed = True
        threading.Timer(10, self.xmlrpc_kill).start()

    def tree_to_dictionary(self, t=None):
        d = {}

        children = None
        if t is None: children = self.fields
        else: children = t.children

        for field in children:
            value = None
            if isinstance(field.wx_field, TextCtrl):
                value = field.wx_field.GetValue()
                if field.text_type == STRINGLIST_SETTING:
                    d[field.original] = [
                        x for x in value.replace(", ", ",").split(",") if x
                    ]  # don't count empty strings
                elif field.text_type == INTEGERLIST_SETTING:
                    d[field.original] = [
                        int(x) for x in value.replace(", ", ",").split(",") if x
                    ]  # don't count empty strings
                elif field.text_type == INTEGER_SETTING:
                    d[field.original] = int(value)
                else:
                    d[field.original] = value.replace("\\", "/")
            elif isinstance(field.wx_field, (Panel, ScrolledPanel)):
                d[field.original] = self.tree_to_dictionary(field)
            elif isinstance(field.wx_field, CheckBox):
                d[field.original] = field.wx_field.GetValue()

        return d

    def setup_xmlrpc_server(self):
        self.server_quit = 0
        comm = Communicator()
        self.server = SimpleXMLRPCServer(
            (Communicator.LOCALHOST, comm.com_registry["hmc"]), allow_none=True)
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        self.server.register_function(self.xmlrpc_complete, "complete")
        self.server.register_function(self.xmlrpc_kill, "kill")

    def xmlrpc_kill(self, e=None):
        self.server_quit = 1
        os.kill(os.getpid(), signal.SIGTERM)
        self.Close()

    def xmlrpc_get_message(self):
        if self.completed:
            Timer(1, self.xmlrpc_kill).start()
            return self.tree_to_dictionary()
        else:
            return None

    def xmlrpc_complete(self):
        self.completed = True
        self.Hide()

    def make_page(self, title):
        page = ScrolledPanel(parent=self.notebook, id=-1)
        vbox = BoxSizer(VERTICAL)
        field = Field(page, title)
        self.get_fields(page, vbox, field)
        self.fields.append(field)

        page.SetupScrolling()
        page.SetSizer(vbox)
        self.notebook.AddPage(page, title)

    def get_fields(self, page, vbox, field):
        keys = settings.SETTINGS[field.original].keys()
        keys.sort()

        for label in keys:
            hbox = BoxSizer(HORIZONTAL)
            value = settings.SETTINGS[field.original][label]

            lbl = StaticText(page, label=label)
            hbox.Add(lbl, flag=RIGHT, border=8)

            subfield = Field(None, label)
            item = self.field_from_value(page, value, subfield)
            field.add_child(subfield)

            if item != None:
                hbox.Add(item, proportion=1)
            vbox.Add(hbox, flag=EXPAND | LEFT | RIGHT | TOP, border=5)
            vbox.Add((-1, 5))

    def field_from_value(self, window, value, field):
        item = None
        if isinstance(value, basestring):
            item = TextCtrl(window, value=value)
            field.text_type = STRING_SETTING
        elif isinstance(value, list):
            if isinstance(value[0], basestring):
                item = TextCtrl(window, value=", ".join(value))
                field.text_type = STRINGLIST_SETTING
            elif isinstance(value[0], int):
                item = TextCtrl(window, value=", ".join((str(x) for x in value)))
                field.text_type = INTEGERLIST_SETTING
        elif isinstance(value, bool):
            item = CheckBox(window, -1, '', (120, 75))
            item.SetValue(value)
        elif isinstance(value, int):
            item = TextCtrl(window, value=str(value))
            field.text_type = INTEGER_SETTING
        elif isinstance(value, dict):
            subpage = Panel(window)
            vbox = BoxSizer(VERTICAL)
            alpha = value.keys()
            alpha.sort()
            for lbl in alpha:
                hbox = BoxSizer(HORIZONTAL)
                value2 = value[lbl]
                label = StaticText(subpage, label=lbl)
                hbox.Add(label, flag=RIGHT, border=8)
                subfield = Field(None, lbl)
                item = self.field_from_value(subpage, value2, subfield)
                field.add_child(subfield)
                if item is not None:
                    hbox.Add(item, proportion=1)
                vbox.Add(hbox, flag=EXPAND | LEFT | RIGHT | TOP, border=5)
                vbox.Add((-1, 5))
            subpage.SetSizer(vbox)
            subpage.Show()
            item = subpage
        field.wx_field = item
        return item


# if __name__ == '__main__':
app = App(False)
frame = SettingsFrame(None,
                      settings.SETTINGS_WINDOW_TITLE + settings.SOFTWARE_VERSION_NUMBER)
app.MainLoop()
