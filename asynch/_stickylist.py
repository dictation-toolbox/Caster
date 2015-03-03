import xmlrpclib

from dragonfly import (Function, Text, Grammar, BringApp, WaitWindow, Key,
                       IntegerRef, Dictation, Mimic, MappingRule, FocusWindow)
from lib import  settings
from lib import control
from lib import utilities
from lib.dragonfree import launch


def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(settings.ELEMENT_LISTENING_PORT))
def kill():
    communicate().kill()
def add_word():
    Mimic("copy", "one")._execute()
    communicate().add_name(control.MULTI_CLIPBOARD["1"])
def retrieve(n):
    n = int(n) - 1
    Text(communicate().retrieve(n))._execute()
def remove_word(n):
    n = int(n) - 1
    communicate().remove(n)
def scroll(n):  # n is the index of the list item to scroll to
    communicate().scroll(int(n)-1)
def focus_element():
    FocusWindow(title=settings.ELEMENT_VERSION)._execute()
    WaitWindow(title=settings.ELEMENT_VERSION)._execute()
    


def enable_element():
    launch.run(["pythonw", settings.SETTINGS["paths"]["ELEMENT_PATH"]])
    
#SSticky copy threeky copy toage
class ElementUsageRule(MappingRule):
    mapping = {
    "L scroll to <n>":              Function(scroll, extra="n"),
    "L get <n>":                    Function(retrieve, extra="n"),
    "L add word":                   Function(add_word),
    "L remove word <n>":            Function(remove_word, extra="n"),
    
    }   
    extras = [
              IntegerRef("n", 1, 200),
              IntegerRef("n2", 1, 100),
              Dictation("text"),
             ]
    defaults = {"n": 1, "n2": 1,
               "text": "",
               }

eur=ElementUsageRule()

class ElementLaunchRule(MappingRule):
    mapping = {
    "run element":                  Function(enable_element)+Function(eur.enable),
    "kill element":                 Function(kill)+Function(eur.disable),
    }   
    extras = []
    defaults = {}


elr=ElementLaunchRule()

grammar = Grammar('elementview')
grammar.add_rule(elr)
grammar.add_rule(eur)
grammar.load()

if not utilities.window_exists(classname= None, windowname=settings.ELEMENT_VERSION):
    eur.disable()
