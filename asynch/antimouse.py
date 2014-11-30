'''
Created on Nov 15, 2014

@author: dave
'''
import itertools, glob
from threading import Timer

# from asynch.bottleserver import BottleServer
# from asynch.legion import LegionScanner
from lib.systemtrayicon.sti import SysTrayIcon


# class AMServer(BottleServer):
#     def __init__(self):
#         ''''''
#         BottleServer.__init__(self, 1339)
#         #am=BottleServer.Message()

class AntiMouse(SysTrayIcon):
    
    icons = itertools.cycle(glob.glob('*.ico'))
    hover_text = "AntiMouse Dragon Assistant"
    def hello(self, sysTrayIcon): print "Hello World."
    def simon(self, sysTrayIcon): print "Hello Simon."
    def switch_icon(self, sysTrayIcon):
        sysTrayIcon.icon = self.icons.next()
        sysTrayIcon.refresh_icon()
    
    def bye(self, sysTrayIcon): 
        print 'Bye, then.'
        raise IndexError()
        if self.server:
            self.server.die()
    
    def start_everything(self):
        ''''''
#         self.legion_scanner = LegionScanner()
#         self.server = AMServer()
    
    def __init__(self):
        self.server = None
        self.legion_scanner = None
        self.rectangle_scanner = None
        
        menu_options = (('Say Hello', self.icons.next(), self.hello),
                    ('Switch Icon', None, self.switch_icon),
                    ('A sub-menu', self.icons.next(), (('Say Hello to Simon', self.icons.next(), self.simon),
                                                  ('Switch Icon', self.icons.next(), self.switch_icon),
                                                 ))
                   )
        Timer(1, self.start_everything).start()
        SysTrayIcon.__init__(self, self.icons.next(), self.hover_text, menu_options, on_quit=self.bye, default_menu_index=1)
        print " do we get here "

# c = BottleServer(1338)
c = AntiMouse()
