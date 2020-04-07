from dragonfly import Function, Playback, RecognitionHistory, MappingRule, get_current_engine

from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.short import R, L, S
from castervoice.lib.util import recognition_history

_history = recognition_history.get_and_register_history(10)


class Again(MappingRule):

    mapping = {
        "again (<n> [(times|time)] | do)":
            R(Function(lambda n: Again._create_asynchronous(n)), show=False),  # pylint: disable=E0602
    }
    extras = [IntegerRefST("n", 1, 50)]
    defaults = {"n": 1}

    @staticmethod
    def _repeat(utterance):
        Playback([(utterance, 0.0)]).execute()
        return False

    @staticmethod
    def _create_asynchronous(n):
        if len(_history) == 0:
            return

        last_utterance_index = 2
        if get_current_engine().name in ["sapi5shared", "sapi5", "sapi5inproc"]:  # ContextStack adds the word to history before executing it
            if len(_history) == 1: return
            last_utterance_index = 2

        utterance = [
            str(x) for x in " ".join(_history[len(_history) - last_utterance_index]).split()
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
    details = RuleDetails(name="repeat that")
    return Again, details
