from dragonfly import (BringApp, Key, Function, Text, Grammar, Playback, 
                       IntegerRef,Dictation,Choice,Mimic,MappingRule)
import sys, httplib, json
import paths, utilities, helpdisplay

def retrieve(n):
    n = int(n)-1
    Text(send("retrieve", n))._execute()

def scroll(n):#n is the index of the list item to scroll to
    send("scroll", (int(n)-1))

def sticky_from_unordered(n, n2):
    n = int(n)-1# index of word in unordered list
    if n<10:
        n=n+10
    n2 = int(n2)-1# index of target slot in sticky list
    send("sticky", n, n2, "")
    
def sticky_copy(n):
    n = int(n)-1# index of target slot in sticky list
    Mimic("copy","one")._execute()
    send("sticky", "1", n, utilities.MULTI_CLIPBOARD["1"])

def add_word():
    Mimic("copy","one")._execute()
    send("add", utilities.MULTI_CLIPBOARD["1"])

def remove_word(n):
    n = int(n)-1
    send("remove", n)

def send(action_type, data, *more_data):
    try:
        c = httplib.HTTPConnection('localhost', 1337)
        data_to_send={}
        data_to_send["action_type"]=str(action_type)
        if action_type in ["retrieve","sticky","remove","unsticky","scroll"]:
            data_to_send["index"]=data
            if action_type=="sticky":
                data_to_send["sticky_index"]=more_data[0]
                data_to_send["auto_sticky"]=more_data[1]
        elif action_type in ["add"]:
            data_to_send["name"]=data
        c.request('POST', '/process', json.dumps(data_to_send))
        doc = c.getresponse().read()
        if len(doc)>100:
            doc="length error in send()"
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
    "sticky list <n> to <n2>":      Function(sticky_from_unordered, extra={"n","n2"}),
    "sticky copy [<n>]":            Function(sticky_copy, extra="n"),
    "add word":                     Function(add_word),
    "remove word <n>":              Function(remove_word, extra="n"),
    
    
    
    }
    extras = [
              IntegerRef("n", 1, 500),
              IntegerRef("n2", 1, 500),
              Dictation("text"),
             ]
    defaults ={"n": 1,"n2": 1,
               "text": "", 
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