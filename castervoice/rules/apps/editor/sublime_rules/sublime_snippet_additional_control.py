import json
import os

from copy import deepcopy

from dragonfly import (MappingRule, Choice, Dictation, Grammar,Repeat, Function,RunCommand,FocusWindow,RecognitionObserver)


from castervoice.lib import settings, utilities, context, contexts
from castervoice.lib.actions import Key, Text
from castervoice.lib.const import CCRType
from castervoice.lib.context import AppContext
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

try : 
    from sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,snippet_state,send_sublime,SublimeCommand,grammars_with_snippets
except ImportError:
    from castervoice.rules.apps.editor.sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,snippet_state,grammars_with_snippets



initial = {
        "variant <n>":
            R(Key("c-z") + SnippetVariant(n="n")),
        "display variants":
            R(Key("c-z") + DisplaySnippetVariants()),
}


# global controll grammar WIP



last_keys = set()
last_rule = None

class SublimeSnippetAdditionalControllRule(BaseSelfModifyingRule):
    pronunciation = "sublime snippet additional control"
    observer = None
    last = None
    def __init__(self, *args, **kwargs):
        SublimeSnippetAdditionalControllRule.last = self 
        super(SublimeSnippetAdditionalControllRule, self).__init__(os.path.join(settings.SETTINGS["paths"]["USER_DIR"],"nothing.toml"),"sublime snippet additional control")


    def _deserialize(self):
        self._smr_mapping = initial.copy()
        self._smr_extras =  [IntegerRefST("n",1,10)]
        self._smr_defaults =  {}

        names = snippet_state["extra_data"].keys()        
        if last_rule:
            for e in grammars_with_snippets[last_rule]["extras"]:
                final_name = snippet_state["remap_data"].get(e.name,e.name)
                if isinstance(e,Choice) and final_name in names:
                    self._smr_mapping["variant <"+e.name+">"] = R(Key("c-z") + SnippetVariant(**{e.name:final_name}))
                    self._smr_extras.append(e)
                    all_options = list(e._choices.values())
                    if e.name in grammars_with_snippets[last_rule]["defaults"]:
                        default_item=grammars_with_snippets[last_rule]["defaults"][e.name]
                        if default_item not in all_options:
                            all_options.append(default_item)
                    spoken_name = grammars_with_snippets[last_rule]["rename"].get(e.name,e.name)
                    self._smr_mapping["display " + spoken_name + " variants"] = R(Key("c-z") + DisplaySnippetVariants(final_name,all_options))
        # print(self._smr_mapping)


    
    def _refresh(self,rule = None,*args):
        global last_keys,last_rule
        if type(rule) not in grammars_with_snippets:
            # print(rule,grammars_with_snippets.keys())
            return 
        if last_keys == set(snippet_state["extra_data"].keys()) and type(rule)==last_rule:
            return 0
        else:
            last_keys = set(snippet_state["extra_data"].keys())
            last_rule = type(rule)
            self.reset()

    
class Observer(RecognitionObserver):
    """docstring for Observer"""
    last = None
    def __init__(self, *args, **kw):
        super(Observer, self).__init__(*args, **kw)
        Observer.last = self

    def on_post_recognition(self, words, rule):
        if Observer.last is not self:
            self.unregister()
            return 
        if SublimeSnippetAdditionalControllRule.last:
            SublimeSnippetAdditionalControllRule.last._refresh(rule,words)

observer = Observer()
observer.register()



def get_rule():
    return SublimeSnippetAdditionalControllRule, RuleDetails(name="sublime snippet additional control", executable=["sublime_text"])
    

    

    

