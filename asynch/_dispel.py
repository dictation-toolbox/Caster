import natlink
import winsound
from dragonfly import (Function, Text, Grammar, BringApp, WaitWindow, Key,
                       IntegerRef, Dictation, Mimic, MappingRule)
from lib import utilities, paths, settings

class Dispel:# this needs an entry in the settings file, needs to retain information when Dragon is reset
    def __init__(self):
        self.second = 1000
        self.minute = 60000
        self.hour = 3600000
        #
        self.period=25# number of minutes
        self.delay_amount=5
        self.remaining=self.period
        
    def start(self):
        self.reset()
        utilities.report("T: " +str(self.remaining)+" m")
        natlink.setTimerCallback(self.tick, self.minute)
    def stop(self):
        utilities.report("ending dispel")
        natlink.setTimerCallback(None, 0)
    
    def tick(self):# one time increment passes
        self.remaining-=1
        if self.remaining<=0:
            winsound.PlaySound(paths.ALARM_SOUND_PATH, winsound.SND_FILENAME)
        utilities.report("T: " +str(self.remaining)+" m")
        
    def delay(self):
        self.remaining+=self.delay_amount
        
    def reset(self):
        self.remaining=self.period

ALARM=Dispel()

class MainRule(MappingRule):
    mapping = {
    "run dispel":                   Function(ALARM.start),
    "kill dispel":                  Function(ALARM.stop),
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
