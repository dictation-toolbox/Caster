from dragonfly import get_engine, MimicFailure
from castervoice.lib import printer, control


# TODO: ExclusiveManager should be integrated into or with grammar_manager/grammar_activator?
class ExclusiveManager(object):
    """
    Loads and switches exclusivity for caster modes
    """
    def __init__(self):
        self._get_engine = get_engine
        self.rule_names = ["CasterMicRule", "DictationSinkRule"]
        self.exclusive_grammars = {}

    def set_mode(self, mode, modetype):
        """
        Sets modes
        :param mode: str - sleeping, on, off
        :param modetype: 'mic_mode' or 'engine_mode' str
        """
        if modetype == "mic_mode":
            self._get_grammars_loaded()
            if mode == "sleeping":
                self._set_grammars_exclusivity(self.exclusive_grammars, True)
                printer.out("Caster: Microphone is sleeping")
            if mode == "on":
                self._set_grammars_exclusivity(self.exclusive_grammars, False)
                printer.out("Caster: Microphone is on")
            if mode == "off":
                printer.out("Caster: Microphone is off")
        else:
            printer.out("{}, {} not implemented".format(mode, modetype))

    def _get_grammars_loaded(self):
        self.exclusive_grammars.clear()
        for rule_name in self.rule_names:
            for grammar in get_engine().grammars:
                for rule in grammar.rules:
                    if rule.exported and rule_name in str(rule):
                        self.exclusive_grammars.update({rule_name: grammar})
            if rule_name not in self.exclusive_grammars:
                self._activate_grammar(rule_name)

    def _activate_grammar(self, rule_name):
        # TODO: This is a hack. `_change_rule_enabled` should only be accessed in the grammar_manager         
        try:
            if str(rule_name) == "CasterMicRule":
                control.nexus()._grammar_manager._change_rule_enabled("CasterMicRule", True)
            if str(rule_name) == "DictationSinkRule":
                control.nexus()._grammar_manager._change_rule_enabled("DictationSinkRule", True)
            self._get_grammars_loaded()
        except MimicFailure as e:
            printer.out("Caster: {}".format(e))


    def _set_grammars_exclusivity(self, grammars, state):
        for rule_name, grammar in grammars.items():
            grammar.set_exclusive(state)
        self._get_engine().process_grammars_context()
