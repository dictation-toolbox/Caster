from dragonfly import RecognitionHistory
from dragonfly.actions.action_base import Repeat
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_playback import Playback

from castervoice.asynch.hmc import h_launch
from castervoice.lib import settings

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R, L, S
from castervoice.lib.util import recognition_history


class HistoryRule(BaseSelfModifyingRule):

    pronunciation = "history"
    mapping = {"default sequence": NullAction()}

    def __init__(self):
        super(HistoryRule, self).__init__(settings.settings(["paths", "SM_HISTORY_PATH"]))
        self._history = recognition_history.get_and_register_history(20)
        self._preserved = None

    def _record_from_history(self):
        """
        Inspects the recognition history, formats it for the GUI component which
        lets the user choose which of their prior utterances will become the
        Playbacks for the new command.
        """

        # save the list as it was when the command was spoken
        self._preserved = self._history[:]

        # format for display
        formatted = ""
        for t in self._preserved:
            for w in t:
                formatted += w.split("\\")[0] + "[w]"
            formatted += "[s]"
        formatted = formatted.encode("unicode_escape")
        # use a response window to get a spec and word sequences for the new macro
        h_launch.launch(settings.QTYPE_RECORDING, data=formatted)
        on_complete = AsynchronousAction.hmc_complete(lambda data: self._add_recorded_macro(data))
        AsynchronousAction([L(S(["cancel"], on_complete))],
                           time_in_seconds=0.5,
                           repetitions=300,
                           blocking=False).execute()

    def _add_recorded_macro(self, data):
        """
        Receives data asynchronously from a GUI component. Transforms said
        data into a new command.

        :param data: a dict containing both the spec and the indices of
            the selected utterances (which are stored locally) -- these
            are used to build the Playback actions. Also contains a
            boolean "repeatable" which indicates that the new command
            should get a repeat multiplier option added to it.
        :return:
        """
        spec = data["word"]

        word_sequences = []  # word_sequences is a list of lists of strings
        for i in data["selected_indices"]:
            # Convert from a tuple to a list because we may need to modify it.
            single_sequence = list(self._preserved[i])
            # clean the results
            for k in range(0, len(single_sequence)):
                if "\\" in single_sequence[k]:
                    single_sequence[k] = single_sequence[k].split("\\")[0]
            word_sequences.append(single_sequence)

        # clear the dictation cache
        self._preserved = None

        if spec != "" and len(word_sequences) > 0:
            if data["repeatable"]:
                spec += " [times <n>]"
            self._refresh(spec, word_sequences)

    def _refresh(self, *args):
        """
        :param args: [0] = spec,
                     [1] = list of lists of strings which becomes a series of Playback actions
        :return:
        """

        if len(args) > 0:
            spec = str(args[0])
            sequences = args[1]
            self._config.put(spec, sequences)
            self._config.save()
        else:
            self._config.replace({})

        self.reset()

    def _delete_recorded_macros(self):
        """
        Deletes all macros.
        """
        self._refresh()

    def _deserialize(self):
        mapping = {}
        recorded_macros = self._config.get_copy()
        for spec in recorded_macros:
            sequences = recorded_macros[spec]
            delay = settings.settings(["miscellaneous", "history_playback_delay_secs"])
            # The associative string (ascii_str) must be ascii, but the sequences within Playback must be Unicode.
            mapping[spec] = R(
                Playback([(sequence, delay) for sequence in sequences]),
                rdescript="Recorded Macro: " + spec) * Repeat(extra="n")
        mapping["record from history"] = R(
            Function(lambda: self._record_from_history()), rdescript="Record From History")
        mapping["delete recorded macros"] = R(
            Function(lambda: self._delete_recorded_macros()), rdescript="Delete Recorded Macros")
        self._smr_mapping = mapping


def get_rule():
    return [HistoryRule, RuleDetails(ccrtype=CCRType.SELFMOD)]
