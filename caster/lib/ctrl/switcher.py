'''
Created on Oct 7, 2015

@author: synkarius
'''
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_mimic import Mimic

from caster.lib import settings, utilities
from caster.lib.dfplus.merge.ccrmerger import Inf

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