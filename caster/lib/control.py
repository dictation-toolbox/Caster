import logging
from threading import Timer
import time

from dragonfly import RecognitionHistory, Grammar

from caster.lib import settings, utilities
from caster.lib.dfplus.communication import Communicator
from caster.lib.dfplus.merge.ccrmerger import CCRMerger


_NEXUS = None

class StatusIntermediary:
    def __init__(self, c):
        self.communicator = c
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").hint(message)
        else:
            utilities.report(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self.communicator.get_com("status").text(message)
        else:
            utilities.report(message)
    def kill(self):
        if utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
            self.communicator.get_com("status").kill()

class DependencyMan:
    def __init__(self):
        if not settings.WSR:
            self.list = [
                       ("natlink", None, ["Auto-Command full capabilities"], "http://sourceforge.net/projects/natlink"),
                       ("PIL", None, ["Legion"], "https://pypi.python.org/pypi/Pillow"),
                       #("wx", None, ["Settings Window"], "http://www.wxpython.org"),
                       ("win32ui", "pywin32", ["very many essential"], "http://sourceforge.net/projects/pywin32")
                        ]
            warnings = 0
            for dep in self.list:
                is_win32ui = dep[0] == "win32ui"
                try:
                    exec("import " + dep[0])
                except Exception:
                    if not dep[0] in settings.SETTINGS["one time warnings"]:
                        warnings += 1
                        settings.SETTINGS["one time warnings"][dep[0]] = True
                        urgency = "You can get it at " if is_win32ui else "If you wish to use those features, you can get it at "
                        print "\n" + dep[0] + " is required for ", dep[2], " features. " + urgency + dep[3] + "\n"
                else:
                    name = dep[0] if not is_win32ui else dep[1]
                    exec("self." + name.upper() + "=True")
            if warnings > 0:
                settings.save_config()

    NATLINK = False
    PIL = False
    PYWIN32 = False
    WX = False

class TimerForWSR(object):
    '''
    Copied verbatim from Dragonfly, but doesn't require
    Natlink and has been those parts reimplemented    
    '''
    class Callback(object):
        def __init__(self, function, interval):
            self.function = function
            self.interval = interval
            self.next_time = time.clock() + self.interval
        def call(self):
            self.next_time += self.interval
            try:
                self.function()
            except Exception, e:
                logging.getLogger("timer").exception("Exception during timer callback")
                print "Exception during timer callback: %s (%r)" % (e, e)

    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []
        self._continue = {"_continue": False}

    def add_callback(self, function, interval):
        self.callbacks.append(self.Callback(function, interval))
        print len(self.callbacks)
        if len(self.callbacks) == 1:
            self.setTimerCallback(self.callback)

    def remove_callback(self, function):
        for c in self.callbacks:
            if c.function == function: self.callbacks.remove(c)
        if len(self.callbacks) == 0:
            self.setTimerCallback(None)

    def callback(self):
        now = time.clock()
        for c in self.callbacks:
            if c.next_time < now: c.call()
    
    def setTimerCallback(self, callback):
        _continue = self._continue
        if callback==None:
            _continue["_continue"] = False
        else:
            _continue["_continue"] = True
            _interval = self.interval
            def call():
                if _continue["_continue"]:
                    callback()
                    Timer(_interval, call).start()
            Timer(_interval, call).start()

class Nexus:
    def __init__(self):
        
        self.state = None
        self.clip = {}
        self.sticky = []
        self.history = []
        if not settings.WSR:
            self.history = RecognitionHistory(20)
            self.history.register()
        self.preserved = None
        
        self.comm = Communicator()
        self.intermediary = StatusIntermediary(self.comm)
        self.timer = TimerForWSR(0.025)
        if not settings.WSR:
            from dragonfly.timer import _Timer
            self.timer = _Timer(0.025)
        self.dep = DependencyMan()
        
        self.macros_grammar = Grammar("recorded_macros")
        self.noderules = []
        
        self.merger = CCRMerger()
    
    def inform_state(self, state):# resolves circular import 
        self.state = state
        

def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS













