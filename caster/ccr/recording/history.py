from dragonfly.actions.action_base import Repeat
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_playback import Playback

from caster.lib.asynch.hmc import h_launch
from caster.lib import control
from caster.lib import settings, utilities
from caster.lib.dfplus.merge.selfmodrule import SelfModifyingRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.actions2 import NullAction
from caster.lib.dfplus.state.short import R, L, S

_NEXUS = control.nexus()


class HistoryRule(SelfModifyingRule):
    def __init__(self, nexus):
        SelfModifyingRule.__init__(self)
        self.nexus = nexus

    pronunciation = "history"
    mapping = {"default sequence": NullAction()}

    def record_from_history(self):
        # save the list as it was when the command was spoken
        self.nexus.preserved = self.nexus.history[:]

        # format for display
        formatted = ""
        for t in self.nexus.preserved:
            for w in t:
                formatted += w.split("\\")[0] + "[w]"
            formatted += "[s]"

        # use a response window to get a spec and word sequences for the new macro
        h_launch.launch(settings.QTYPE_RECORDING, data=formatted)
        on_complete = AsynchronousAction.hmc_complete(
            lambda data: self.add_recorded_macro(data), self.nexus)
        AsynchronousAction(
            [L(S(["cancel"], on_complete))],
            time_in_seconds=0.5,
            repetitions=300,
            blocking=False).execute()

    def add_recorded_macro(self, data):
        spec = data["word"]

        word_sequences = []  # word_sequences is a list of lists of strings
        for i in data["selected_indices"]:
            # Convert from a tuple to a list because we may need to modify it.
            single_sequence = list(self.nexus.preserved[i])
            # clean the results
            for k in range(0, len(single_sequence)):
                if "\\" in single_sequence[k]:
                    single_sequence[k] = single_sequence[k].split("\\")[0]
            word_sequences.append(single_sequence)

        # clear the dictation cache
        self.nexus.preserved = None

        if spec != "" and len(word_sequences) > 0:
            if data["repeatable"]:
                spec += " [times <n>]"
            self.refresh(spec, word_sequences)

    def refresh(self, *args):
        '''args: spec, list of lists of strings'''

        # get mapping
        recorded_macros = utilities.load_toml_file(
            settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        if len(args) > 0:
            recorded_macros[args[0]] = args[1]
            utilities.save_toml_file(recorded_macros,
                                     settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        mapping = {}
        for spec in recorded_macros:
            # Create a copy of the string without Unicode characters.
            ascii_str = str(spec)
            sequences = recorded_macros[spec]
            delay = settings.SETTINGS["miscellaneous"]["history_playback_delay_secs"]
            # It appears that the associative string (ascii_str) must be ascii, but the sequences within Playback must be Unicode.
            mapping[ascii_str] = R(
                Playback([(sequence, delay) for sequence in sequences]),
                rdescript="Recorded Macro: " + ascii_str)
        mapping["record from history"] = R(
            Function(self.record_from_history), rdescript="Record From History")
        mapping["delete recorded macros"] = R(
            Function(self.delete_recorded_macros), rdescript="Delete Recorded Macros")
        # reload with new mapping
        self.reset(mapping)

    def load_recorded_macros(self):
        self.refresh()

    def delete_recorded_macros(self):
        utilities.save_toml_file({}, settings.SETTINGS["paths"]["RECORDED_MACROS_PATH"])
        self.refresh()


_NEXUS.merger.add_selfmodrule(HistoryRule(_NEXUS))
