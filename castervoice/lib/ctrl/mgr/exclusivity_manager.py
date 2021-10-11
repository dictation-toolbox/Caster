from dragonfly import get_engine
from castervoice.lib import printer


# TODO: ExclusiveManager should be integrated into or with grammar_manager/grammar_activator?
class ExclusiveManager(object):
    """
    Loads and switches exclusivity for caster modes
    """
    def __init__(self):
        self.sleep_grammar = None
        self._get_engine = get_engine
        self._set_sleep_grammar()

    def set_mode(self, mode, modetype):
        """
        Sets modes
        :param mode: str - sleeping, on, off
        :param modetype: 'mic_mode' or 'engine_mode' str
        """
        if modetype == "mic_mode":
            if mode == "sleeping":
                self._set_grammar_exclusivity(self.sleep_grammar, True)
                printer.out("Caster: Microphone is sleeping")
            if mode == "on":
                self._set_grammar_exclusivity(self.sleep_grammar, False)
                printer.out("Caster: Microphone is on")
            if mode == "off":
                printer.out("Caster: Microphone is off")
        else:
            printer.out("{}, {} not implemented".format(mode, modetype))

    def _set_sleep_grammar(self):
        for grammar in self._get_engine().grammars:
            for rule in grammar.rules:
                if rule.exported and "CasterMicRule" in str(rule):
                    self.sleep_grammar = grammar
                    return
        else:
            printer.out("Caster: ExclusiveManager 'CasterMicRule' grammar not found, is it active? say 'enable caster mic modes'")

    def _set_grammar_exclusivity(self, grammar, state):
        grammar.set_exclusive(state)
        self._get_engine().process_grammars_context()
