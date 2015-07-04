import os
import sys

import wx
from wx.lib.scrolledpanel import ScrolledPanel


try: # Style C -- may be imported into Caster, or externally
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem/"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    import SimpleXMLRPCServer
    from SimpleXMLRPCServer import *
    from caster.lib import settings
    from caster.lib.dfplus.communication import Communicator

class SettingsFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        self.CenterOnScreen()
        
        # Create the notebook 
        self.notebook = wx.Notebook(self, style=wx.NB_MULTILINE)

        # Setting up the menu
        file_menu = wx.Menu()
        save_item = file_menu.Append(wx.ID_SAVE, '&Save...', 'Save Settings')
        exit_item = file_menu.Append(wx.ID_EXIT, '&Exit...', 'Exit Settings Window')
#         self.Bind(wx.EVT_MENU, self.OnOpen, menu_item)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)
        
        alpha = settings.SETTINGS.keys()
        alpha.sort()
        for top in alpha:
            self.make_page(top)
        
        self.Show()
        
    def make_page(self, title): 
        page = ScrolledPanel(parent = self.notebook, id = -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.get_fields(page, vbox, title)
        
        page.SetupScrolling()
        page.SetSizer(vbox)
        self.notebook.AddPage(page, title)
    
    def get_fields(self, page, vbox, title):
        keys = settings.SETTINGS[title].keys()
        keys.sort()
        
        for label in keys:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            value = settings.SETTINGS[title][label]
            
            lbl = wx.StaticText(page, label=label)
            hbox.Add(lbl, flag=wx.RIGHT, border=8)
            
            item = self.field_from_value(page, value)
            
            if item!=None:
                hbox.Add(item, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)
            vbox.Add((-1, 5))
    
    def field_from_value(self, panel, value):
        if isinstance(value, basestring):
            return wx.TextCtrl(panel, value=value)
        elif isinstance(value, list):
            return wx.TextCtrl(panel, value=", ".join(value))
        elif isinstance(value, bool):
            item = wx.CheckBox(panel, -1, '', (120, 75))
            item.SetValue(value)
            return item
        elif isinstance(value, int):
            return wx.TextCtrl(panel, value=str(value))
        elif isinstance(value, dict):
            subpage = wx.Panel(panel)
            vbox = wx.BoxSizer(wx.VERTICAL)
            alpha = value.keys()
            alpha.sort()
            for lbl in alpha:
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                value2 = value[lbl]
                label = wx.StaticText(subpage, label=lbl)
                hbox.Add(label, flag=wx.RIGHT, border=8)
                item = self.field_from_value(subpage, value2)
                if item!=None:
                    hbox.Add(item, proportion=1)
                vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)
                vbox.Add((-1, 5))
            subpage.SetSizer(vbox)
            subpage.Show()
            return subpage
        return None

if __name__ == '__main__':
    app = wx.App(False)
    frame = SettingsFrame(None, "Caster Settings Window v " +settings.SOFTWARE_VERSION_NUMBER)
    app.MainLoop()