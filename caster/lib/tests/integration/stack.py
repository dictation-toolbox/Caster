from Tkinter import Widget
import random
import time
import unittest

from dragonfly.actions.action_key import Key
from dragonfly.actions.action_pause import Pause
from dragonfly.actions.action_text import Text
from dragonfly.grammar.elements import Dictation
from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.rule_mapping import MappingRule

from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from caster.lib.dfplus.state.actions2 import ConfirmAction, BoxAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.tests.testutils import get_playback, get_output


LAST_TIME=0
def print_time():
    global LAST_TIME
    print(str(time.time()-LAST_TIME)[0])
    LAST_TIME=time.time()
def close_last_spoken(spoken):
    first = spoken[0]
    Text("</"+first+">").execute()
def close_last_rspec(rspec):
    Text("</"+rspec+">").execute()
def _abc(data):
    print(data)
FINISHER_TEXT="finisher successful"

class StackTest(MappingRule):
    '''test battery for the ContextStack'''
    
    
    mapping = {
        "close last tag":               ContextSeeker([L(S(["cancel"], None),
                                                         S(["html spoken"], close_last_spoken, use_spoken=True), 
                                                         S(["span", "div"], close_last_rspec, use_rspec=True))
                                                       ]),
        "html":                         R(Text("<html>"), rspec="html spoken"), 
        "divider":                      R(Text("<div>"), rspec="div"),
        "span":                         R(Text("<span>"), rspec="span"),
        "backward seeker [<text>]":     ContextSeeker([L(S(["ashes"], Text("ashes1 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery1 [%(text)s] "))), 
                                                       L(S(["ashes"], Text("ashes2 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery2 [%(text)s] ")))
                                                       ]), 
        "forward seeker [<text>]":      ContextSeeker(forward=
                                                      [L(S(["ashes"], Text("ashes1 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery1 [%(text)s] "))), 
                                                       L(S(["ashes"], Text("ashes2 [%(text)s] ")),
                                                          S(["bravery"], Text("bravery2 [%(text)s] ")))
                                                       ]),
        "asynchronous test":            AsynchronousAction([L(S(["ashes", "charcoal"], print_time, None),
                                                          S(["bravery"], Text, "bravery1"))
                                                       ], time_in_seconds=0.2, repetitions=20, 
                                                           finisher=Text(FINISHER_TEXT), 
                                                           blocking=False),
        "ashes":                        RegisteredAction(Text("ashes _ "), rspec="ashes"),
        "bravery":                      RegisteredAction(Text("bravery _ "), rspec="bravery"),
        "charcoal <text> [<n>]":        R(Text("charcoal _ %(text)s"), rspec="charcoal"),
                                
        "test confirm action":          ConfirmAction(Key("a"), rdescript="Confirm Action Test", instructions="some words here"),
        
        "test box action":              BoxAction(lambda data: _abc(data), rdescript="Test Box Action", box_type=settings.QTYPE_DEFAULT, 
                                                  log_failure=True),
    }
    extras = [
              Dictation("text"),
              Dictation("text2"),
              IntegerRefST("n", 1, 5)
             ]
    defaults = {"text": "", "text2": ""}



class TestOutput(unittest.TestCase):
    
    def setUp(self):
        self.grammar = Grammar("TestOutput_"+str(random.randint(0, 1000)))
        self.grammar.add_rule(StackTest())
        self.grammar.load()
    def tearDown(self):
        self.grammar.disable()
        self.grammar.unload()
        self.grammar = None

    def test_stack_actions(self):
        get_playback(["asynchronous test"]).execute()
        get_playback(["dot"]).execute()
        get_playback(["cancel"]).execute()
        output = get_output()
        self.assertTrue(output.count(FINISHER_TEXT)==0)
        
        get_playback(["asynchronous test"]).execute()
        Pause("500").execute()
        output = get_output()
        self.assertTrue(output.count(FINISHER_TEXT)==1)
        
        get_playback(["html", "close last tag"]).execute()
        output = get_output()
        self.assertEqual(output, "<html></html>")
        
        get_playback(["divider", "close last tag"]).execute()
        output = get_output()
        self.assertEqual(output, "<div></div>")
        