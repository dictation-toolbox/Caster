import json
import os

from copy import deepcopy

from dragonfly import (
    MappingRule, Choice, Dictation, Grammar,
    Repeat, Function,RunCommand,RecognitionObserver
)
from dragonfly.engines.backend_text.engine import  TextInputEngine 


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

try : 
    last_state,last_rule,meaningful
except :    
    last_state = snippet_state.copy()
    last_rule = None
    meaningful = False

try :
    engine # upon reload keep the old engine and just to be sure clean it up
    for grammar in engine.grammars: 
        grammar.unload()
except :
    engine = TextInputEngine()

class SublimeSnippetControllRule(BaseSelfModifyingRule):
    last = None
    def __init__(self, *args, **kwargs):
        SublimeSnippetControllRule.last = self 
        super(SublimeSnippetControllRule, self).__init__(None,"sublime snippet control")
        # super(SublimeSnippetControllRule, self).__init__(os.path.join(settings.SETTINGS["paths"]["USER_DIR"],"nothing.toml"),"sublime snippet additional control")

    def rename(self,extra_name):
        return snippet_state["remap_data"].get(extra_name,extra_name)

    def get_last(self,field_name):
        rule = last_rule
        if type(last_rule).__name__.startswith("Repeat"):
            rule = last_rule.extras[1].children[0].rule
        if hasattr(rule,"_smr_" + field_name):
            return getattr(rule,"_smr_" + field_name)
        if hasattr(rule,field_name):
            return getattr(rule,field_name)
        else:
            raise ValueError("Problem inside sublime snippet control, the last rule was " + str(rule))
        # return grammars_with_snippets[last_rule][field_name]

    def _deserialize(self):
        global meaningful
        self._smr_mapping = {}
        self._smr_extras = []
        self._smr_defaults = {}
        names = snippet_state["extra_data"].keys()   # List[str]
        snippet = snippet_state["snippet"] # Union[str,List[str],Callable]
        if last_rule:
            meaningful = True
            default = self.get_last("defaults")
            if isinstance(snippet,str):
                self._smr_mapping = initial.copy()
                self._smr_extras =  [IntegerRefST("n",1,10)]
                self._smr_defaults =  {}
                meaningful = False
            elif isinstance(snippet,list):
                self._smr_mapping = initial.copy()
                self._smr_extras =  [IntegerRefST("n",1,len(snippet) + 1)]
                self._smr_defaults =  {}
            elif callable(snippet):
                for e in self.get_last("extras"): # Element
                    final_name = self.rename(e.name) 
                    if final_name in names:
                        self._smr_mapping["variant <"+e.name+">"] = R(Key("c-z") + SnippetVariant(**{e.name:final_name}))
                        self._smr_extras.append(e)
                        if isinstance(e,(Choice)) and e._extras is None:
                            spoken_name = final_name.upper() if len(final_name) == 1 else final_name
                            all_options = list(e._choices.values()) + ([default[e.name]] if e.name in default else [])
                            self._smr_mapping["display "+spoken_name+" variant"] = R(
                                Key("c-z") + DisplaySnippetVariants(final_name,all_options)
                            )
                        if isinstance(e,IntegerRefST):
                            spoken_name = final_name.upper() if len(final_name) == 1 else final_name
                            all_options = list(range(e._rule._element._min,e._rule._element._max))
                            self._smr_mapping["display "+spoken_name+" variant"] = R(
                                Key("c-z") + DisplaySnippetVariants(final_name,all_options)
                            )
        else:
            meaningful = True
            self._smr_mapping = initial.copy()
            self._smr_extras =  [IntegerRefST("n",1,10)]
            self._smr_defaults =  {}
            meaningful = False




    def process_recognition(self,node):
        words,successful = node.words(),{} # List[String],Dict[String,Any]
        for e in self._smr_extras:
            class LocalRule(MappingRule):
                mapping = {
                    "variant <"+e.name+">": 
                    Function(lambda **kwargs: 
                        successful.update({self.rename(k):v for k,v in kwargs.items() if k not in ["_node","_grammar","_rule"] }))
                }
                extras = [e]
            grammar = Grammar(e.name,engine=engine)
            grammar.add_rule(LocalRule())
            grammar.load()
            try : 
                engine.mimic(words)
            except :
                pass
            grammar.unload()
        assert successful or not "".join(words).strip().startswith("variant"),"Successful " + str(successful) + " words " + words
        if len(successful)==1 or not "".join(words).strip().startswith("variant"):
            MappingRule.process_recognition(self,node)
        else:
            (Key("c-z") + DisplayMultipleSnippetVariants(successful)).execute()
            

                
    def _refresh(self,rule = None,*args):
        global last_state,last_rule
        if  type(rule).__name__ == "SublimeSnippetControllRule":
            last_state = snippet_state.copy()
            return 
        if last_state != snippet_state and rule:
            last_state = snippet_state.copy()
            last_rule=rule
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
        
        if SublimeSnippetControllRule.last:
            SublimeSnippetControllRule.last._refresh(rule,words)
# data

observer = Observer()
observer.register()





def get_rule():
    return SublimeSnippetControllRule, RuleDetails(name="sublime snippet control", executable=["sublime_text"],function_context=lambda: meaningful)
    

    

    

