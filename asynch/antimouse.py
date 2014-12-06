'''
Created on Nov 15, 2014

@author: dave
'''
import httplib
import itertools, glob
import json
import os
import signal
from subprocess import Popen
import sys
from threading import Timer

BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
sys.path.append(BASE_PATH)
from asynch import legion
from asynch.bottleserver import BottleServer
from asynch.legion import LegionScanner
from lib import utilities
from lib.systemtrayicon.sti import SysTrayIcon


class AMServer(BottleServer):
    def __init__(self):
        ''''''
        BottleServer.__init__(self, 1339)
    
    def process_requests(self):
        '''virtual method'''

class AntiMouse(SysTrayIcon):
    def __init__(self):
        self.server = None
        self.legion_scanner = None
        
        # stuff from the example
        self.icons = itertools.cycle(glob.glob('*.ico'))
        self.hover_text = "AntiMouse Dragon Assistant"
        menu_options = (('Say Hello', self.icons.next(), self.hello),
                    ('Switch Icon', None, self.switch_icon),
                    ('A sub-menu', self.icons.next(), (('Say Hello to Simon', self.icons.next(), self.simon),
                                                  ('Switch Icon', self.icons.next(), self.switch_icon),
                                                 ))
                   )
        Timer(1, self.start_everything).start()
        SysTrayIcon.__init__(self, self.icons.next(), self.hover_text, menu_options, on_quit=self.bye, default_menu_index=1)
        os.kill(os.getpid(), signal.SIGTERM)
    
    def hello(self, sysTrayIcon): print "Hello World."
    def simon(self, sysTrayIcon): 
        print "Hello Simon."
        Popen('pythonw C:/NatLink/NatLink/MacroSystem/lib/display.py'.split(),shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    def switch_icon(self, sysTrayIcon):
        sysTrayIcon.icon = self.icons.next()
        sysTrayIcon.refresh_icon()
    
    def bye(self, sysTrayIcon): 
        print 'Bye, then.'
    
    def start_everything(self):
        ''''''
        self.legion_scanner = LegionScanner()
        Timer(1, self.update).start()
        self.server = AMServer()
    
    def update(self):
        self.legion_scanner.scan()
        self.last = self.legion_scanner.get_update()
        if self.last!=None and utilities.window_exists(None, "legiongrid"):
            self.send("legion", self.last)
            
        Timer(10, self.update).start()
    
    def send(self, destination, data):
        formatted_data={}
        try:
            c = httplib.HTTPConnection('localhost', legion.LEGION_LISTENING_PORT)
            if destination=="legion":
                ''''''
                formatted_data["data_tirg"]=data[0]
                formatted_data["data_rex"]=data[1]
                formatted_data["redraw"]=True
            elif destination=="dragon":
                ''''''
            
            c.request('POST', '/process', json.dumps(formatted_data))
        except Exception:
            utilities.report(utilities.list_to_string(sys.exc_info()), log=True)


am = AntiMouse()
