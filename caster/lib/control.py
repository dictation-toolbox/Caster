import logging
from threading import Timer
import time

from dragonfly import RecognitionHistory, Grammar, Mimic
from dragonfly.actions.action_function import Function

from caster.lib import settings, utilities
from caster.lib.dfplus.communication import Communicator
from caster.lib.dfplus.merge.ccrmerger import CCRMerger, Inf


_NEXUS = None

if settings.WSR == False:
    import natlink

class AutoSwitcher(object):
    def __init__(self, nexus):
        self._nexus = nexus
        self._last = False
        self._has_run_first_time = False
        self.auto_enabled_languages = None
        self.last_extension = None
        self.is_natlink = settings.WSR == False
        
        self._ON = Mimic("command", "mode", "on")+Function(lambda: nexus.intermediary.text("Command Mode On"))
        self._OFF = Mimic("command", "mode", "off")+Function(lambda: nexus.intermediary.text("Command Mode Off"))
        self.begin()
    
    def begin(self):
        ''''''
        if settings.SETTINGS["auto_com"]["active"]:
            if self._nexus.dep.NATLINK and not settings.WSR:
                self._nexus.timer.add_callback(lambda: self._toggle(), settings.SETTINGS["auto_com"]["interval"])
            else:
                utilities.availability_message("Auto-Command-Mode", "natlink")
    
    def _toggle(self):
        if self.is_natlink and natlink.getMicState()!="on":
            return
        
        '''determines whether to toggle and then if so toggles appropriately'''
        should_toggle = False
        if not self._has_run_first_time:
            should_toggle = True
            self._has_run_first_time = True
        if not settings.SETTINGS["auto_com"]["change_language_only"]:
            current_window = utilities.get_active_window_path().split("\\")[-1]
            should_be_on = current_window in settings.SETTINGS["auto_com"]["executables"]
            should_toggle = should_be_on != self._last
            self._last = should_be_on
        
            if should_toggle:
                e = self._ON if self._last else self._OFF
                e.execute()
        
        '''language switching section'''
        if settings.SETTINGS["auto_com"]["change_language"]:
            self._toggle_language()
    
    def _send_message(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            self._nexus.intermediary.text(message)
    
    def _toggle_language(self):
        '''attempt to figure out what the file extension in the active window is'''
        filename, folders, title = utilities.get_window_title_info()
        extension = None
        if filename is not None: extension = "." + filename.split(".")[-1]
        
        '''see if the file extension changed'''
        if self.last_extension != extension:
            
            '''autos is a generated registry of:
               {extension: [language rule names]}'''
            autos = self._nexus.merger.language_autos()
            
            if extension is not None and extension in autos.keys(): # if the extension is registered
                languages = autos[extension] # get the languages to activate for that extension
                
                for language in languages: # activate them
                    self._nexus.merger.merge(Inf.RUN, language, enable=True)
                    self._send_message("Enabled '"+language+"'")
                    
                self.auto_enabled_languages = languages
                
            elif self.auto_enabled_languages is not None:
                for language in self.auto_enabled_languages:
                    self._nexus.merger.merge(Inf.RUN, language, enable=False)
                    self._send_message("Disabled '"+language+"'")
                self.auto_enabled_languages = None
                
        
        self.last_extension = extension

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
        self.auto = AutoSwitcher(self)
    
    def inform_state(self, state):# resolves circular import 
        self.state = state
        

def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS













