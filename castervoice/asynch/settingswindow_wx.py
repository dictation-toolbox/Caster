from __future__ import print_function
import numbers
import os
import six
import sys
import threading

if six.PY2:
    from SimpleXMLRPCServer import SimpleXMLRPCServer   # pylint: disable=import-error
else:
    from xmlrpc.server import SimpleXMLRPCServer  # pylint: disable=no-name-in-module

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import printer
    from castervoice.lib import settings
    from castervoice.lib.merge.communication import Communicator

try:
    from wx import (Notebook, NB_MULTILINE, Menu, ID_EXIT, EVT_MENU, MenuBar, BoxSizer,
                    VERTICAL, HORIZONTAL, StaticText, RIGHT, EXPAND, LEFT, TOP, TextCtrl,
                    Panel, App, Frame, CheckBox, EVT_CLOSE, ID_ANY)
    from wx.lib.scrolledpanel import ScrolledPanel
    import wx.lib.newevent
except ImportError:
    # TODO: Because the console is invisible, this should be handled by some sort of
    # GUI element like a message box.
    print(
        """
        An error was encountered while trying to import the `wxPython` module. Please
        use `python -m pip install --upgrade wxPython` to install the latest version.
        """ + settings.GENERIC_HELP_MESSAGE, file=sys.stderr)
    raise


settings.initialize()
DICT_SETTING = 1
STRING_SETTING = 2
STRING_LIST_SETTING = 4
NUMBER_LIST_SETTING = 8
NUMBER_SETTING = 16
BOOLEAN_SETTING = 32

OnKillEvent, EVT_ON_KILL = wx.lib.newevent.NewEvent()
OnCompleteEvent, EVT_ON_COMPLETE = wx.lib.newevent.NewEvent()
SETTINGS_FRAME = None


class Field:
    def __init__(self, widget, original, text_type=None):
        self.children = []
        self.widget = widget
        self.original = original
        self.text_type = text_type

    def add_child(self, field):
        self.children.append(field)


class SettingsFrame(Frame):
    def __init__(self, parent, title, server):
        Frame.__init__(self, parent, title=title, size=(500, 400))
        global SETTINGS_FRAME
        SETTINGS_FRAME = self
        self.server = server
        self.setup_xmlrpc_server()
        self.completed = False
        self.notebook = Notebook(self, style=NB_MULTILINE)
        file_menu = Menu()
        self.next_page = file_menu.Append(ID_ANY, '&Next page\tRAWCTRL+TAB', 'Next page')
        self.prev_page = file_menu.Append(ID_ANY, '&Prev page\tRAWCTRL+SHIFT+TAB', 'Prev page')
        self.Bind(EVT_MENU, self.OnTab, self.next_page)
        self.Bind(EVT_MENU, self.OnTab, self.prev_page)
        exit_item = file_menu.Append(ID_EXIT, '&Exit...', 'Exit Settings Window')
        self.Bind(EVT_MENU, self.prepare_for_exit, exit_item)
        menu_bar = MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)
        self.fields = []
        for top in sorted(settings.SETTINGS.keys()):  # pylint: disable=no-member
            self.make_page(top)
        self.CenterOnScreen()
        self.Show()
        self.Bind(EVT_ON_KILL, self.OnKill)
        self.Bind(EVT_ON_COMPLETE, self.OnComplete)
        self.Bind(EVT_CLOSE, self.xmlrpc_kill)
        self.expiration = threading.Timer(300, self.xmlrpc_kill)
        self.expiration.start()

    def OnTab(self, event):
        the_id = event.GetId()
        curr = self.notebook.GetSelection()
        next = curr + 1 if the_id == self.next_page.GetId() else curr - 1
        page_count = self.notebook.GetPageCount()
        next = 0 if next == page_count else page_count - 1 if next < 0 else next
        self.notebook.ChangeSelection(next)

    def OnKill(self, event):
        self.expiration.cancel()
        self.server.shutdown()
        self.Destroy()

    def OnComplete(self, event):
        self.completed = True
        self.Hide()

    def prepare_for_exit(self, e):
        self.Hide()
        self.completed = True
        threading.Timer(10, self.xmlrpc_kill).start()

    def tree_to_dictionary(self, t=None):
        d = {}
        children = self.fields if t is None else t.children
        for field in children:
            value = None
            if isinstance(field.widget, TextCtrl):
                value = field.widget.GetValue()
                if field.text_type == STRING_LIST_SETTING:
                    d[field.original] = [
                        x for x in value.replace(", ", ",").split(",") if x
                    ]  # don't count empty strings
                elif field.text_type == NUMBER_LIST_SETTING:
                    temp_list = (
                        float(x) for x in value.replace(", ", ",").split(",") if x
                    )  # don't count empty strings
                    d[field.original] = [int(x) if x.is_integer() else x for x in temp_list]
                elif field.text_type == NUMBER_SETTING:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                    d[field.original] = float(value)
                else:
                    d[field.original] = value.replace("\\", "/")
            elif isinstance(field.widget, (Panel, ScrolledPanel)):
                d[field.original] = self.tree_to_dictionary(field)
            elif isinstance(field.widget, CheckBox):
                d[field.original] = field.widget.GetValue()
        return d

    def setup_xmlrpc_server(self):
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        self.server.register_function(self.xmlrpc_complete, "complete")
        self.server.register_function(self.xmlrpc_kill, "kill")
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def xmlrpc_kill(self, e=None):
        wx.PostEvent(SETTINGS_FRAME, OnKillEvent())

    def xmlrpc_get_message(self):
        if self.completed:
            threading.Timer(1, self.xmlrpc_kill).start()
            return self.tree_to_dictionary()
        else:
            return None

    def xmlrpc_complete(self):
        wx.PostEvent(SETTINGS_FRAME, OnCompleteEvent())

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
        for label in sorted(settings.SETTINGS[field.original].keys()):
            hbox = BoxSizer(HORIZONTAL)
            value = settings.SETTINGS[field.original][label]
            lbl = StaticText(page, label=label)
            hbox.Add(lbl, flag=RIGHT, border=8)
            subfield = Field(None, label)
            item = self.field_from_value(page, value, subfield)
            field.add_child(subfield)
            if item is not None:
                hbox.Add(item, proportion=1)
            vbox.Add(hbox, flag=EXPAND | LEFT | RIGHT | TOP, border=5)
            vbox.Add((-1, 5))

    def field_from_value(self, window, value, field):
        item = None
        if isinstance(value, six.string_types):
            item = TextCtrl(window, value=value)
            field.text_type = STRING_SETTING
        elif isinstance(value, list):
            if isinstance(value[0], six.string_types):
                item = TextCtrl(window, value=", ".join(value))
                field.text_type = STRING_LIST_SETTING
            elif isinstance(value[0], numbers.Real):
                item = TextCtrl(window, value=", ".join((str(x) for x in value)))
                field.text_type = NUMBER_LIST_SETTING
        elif isinstance(value, bool):
            item = CheckBox(window, -1, '', (120, 75))
            item.SetValue(value)
        elif isinstance(value, numbers.Real):
            item = TextCtrl(window, value=str(value))
            field.text_type = NUMBER_SETTING
        elif isinstance(value, dict):
            subpage = Panel(window)
            vbox = BoxSizer(VERTICAL)
            for lbl in sorted(value.keys()):
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
        else:
            # This is left for bug reporting purposes.
            printer.out(("{} from the field {} was not assigned to " +
                         "{} because type {} wasn't properly handled.").
                        format(value, field, window, type(value)))
        field.widget = item
        return item


def main():
    server_address = (Communicator.LOCALHOST, Communicator().com_registry["hmc"])
    # Enabled by default logging causes RPC to malfunction when the GUI runs on
    # pythonw.  Explicitly disable logging for the XML server.
    server = SimpleXMLRPCServer(server_address, logRequests=False, allow_none=True)
    app = App(False)
    SettingsFrame(None,
                  settings.SETTINGS_WINDOW_TITLE + settings.SOFTWARE_VERSION_NUMBER,
                  server)
    app.MainLoop()


if __name__ == '__main__':
    main()
