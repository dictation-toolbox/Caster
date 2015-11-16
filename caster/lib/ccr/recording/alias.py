

from dragonfly.actions.action_function import Function
from dragonfly.actions.action_text import Text

from caster.asynch.hmc import h_launch
from caster.lib import context, utilities, settings
from caster.lib import control
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import R, L, S

_NEXUS = control.nexus()


def read_highlighted(max_tries):
    for i in range(0, max_tries):
        result=context.read_selected_without_altering_clipboard(True)
        if result[0]==0: return result[1]
    return None

def delete_all(alias, path):
    aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
    aliases[path] = {}
    utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
    alias.refresh()

class VanillaAlias(SelfModifyingRule):
    mapping = { "default vanilla command":       NullAction() }
    json_path = "single_aliases"
    pronunciation = "vanilla alias"
    
    def vanilla_alias(self, spec):
        spec = str(spec)
        if spec!="":
            text = read_highlighted(10)
            if text!=None: self.refresh(spec, str(text))
    
    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not VanillaAlias.json_path in aliases:
            aliases[VanillaAlias.json_path] = {}
        if len(args)>0:
            aliases[VanillaAlias.json_path][args[0]] = args[1]
            utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[VanillaAlias.json_path]:
            mapping[spec] = R(Text(str(aliases[VanillaAlias.json_path][spec])),rdescript="Alias: "+spec)
        mapping["vanilla alias <s>"] = R(Function(lambda s: self.vanilla_alias(s)), rdescript="Create Vanilla Alias")
        mapping["delete vanilla aliases"] = R(Function(lambda: delete_all(self, VanillaAlias.json_path)), rdescript="Delete Vanilla Aliases")
        self.reset(mapping)


class ChainAlias(SelfModifyingRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)
        self.nexus = nexus
    
    json_path = "chain_aliases"    
    mapping = { "default chain command":       NullAction() }
    pronunciation = "chain alias"
    
    def chain_alias(self):
        text = read_highlighted(10)
        if text is not None:
            h_launch.launch(settings.QTYPE_INSTRUCTIONS, data="Enter_spec_for_command|")
            on_complete = AsynchronousAction.hmc_complete(lambda data: self.refresh(data[0].replace("\n", ""), text), self.nexus)
            AsynchronousAction([L(S(["cancel"], on_complete, None))], 
                               time_in_seconds=0.5, 
                               repetitions=300, 
                               blocking=False).execute()
    
    

    def refresh(self, *args):
        aliases = utilities.load_json_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not ChainAlias.json_path in aliases:
            aliases[ChainAlias.json_path] = {}
        if len(args)>0 and args[0]!="":
            aliases[ChainAlias.json_path][args[0]] = args[1]
            utilities.save_json_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[ChainAlias.json_path]:
            mapping[spec] = R(Text(str(aliases[ChainAlias.json_path][spec])),rdescript="Chain Alias: "+spec)
        mapping["chain alias"] = R(Function(self.chain_alias), rdescript="Create Chainable Alias")
        mapping["delete chain aliases"] = R(Function(lambda: delete_all(self, ChainAlias.json_path)), rdescript="Delete Vanilla Aliases")
        self.reset(mapping)

control.nexus().merger.add_selfmodrule(ChainAlias(_NEXUS))

    