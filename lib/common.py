'''
Created on Nov 30, 2014

@author: dave
'''
from dragonfly import RecognitionHistory
from dragonfly.timer import _Timer

from lib.filter import Filter

def get_instance(name):
    if name=="MULTI_CLIPBOARD":
        global MULTI_CLIPBOARD
        try:
            MULTI_CLIPBOARD
        except NameError:
            MULTI_CLIPBOARD={}
        return MULTI_CLIPBOARD
    elif name=="DICTATION_CACHE":
        global DICTATION_CACHE
        try:
            DICTATION_CACHE
        except NameError:
            DICTATION_CACHE=RecognitionHistory(10)
            DICTATION_CACHE.register()
        return DICTATION_CACHE
    elif name=="TIMER_MANAGER":
        global TIMER_MANAGER
        try:
            TIMER_MANAGER
        except NameError:
            TIMER_MANAGER=_Timer(1)
        return TIMER_MANAGER
    elif name=="FILTER":
        global FILTER
        try:
            FILTER
        except NameError:
            FILTER=Filter()
            # FILTER.initialize()
            # also need to do filter clean up, unloading
        return FILTER
    return


# preserves singletons
MULTI_CLIPBOARD = get_instance("MULTI_CLIPBOARD")
DICTATION_CACHE = get_instance("DICTATION_CACHE")
TIMER_MANAGER = get_instance("TIMER_MANAGER")
FILTER = get_instance("FILTER")

def print_startup_message():
    print "*- Starting Sorcery v.203 -*"







