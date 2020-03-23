import json
import os

from copy import deepcopy

from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow)
from dragonfly import *

from castervoice.lib import settings, utilities, context, contexts
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from castervoice.lib.sublime import send_sublime,SublimeCommand
from castervoice.lib.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,snippet_state

from castervoice.lib.const import CCRType

initial = {
        "variant <n>":
            R(Key("c-z") + SnippetVariant(n="n")),
        "display variants":
            R(Key("c-z") + DisplaySnippetVariants()),
}

# 
# global controll grammar WIP
#

last_keys = set()

class SublimeSnippetAdditionalControllRule(BaseSelfModifyingRule):
    pronunciation = "sublime snippet additional control"

    last = None
    def __init__(self, *args, **kwargs):
        def printr(*args):
            print(args)
        SublimeSnippetAdditionalControllRule.last = self 
        super(SublimeSnippetAdditionalControllRule, self).__init__(os.path.join(settings.SETTINGS["paths"]["USER_DIR"],"nothing.toml"),"sublime snippet additional control")


    def _deserialize(self):
        self._smr_mapping = initial.copy()
        self._smr_extras =  [IntegerRefST("n",1,10)]
        self._smr_defaults =  {}
        for name in snippet_state["extra_data"].keys():

            print(name)
            self._smr_mapping["variant show "+name] = R(Text(name))
            print(self._smr_mapping)

    
    def _refresh(self):
        print("The refreshing snippets",snippet_state)
        global last_keys
        if last_keys == set(snippet_state["extra_data"].keys()):
            return 
        else:
            Text("refreshed").execute()
            last_keys = set(snippet_state["extra_data"].keys())
            self.reset()
        # self.reset()try : 
#dear
#---------------------------------------------------------------------------
refresh_after_command_callback = lambda *args,**kwargs: SublimeSnippetAdditionalControllRule.last._refresh() if SublimeSnippetAdditionalControllRule.last else None
# refresh_after_command_callback = lambda words,rule:SublimeSnippetAdditionalControllRule.last._refresh() if SublimeSnippetAdditionalControllRule.last else None
register_post_recognition_callback(refresh_after_command_callback)

    


def get_rule():
    return SublimeSnippetAdditionalControllRule, RuleDetails(ccrtype=CCRType.SELFMOD, executable=["sublime_text"])
    

    

    

 
    


