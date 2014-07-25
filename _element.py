from dragonfly import (BringApp, Key, Function, Text, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,WaitWindow,MappingRule)
import sys, httplib, json
import paths, utilities, helpdisplay

def retrieve(n):
    n = int(n)-1
    Text(send("retrieve", n))._execute()

def scroll(n):#n is the index of the list item to scroll to
    send("scroll", (int(n)-1))

def send(action_type, data):
    try:
        c = httplib.HTTPConnection('localhost', 1337)
        data_to_send={}
        data_to_send["action_type"]=str(action_type)
        if action_type in ["retrieve","sticky","delete","unsticky","scroll"]:
            data_to_send["index"]=data
        elif action_type in ["add"]:
            data_to_send["name"]=data
        c.request('POST', '/process', json.dumps(data_to_send))
        doc = c.getresponse().read()
        utilities.report(doc)
        return doc
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
        return "SEND() ERROR"

def enable_element_commands():
    # to do: bringapp on the executable
    grammar.enable()
    enabler.disable()
    
def disable_element_commands():
    # to do:  kill the executable
    grammar.disable()
    enabler.enable()

class MainRule(MappingRule):
    mapping = {
    "disable element":              Function(disable_element_commands),
    "scroll to <n>":                Function(scroll, extra="n"),
    "get <n>":                      Function(retrieve, extra="n"),
    
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
grammar.disable()

class EnablerRule(MappingRule):
    mapping = {
    "enable element":              Function(enable_element_commands),
    }

enabler = Grammar('element_enabler')
enabler.add_rule(EnablerRule())
enabler.load()