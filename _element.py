from dragonfly import (BringApp, Key, Function, Text, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,WaitWindow,MappingRule)
import sys, httplib, json
import paths, utilities, helpdisplay

def run_element():
    
    try:
        c = httplib.HTTPConnection('localhost', 1337)
        data_to_send={}
        data_to_send["action_type"]="retrieve"
        data_to_send["index"]=0
        c.request('POST', '/process', json.dumps(data_to_send))
        doc = c.getresponse().read()
        utilities.report(doc)
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))

class MainRule(MappingRule):
    
    mapping = {
    "element request":              Function(run_element),
    
    
    }
    extras = [
              IntegerRef("n", 1, 1000),
              Dictation("text"),
             ]
    defaults ={"n": 1,
               "text": ""
               }

grammar = Grammar('element')
grammar.add_rule(MainRule())
grammar.load()
