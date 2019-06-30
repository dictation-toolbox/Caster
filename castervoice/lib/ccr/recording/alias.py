from castervoice.lib.imports import *
from castervoice.asynch.hmc import h_launch

_NEXUS = control.nexus()

def read_highlighted(max_tries):
    for i in range(0, max_tries):
        result = context.read_selected_without_altering_clipboard(True)
        if result[0] == 0: return result[1]
    return None


def delete_all(alias, path):
    aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
    aliases[path] = {}
    utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
    alias.refresh()

class AliasRule(SelfModifyingRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)
        self.nexus = nexus

    def alias(self, spec):
        text = read_highlighted(10)
        spec = str(spec)
        if text is not None:
            if spec:
                self.refresh(spec, str(text))
            else:
                h_launch.launch(settings.QTYPE_INSTRUCTIONS, data="Enter_spec_for_command|")
                on_complete = AsynchronousAction.hmc_complete(
                    lambda data: self.refresh(data[0].replace("\n", ""), text), self.nexus)
                AsynchronousAction(
                    [L(S(["cancel"], on_complete))],
                    time_in_seconds=0.5,
                    repetitions=300,
                    blocking=False).execute()


class Alias(AliasRule):
    mapping = {"default command": NullAction()}
    toml_path = "single_aliases"
    pronunciation = "alias"

    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not Alias.toml_path in aliases:
            aliases[Alias.toml_path] = {}
        if len(args) > 0:
            aliases[Alias.toml_path][args[0]] = args[1]
            utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[Alias.toml_path]:
            mapping[spec] = R(
                Text(str(aliases[Alias.toml_path][spec])),
                rdescript="Alias: " + spec)
        mapping["alias [<s>]"] = R(
            Function(lambda s: self.alias(s)), rdescript="Create Alias")
        mapping["delete aliases"] = R(
            Function(lambda: delete_all(self, Alias.toml_path)),
            rdescript="Delete Aliases")
        self.reset(mapping)


class ChainAlias(AliasRule):
    toml_path = "chain_aliases"
    mapping = {"default chain command": NullAction()}
    pronunciation = "chain alias"

    def refresh(self, *args):
        aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not ChainAlias.toml_path in aliases:
            aliases[ChainAlias.toml_path] = {}
        if len(args) > 0 and args[0] != "":
            aliases[ChainAlias.toml_path][args[0]] = args[1]
            utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[ChainAlias.toml_path]:
            mapping[spec] = R(
                Text(str(aliases[ChainAlias.toml_path][spec])),
                rdescript="Chain Alias: " + spec)
        mapping["chain alias [<s>]"] = R(
            Function(lambda s: self.alias(s)), rdescript="Create Chainable Alias")
        mapping["delete chain aliases"] = R(
            Function(lambda: delete_all(self, ChainAlias.toml_path)),
            rdescript="Delete Aliases")
        self.reset(mapping)

_NEXUS = control.nexus()

if settings.SETTINGS["feature_rules"]["alias"]:
    control.non_ccr_app_rule(Alias(_NEXUS), context=None, rdp=False, filter=False)

if settings.SETTINGS["feature_rules"]["chainalias"]:
    control.selfmod_rule(ChainAlias(_NEXUS))
