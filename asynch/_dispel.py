import winsound

from dragonfly import (Function, Text, Grammar, BringApp, WaitWindow, Key,
                       IntegerRef, Dictation, Mimic, MappingRule)

from lib import paths
from lib import control
from lib import utilities


class Dispel:  # this needs an entry in the settings file, needs to retain information when Dragon is reset
    def __init__(self):
        self.minute = 60
        self.hour = 3600
        #
        self.settings = utilities.load_json_file(paths.DISPEL_JSON_PATH)
        self.PERIOD = 25  # number of minutes
        self.DELAY_AMOUNT = 5
        self.remaining = 0
        self.active = False
        self.load()  # load saved settings from last run
        if self.active:
            self.resume()
        
        
    def start(self):
        self.reset()
        utilities.report("T: " + str(self.remaining) + " m")
        control.TIMER_MANAGER.add_callback(self.tick, self.minute)
    def resume(self):
        utilities.report("T: " + str(self.remaining) + " m")
        control.TIMER_MANAGER.add_callback(self.tick, self.minute)
    def stop(self):
        self.active = False
        self.save_settings()
        utilities.report("ending dispel")
        control.TIMER_MANAGER.remove_callback(self.tick)
    
    def save_settings(self):
        self.settings["remaining"] = self.remaining
        self.settings["active"] = self.active
        utilities.save_json_file(self.settings, paths.DISPEL_JSON_PATH)
    def load(self):
        if "remaining" in self.settings and "active" in self.settings:
            self.remaining = int(self.settings["remaining"])
            self.active = self.settings["active"]
        else:
            self.remaining = self.PERIOD
            self.active = False
    
    def tick(self):  # one time increment passes
        self.remaining -= 1
        self.save_settings()
        if self.remaining <= 0:
            winsound.PlaySound(paths.ALARM_SOUND_PATH, winsound.SND_FILENAME)
        utilities.report("T: " + str(self.remaining) + " m")
        
    def delay(self):
        self.remaining += self.DELAY_AMOUNT
        
    def reset(self):
        self.active = True
        self.remaining = self.PERIOD

ALARM = Dispel()

class MainRule(MappingRule):
    mapping = {
    "run dispel":                   Function(ALARM.start),
    "kill dispel":                  Function(ALARM.stop),
    "resume dispel":                Function(ALARM.resume),
#
    "delay dispel":                 Function(ALARM.delay),
    "I am (sitting | standing) [now]":Function(ALARM.reset),
    }
    extras = [
              IntegerRef("n", 1, 500),
              IntegerRef("n2", 1, 500),
              Dictation("text"),
             ]
    defaults = {"n": 1, "n2": 1,
               "text": "",
               }

grammar = Grammar('dispel')
grammar.add_rule(MainRule())
grammar.load() 
