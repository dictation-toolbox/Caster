from dragonfly import Function, Playback, RecognitionHistory

from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.short import R, L, S


class Again(MergeRule):
    def __init__(self):
        MergeRule.__init__(
            self,
            name="repeat that",
            extras=[IntegerRefST("n", 1, 50)],
            defaults={"n": 1},
            mapping={
                "again (<n> [(times|time)] | do)":
                    R(Function(lambda n: self._create_asynchronous(n)), show=False)
            })
        self._history = RecognitionHistory(10)

    @staticmethod
    def _repeat(utterance):
        Playback([(utterance, 0.0)]).execute()
        return False

    def _create_asynchronous(self, n):
        if len(self._history) == 0:
            return

        last_utterance_index = 1
        if settings.WSR:  # ContextStack adds the word to history before executing it
            if len(self._history) == 1: return
            last_utterance_index = 2

        utterance = [
            str(x) for x in " ".join(self._history[len(self._history) - last_utterance_index]).split()
        ]
        if utterance[0] == "again": return
        forward = [L(S(["cancel"], lambda: Again._repeat(utterance)))]
        AsynchronousAction(
            forward,
            rdescript="Repeat Last Action",
            time_in_seconds=0.2,
            repetitions=int(n),
            blocking=False).execute()


def get_rule():
    details = RuleDetails(name="again rule", rdp_mode_exclusion=True)
    return Again, details

