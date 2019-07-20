from castervoice.lib.imports import *
from castervoice.asynch.hmc import h_launch


class _BaseAliasRule(SelfModifyingRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)
        self.nexus = nexus

    def _alias(self, spec):
        text = _BaseAliasRule._read_highlighted(10)
        spec = str(spec)
        if text is not None:
            if spec:
                self._refresh(spec, str(text))
            else:
                h_launch.launch(settings.QTYPE_INSTRUCTIONS, data="Enter_spec_for_command|")
                on_complete = AsynchronousAction.hmc_complete(
                    lambda data: self._refresh(data[0].replace("\n", ""), text), self.nexus)
                AsynchronousAction(
                    [L(S(["cancel"], on_complete))],
                    time_in_seconds=0.5,
                    repetitions=300,
                    blocking=False).execute()

    def _delete_all(self, path):
        aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        aliases[path] = {}
        utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        self._refresh()

    @staticmethod
    def _read_highlighted(max_tries):
        for i in range(0, max_tries):
            result = context.read_selected_without_altering_clipboard(True)
            if result[0] == 0: return result[1]
        return None


class BaseAlias(_BaseAliasRule):
    mapping = {"default command": NullAction()}
    toml_path = "single_aliases"
    pronunciation = "alias"

    def _refresh(self, *args):
        """
        Takes a spec and text, creates a Text command, resets with new info.

        :param args: spec, text
        :return:
        """
        aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not BaseAlias.toml_path in aliases:
            aliases[BaseAlias.toml_path] = {}
        if len(args) > 0:
            aliases[BaseAlias.toml_path][args[0]] = args[1]
            utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[BaseAlias.toml_path]:
            mapping[spec] = R(
                Text(str(aliases[BaseAlias.toml_path][spec])),
                rdescript="Alias: " + spec)
        mapping["alias [<s>]"] = R(
            Function(lambda s: self._alias(s)), rdescript="Create Alias")
        mapping["delete aliases"] = R(
            Function(lambda: self._delete_all(BaseAlias.toml_path)),
            rdescript="Delete Aliases")
        self.reset(mapping)


class ChainBaseAlias(_BaseAliasRule):
    toml_path = "chain_aliases"
    mapping = {"default chain command": NullAction()}
    pronunciation = "chain alias"

    def _refresh(self, *args):
        aliases = utilities.load_toml_file(settings.SETTINGS["paths"]["ALIAS_PATH"])
        if not ChainBaseAlias.toml_path in aliases:
            aliases[ChainBaseAlias.toml_path] = {}
        if len(args) > 0 and args[0] != "":
            aliases[ChainBaseAlias.toml_path][args[0]] = args[1]
            utilities.save_toml_file(aliases, settings.SETTINGS["paths"]["ALIAS_PATH"])
        mapping = {}
        for spec in aliases[ChainBaseAlias.toml_path]:
            mapping[spec] = R(
                Text(str(aliases[ChainBaseAlias.toml_path][spec])),
                rdescript="Chain Alias: " + spec)
        mapping["chain alias [<s>]"] = R(
            Function(lambda s: self._alias(s)), rdescript="Create Chainable Alias")
        mapping["delete chain aliases"] = R(
            Function(lambda: self._delete_all(ChainBaseAlias.toml_path)),
            rdescript="Delete Aliases")
        self.reset(mapping)


_NEXUS = control.nexus()

if settings.SETTINGS["feature_rules"]["alias"]:
    control.non_ccr_app_rule(BaseAlias(_NEXUS), context=None, rdp=False, filter=False)

if settings.SETTINGS["feature_rules"]["chainalias"]:
    control.selfmod_rule(ChainBaseAlias(_NEXUS))
