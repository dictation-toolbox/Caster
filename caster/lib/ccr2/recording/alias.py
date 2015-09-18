'''
Created on Sep 3, 2015

@author: synkarius
'''
import re

from dragonfly.actions.action_function import Function
from dragonfly.actions.action_paste import Paste

from caster.asynch.hmc import h_launch
from caster.lib import context, utilities, settings, control
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import R


def read_highlighted(max_tries):
    for i in range(0, max_tries):
        result=context.read_selected_without_altering_clipboard(True)
        if result[0]==0: return result[1]
    return None

def delete_all(alias):
    utilities.save_json_file({}, settings.SETTINGS["paths"]["ALIAS_PATH"])
    alias.refresh()
    if hasattr(alias, "chain"): alias.chain.refresh()

class AliasesNon(SelfModifyingRule):
    mapping = {
        "default command":       NullAction(), 
        }
    json_path = "single_aliases"
    
    def alias(self, spec):
        spec = str(spec)
        if spec!="":
            text = read_highlighted(10)
            if text!=None: self.refresh(spec, str(text))
    
    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not AliasesNon.json_path in aliases:
            aliases[AliasesNon.json_path] = {}
        if len(args)>0:
            aliases[AliasesNon.json_path][args[0]] = args[1]
            utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[AliasesNon.json_path]:
            mapping[spec] = R(Paste(str(aliases[AliasesNon.json_path][spec])),rdescript="Alias: "+spec)
        mapping["alias <s>"] = R(Function(lambda s: self.alias(s)), rdescript="Create Alias")
        mapping["delete aliases"] = R(Function(lambda: delete_all(self)), rdescript="Delete Aliases")
        # 
        if hasattr(self, "chain"): mapping["chain alias"] = R(Function(self.chain.chain_alias), rdescript="Create Chainable Alias")
        self.reset(mapping)
    
    def set_chain(self, chain):
        self.chain = chain

class Aliases(SelfModifyingRule):
    json_path = "chain_aliases"
    
    mapping = {
        "default chain command":       NullAction(), 
        }
    
    def chain_alias(self):
        text = read_highlighted(10)
        if text!=None:
            h_launch.launch(settings.QTYPE_INSTRUCTIONS, 
                            lambda data: self.refresh(data[0].replace("\n", ""), text), 
                            "Enter_spec_for_command|")
    

    def refresh(self, *args):
        aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not Aliases.json_path in aliases:
            aliases[Aliases.json_path] = {}
        if len(args)>0 and args[0]!="":
            aliases[Aliases.json_path][args[0]] = args[1]
            utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[Aliases.json_path]:
            mapping[spec] = R(Paste(str(aliases[Aliases.json_path][spec])),rdescript="Chain Alias: "+spec)
        if len(mapping)<1: mapping = Aliases.mapping
        self.reset(mapping)

control.nexus().merger.add_selfmodrule(Aliases(), "chain alias")
control.nexus().merger.add_selfmodrule(AliasesNon(), "vanilla alias")
    