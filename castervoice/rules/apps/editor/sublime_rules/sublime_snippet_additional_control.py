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
    from sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,DisplayMultipleSnippetVariants,snippet_state,send_sublime,SublimeCommand,grammars_with_snippets
except ImportError:
    from castervoice.rules.apps.editor.sublime_rules.sublime_snippets import Snippet,SnippetVariant,DisplaySnippetVariants,DisplayMultipleSnippetVariants,snippet_state,grammars_with_snippets



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
                if final_name in names:
                    self._smr_mapping["variant <"+e.name+">"] = R(Key("c-z") + SnippetVariant(**{e.name:final_name}))
                    self._smr_extras.append(e)
                    # try : 
                    #     self._smr_defaults[e.name] = grammars_with_snippets[last_rule]["defaults"][e.name] 
                    # except KeyError:
                    #     pass

                    # self._smr_mapping["display " + spoken_name + " variants"] = R(Key("c-z") + DisplaySnippetVariants(final_name,all_options))
        # print(self._smr_mapping)


    def process_recognition(self,node):
        from dragonfly import Grammar
        from dragonfly.engines.backend_text.engine import  TextInputEngine as get_engine 
        # from dragonfly.engines.backend_text import  get_engine 

        words = node.words()
        successful = {}
        engine = get_engine()
        for e in self._smr_extras:
            class LocalRule(MappingRule):
                mapping = {
                    "variant <"+e.name+">": 
                    Function(lambda **kwargs: 
                        successful.update({k:v for k,v in kwargs.items() if k not in ["_node","_grammar","_rule"] }))
                }
                extras = [e]
            grammar = Grammar("grammar",engine=engine)
            grammar.add_rule(LocalRule())
            grammar.load()
            # engine.load_grammar(grammar)
            try : 
                engine.mimic(words)
            except :
                pass
            # grammar.unload()
        assert successful
        print("successful",successful,engine.grammars,"authornot Oscar vast echor")
        if len(successful)==1:
            MappingRule.process_recognition(self,node)
        else:
            (Key("c-z") + DisplayMultipleSnippetVariants(successful)).execute()













                
    def _refresh(self,rule = None,*args):
        global last_keys,last_rule
        # print(rule,grammars_with_snippets.keys())
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
    # last = None
    def __init__(self, *args, **kw):
        super(Observer, self).__init__(*args, **kw)
        Observer.last = self

    def on_post_recognition(self, node,words, rule):

        if Observer.last is not self:
            self.unregister()
            return 
        if SublimeSnippetAdditionalControllRule.last:
            SublimeSnippetAdditionalControllRule.last._refresh(rule,words)
# data

observer = Observer()
observer.register()





def get_rule():
    return SublimeSnippetAdditionalControllRule, RuleDetails(name="sublime snippet additional control", executable=["sublime_text"])
    

    

    

