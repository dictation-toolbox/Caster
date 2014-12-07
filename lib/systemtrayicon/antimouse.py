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

from bottle import request

from asynch import legion
from asynch.bottleserver import BottleServer
from asynch.legion import LegionScanner
from lib import paths
from lib.systemtrayicon.sti import SysTrayIcon
from lib import runner
from lib import utilities


BASE_PATH = r"C:\NatLink\NatLink\MacroSystem"
sys.path.append(BASE_PATH)


class AMServer(BottleServer):
    def __init__(self, legion_update_fn):
        ''''''
        self.legion_update_fn=legion_update_fn
        BottleServer.__init__(self, 1339)
    
    def receive_request(self):
        with self.lock:
            self.incoming.append(json.loads(request.body.read()))
            self.process_requests()
    
    def process_requests(self):
        for r in self.incoming:
            if r["origin"]=="dragon":
                if r["type"]=="launch_Legion":
                    runner.run(["pythonw", paths.LEGION_PATH])
                    Timer(0.05, self.legion_update_fn).start()
                    
                ''''''
            elif r["origin"]=="msgbox":
                ''''''
            elif r["origin"]=="legion":
                if r["type"]=="req_tirg_update":
                    Timer(0.05, self.legion_update_fn).start()
        self.incoming=[]

class AntiMouse(SysTrayIcon):
    def __init__(self):
        self.server = None
        self.legion_scanner = None
        self.automatic_scan=False
        
        # system tray setup
        self.icons = itertools.cycle(glob.glob('*.ico'))
        self.hover_text = "AntiMouse Dragon Assistant"
        menu_options = (('Toggle Automatic Scans', self.icons.next(), self.toggle_automatic_scan),
#                     ('Switch Icon', None, self.switch_icon),
#                     ('A sub-menu', self.icons.next(), (('Say Hello to Simon', self.icons.next(), self.simon),
#                                                   ('Switch Icon', self.icons.next(), self.switch_icon),
#                                                  ))
                   )
        
        # 
        Timer(1, self.start_everything).start()
        SysTrayIcon.__init__(self, self.icons.next(), self.hover_text, menu_options, on_quit=self.bye, default_menu_index=1)
        os.kill(os.getpid(), signal.SIGTERM)
    
    def toggle_automatic_scan(self, sysTrayIcon):
        self.automatic_scan= not self.automatic_scan
        self.switch_icon(sysTrayIcon)
        if self.automatic_scan:
            self.update()
    
    
    def start_everything(self):
        ''''''
        self.legion_scanner = LegionScanner()
        Timer(1, self.update).start()
        self.server = AMServer(self.update)
    
    def update(self):
        self.legion_scanner.scan()
        self.last = self.legion_scanner.get_update()
        if self.last!=None and utilities.window_exists(None, "legiongrid"):
            self.send("legion", self.last)
        if self.automatic_scan:
            Timer(10, self.update).start()
    
    # demo stuff
    def hello(self, sysTrayIcon): print "Hello World."
    def simon(self, sysTrayIcon): 
        print "Hello Simon."
        runner.run('pythonw C:/NatLink/NatLink/MacroSystem/lib/display.py'.split())
    def switch_icon(self, sysTrayIcon):
        sysTrayIcon.icon = self.icons.next()
        sysTrayIcon.refresh_icon()
    def bye(self, sysTrayIcon): 
        print 'Bye, then.'
    
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
            utilities.simple_log(True)


if __name__ == '__main__':
    am = AntiMouse()
